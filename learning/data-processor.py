import aiocouch
import asyncio
import argparse

import numpy as np

from data.data_classes import Maze, Openings, Opening

parser = argparse.ArgumentParser(
                    prog='Data Processor',
                    description='Preprocess maze data for use in machine learning')
parser.add_argument('--maze-size', type=int, default=10)
parser.add_argument('--explorer', action='store_true')
args = parser.parse_args()


async def process_data(db: aiocouch.Database):
    results = db.find({
        "$and": [
            {
                "width": str(args.maze_size),
            },
            {
                "height": str(args.maze_size)
            }
        ]
    }, limit=1000)

    results = [r.json async for r in results]

    mazes = [Maze.from_database(**res) for res in results]

    X = [maze.openings.to_np_array() for maze in mazes]
    y = [maze.optimal_path.to_np_array() for maze in mazes]

    np.save("mazes.npy", np.array(X))
    np.save("paths.npy", np.array(y))

    observations = []
    actions = []
    rewards = []
    done = []

    for openings, path in zip(map(lambda m: m.openings, mazes), map(lambda m: m.optimal_path, mazes)):
        obs, act, r, d = to_reinforcement(openings, path)
        observations.append(obs)
        actions.append(act)
        rewards.append(r)
        done.append(d)

    observations = np.rot90(np.stack(observations), 3)
    actions = np.rot90(np.stack(actions), 3)
    rewards = np.rot90(np.stack(rewards), 3)
    done = np.rot90(np.stack(done), 3)

    np.save("observations.npy", observations)
    np.save("actions.npy", actions)
    np.save("rewards.npy", rewards)
    np.save("dones.npy", done)

    print(f"Processed {len(mazes)} mazes")

def to_reinforcement(openings: Openings, path):
    episode_length = path.size * path.size

    maze_np = openings.to_np_array(np.float32)
    pos = [0, 0]

    observations = []
    actions = []

    irrelevant = path.size * path.size - path.length
    rewards = np.array([-0.01] * (path.length - 1) + [100.0] + [0.0] * irrelevant, dtype=np.float32)
    done = np.array([0.0] * path.length + [1.0] * irrelevant, dtype=np.float32)


    for action in path.path:
        observation = np.concat((maze_np, (pos[0] / openings.size, pos[1] / openings.size)))
        actions.append(path.map[action])
        observations.append(observation)

        if action == Opening.RIGHT:
            pos[0] += 1
        elif action == Opening.LEFT:
            pos[0] -= 1
        elif action == Opening.TOP:
            pos[1] -= 1
        elif action == Opening.BOTTOM:
            pos[1] += 1

    assert pos == [openings.size - 1, openings.size - 1]


    return np.stack(observations, dtype=np.float32), np.array(actions, dtype=np.uint8), rewards, done

async def main():
    try:
        db_session = aiocouch.CouchDB("http://admin:password@127.0.0.1:5984")
        db: aiocouch.Database = await db_session["maze"]
        await process_data(db)
    finally:
        try:
            await db_session.close()
        except:
            pass

asyncio.run(main())

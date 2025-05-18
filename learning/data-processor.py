import aiocouch
import asyncio
import argparse

import numpy as np

from data.data_classes import Maze


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
    })
    results = [r.json async for r in results]

    mazes = [Maze.from_database(**res) for res in results]

    X = [maze.openings.to_np_array() for maze in mazes]
    y = [maze.optimal_path.to_np_array() for maze in mazes]

    np.save("mazes.npy", np.array(X))
    np.save("paths.npy", np.array(y))

    print(f"Processed {len(mazes)} mazes")

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

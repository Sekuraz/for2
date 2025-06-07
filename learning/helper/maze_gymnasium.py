import asyncio
from typing import Optional

import aiocouch
import numpy as np
import gymnasium as gym

from data.data_classes import Maze, Opening, Openings

class MazeEnv(gym.Env):
    _maze = None

    @property
    def maze(self) -> Maze:
        return self._maze

    @maze.setter
    def maze(self, maze: Maze):
        self._maze = maze
        self._np_openings = maze.openings.to_np_array_binary(typ=np.float32)
        self._correct_transitions = self._create_correct_transitions()

    def _create_correct_transitions(self) -> dict[tuple, Opening]:
        pos = np.array([0.0, 0.0])
        ret = {}

        for step in self._maze.optimal_path:
            ret[tuple(pos)] = step
            pos += self._opening_to_direction[step]
        return ret


    @property
    def np_openings(self) -> np.ndarray:
        return self._np_openings

    def __init__(self, maze_size=5):
        # The size of the square grid
        self._maze = None
        self._np_openings = None

        self.maze_size = maze_size
        self.steps = 0

        # Define the agent and target location; randomly chosen in `reset` and updated in `step`
        self._agent_location = np.array([0, 0], dtype=np.float32)

        # # Observations are dictionaries with the agent's and the target's location.
        # # Each location is encoded as an element of {0, ..., `size`-1}^2
        # self.observation_space = gym.spaces.Dict(
        #     {
        #         "agent": gym.spaces.Box(0, self.maze_size - 1, shape=(2,), dtype=np.uint8),
        #         "maze": gym.spaces.Box(0, int(Opening.ALL), shape=(self.maze_size**2,), dtype=np.uint8),
        #     }
        # )

        self.observation_space = gym.spaces.Box(
            low=0,
            high=1,  # maximum possible value
            shape=(2 + (2 * self.maze_size + 1) ** 2,), # binary representation
            dtype=np.float32
        )

        # We have 4 actions, corresponding to "right", "up", "left", "down"
        self.action_space = gym.spaces.Discrete(4)
        # Dictionary maps the abstract actions to the directions on the grid
        self._action_to_opening = {
            0: Opening.RIGHT,  # right
            1: Opening.LEFT,  # left
            2: Opening.TOP,  # up
            3: Opening.BOTTOM,  # down
        }

        self._opening_to_direction = {
            Opening.RIGHT: np.array([1, 0], dtype=np.float32),  # right
            Opening.LEFT: np.array([-1, 0], dtype=np.float32),  # left
            Opening.TOP: np.array([0, -1], dtype=np.float32),  # up
            Opening.BOTTOM: np.array([0, 1], dtype=np.float32),  # down
        }

        self._opening_to_action = {
            Opening.RIGHT: 0,  # right
            Opening.LEFT: 1,  # left
            Opening.TOP: 2,  # up
            Opening.BOTTOM: 3,  # down
        }

        self.target_location = np.array([self.maze_size - 1, self.maze_size - 1], dtype=np.float32)

        self.loop = asyncio.new_event_loop()
        self.dbsession = None
        self.async_generator = None
        self.loop.run_until_complete(self.get_async_iterator())


    async def get_async_iterator(self):
        db_session = aiocouch.CouchDB("http://admin:password@127.0.0.1:5984")
        db: aiocouch.Database = await db_session["maze"]
        self.async_generator = db.find({
            "$and": [
                {
                    "width": str(self.maze_size),
                },
                {
                    "height": str(self.maze_size)
                }
            ]
        })

    def _get_obs(self):
        return np.concatenate((self._agent_location / self.maze_size, self.np_openings))

    def _distance(self, agent_location=None):
        if agent_location is None:
            agent_location = self._agent_location

        return np.linalg.norm(
                self._agent_location - np.array([self.maze_size - 1, self.maze_size - 1], dtype=np.int8), ord=1
            )

    def _get_info(self):
        return {
            "distance": np.linalg.norm(
                self._agent_location - np.array([self.maze_size - 1, self.maze_size -1], dtype=np.int8), ord=1
            )
        }

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        self.last_positions = set()
        self.steps = 0


        # Choose the agent's location uniformly at random
        self._agent_location = np.array([0, 0], dtype=np.float32)

        # We will sample the target's location randomly until it does not coincide with the agent's location
        try:
            self.maze = Maze.from_database(**self.loop.run_until_complete(anext(self.async_generator)))
        except:
            raise StopIteration

        observation = self._get_obs()
        info = self._get_info()
        return observation, info

    def step(self, action):
        # Map the action (element of {0,1,2,3}) to the direction we walk in
        opening = self._action_to_opening[action]

        self.steps += 1
        if self.steps == 64:
            return self._get_obs(), -1, True, False, self._get_info()

        # ran into a wall
        if self.maze.openings[self._agent_location] & opening != opening:
            return self._get_obs(), -0.1, False, False, self._get_info()

        old_distance = self._distance()
        # We use `np.clip` to make sure we don't leave the grid bounds
        self._agent_location += self._opening_to_direction[opening]

        # An environment is completed if and only if the agent has reached the target
        terminated = np.array_equal(self._agent_location, self.target_location)
        truncated = False
        observation = self._get_obs()
        info = self._get_info()

        tuple_location = tuple(self._agent_location)

        reward = -0.001

        if tuple_location not in self._correct_transitions:
            reward -= 0.001
        if tuple_location in self.last_positions:
            reward -= 0.01
        else:
            self.last_positions.add(tuple_location)
        if terminated:
            reward = 10.0

        return observation, reward, terminated, truncated, info

    def close(self):
        self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        self.loop.run_until_complete(self.dbsession.close())
        self.loop.close()

    def get_training_data(self, batch=512):
        obs = []
        actions = []
        rewards = []
        mazes = 0
        path_sum = 0

        def load_maze():
            maze = Maze.from_database(**self.loop.run_until_complete(anext(self.async_generator)))
            maze_np = maze.openings.to_np_array_binary(typ=np.float32)
            position = np.array([0, 0], dtype=np.float32)
            path_index = 0
            nonlocal mazes, path_sum
            mazes += 1
            path_sum += maze.optimal_path.length

            return maze_np, maze.optimal_path, position, path_index


        maze_np, optimal_path, position, path_index = load_maze()

        for i in range(batch):
            if path_index == optimal_path.length + 1:
                rewards[-1] = 10.0 # finished episode, load a new one
                maze_np, optimal_path, position, path_index = load_maze()

            obs.append(np.concatenate((position / self.maze_size, maze_np)))
            step = optimal_path.path[path_index]
            actions.append(self._opening_to_action[step])
            rewards.append((-0.001))

            # ### debug
            # op = Openings(self.maze_size, np_array=maze_np, position=position / self.maze_size)
            # print(op, step, op.position)


            position += self._opening_to_direction[step]
            path_index += 1

        print(f"loaded {mazes} mazes")
        print(f"mean path length: {path_sum / mazes:.2f}")
        return np.stack(obs), np.array(actions, dtype=np.int32), np.array(rewards)




gym.register(
    id="gymnasium_env/Maze-v0",
    entry_point=MazeEnv,
)

if __name__ == "__main__":
    env = gym.make("gymnasium_env/Maze-v0")
    batch = 10
    X, y, _ = env.unwrapped.get_training_data(batch=batch)
    for i in range(batch):
        print(Openings(10, np_array=X[i][2:], position=X[i][:2] * 10))
        print(f"pos: {int(X[i][0] * 10)},{int(X[i][1] * 10)}; step:", env.unwrapped._action_to_opening[y[i]])

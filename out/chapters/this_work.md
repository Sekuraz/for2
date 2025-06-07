This works aims to prove the presented concepts in a real combination of games and \gls{rl}.
It implements a game, a server for generating the training data from the recorded games and a machine learning model which can use the training data as well as \gls{ppo} learning according to \cite{ppo}.
The chosen game for this demonstration is solving a maze, which can easily map from a game world to an environment for agent learning.


# The Game
The game is implemented as a browser game with a small backend server to record the trajectories used by the human players.
It also records the optimal paths through the maze which are used for training in this example to showcase the potential of the approach.
The implementation is inspired by \cite{game} with the addition of the backend to control the scenarios which are presented to the users and which records the user input.
This data is then stored in a CouchDB database for easy access and searchability.

The game supports arbitrary maze sizes, mazes bigger than 100 by 100 are hard to see on screen.
There is also a game mode which only reveals the maze during exploration.


For this work, mazes of size 10 by 10 and 5 by 5 cells which were completely visible to the user and the agent, were used.

# The Model
For this work, a keras and gymnasium based model was chosen. 
This approach ensures maximum reusablility of the results for future work and leverages leading machine learning environments.
The model itself consists 

# Data Preparation
To consume the data in a standardized way, a \cite{gymnasium} environment for the stored data was implemented.
It requests mazes and trajectories from the database and can present the maze as observation to the agent as well as export many mazes and trajectories as input data for pre-training.

## Model Input Format
The model is used in the pretraining

## Data encoding
During the course of this work, several data encoding techniques were tried and compared.
The first encoding used flags to represent the openings, the non existence of walls in the four directions, of each cell. 
The resulting integer was scaled to a value between 0 and 1.
This leads to a very dense but not easily interpretable representation.
The second encoding uses 0 for passable terrain and 1 for walls, which requires approximately 4 times as many input variables.\footnote{$maze.size * maze.size$ and $(2 * maze.size + 1) * (2 * maze.size + 1$ for square mazes.}
Both encodings use a flat array.
The current position was scaled to a value between 0 and 1 and then prepended to the observation.

$$
obs = np.array([pos.x / maze.size, pos.y / maze.size, *encoded_maze])
$$


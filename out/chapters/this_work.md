This works aims to prove the presented concepts in a real combination of games and \gls{rl}.
It implements a game, a server for generating the training data from the recorded games and a machine learning model 
which can use the data for pre-training as well as online training.
The chosen game for this demonstration is solving a maze, which can easily map from a game world to an environment for agent learning.


# The Game
The game is implemented as a browser game with a small backend server to record the trajectories used by the human players.
It also records the optimal paths through the maze which are used for training in this example to showcase the potential of the approach.
The implementation is inspired by \cite{game} with the addition of the backend to control the scenarios which are presented to the users and which records the user input.
This data is then stored in a CouchDB database for easy access and searchability.

The game supports arbitrary maze sizes, mazes bigger than 100 by 100 are hard to see on screen.
There is also a game mode which only reveals the maze during exploration. 
However, for this work mazes of size 10 by 10 and 5 by 5 cells which were completely visible to the user and the model were used.



# The Model
For this work, a keras \footnote{see \cite{keras}} and gymnasium \footnote{see \cite{gymnasium}} based approach was chosen. 
This approach ensures maximum reusability of the results for future work and leverages leading machine learning environments.
There is an actor-critic implementation for this work, however pre-training is only done on the actor model.
The critic could be pre-trained by freezing the actor after the initial training.

## Policy Optimization
To make this work relevant for current \gls{rl} models, \gls{ppo} as described in \cite{ppo} was chosen as the optimizer
for the online learning phase.
The reference implementation in \cite{keras-ppo} was adapted for this research question.

## Model Input Format
The pre-training step uses trajectories in accordance to the `keras.fit` api where each observation of a position in maze
in the training tensor has one corresponding action from the action space in the target data.


# Data Preparation
To consume the data in a standardized way, a gymnasium environment for the stored data was implemented.
It requests mazes and trajectories from the database and can present the maze as observation to the agent as well as 
export many mazes and trajectories as input data for pre-training.


## Data encoding
During the course of this work, several data encoding techniques were tried and compared.
All the encodings are based on numpy arrays.
The first encoding uses flags to represent the openings, the non-existence of walls in the four directions, of each cell. 
The resulting integer was scaled to a value between 0 and 1.
This leads to a very dense but not easily interpretable representation.
The second encoding uses 0 for passable terrain and 1 for walls, which requires approximately 4 times as many input 
variables.\footnote{$maze.size * maze.size$ in contrast to $(2 * maze.size + 1) * (2 * maze.size + 1)$ for square mazes.}
Both encodings use a flat array.
The current position was scaled to a value between 0 and 1 and then prepended to the observation.

\bigskip
```{#obs .python caption="Observation encoding with numpy."}
observation = np.array([pos.x / maze.size, pos.y / maze.size, *encoded_maze])
```

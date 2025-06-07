# System stability
At the time of writing HAWK is not yet a stabile system and thus performance can vary between nodes.
The new filesystem is not yet ready, so an old filesystem with sub-par connection was used.
There is also a problem when some nodes are not working properly and taken offline.
The queue system then uses nodes from other physical unit of HAWK to bring the total number of nodes to the amount
requested by the user.
This behavior leads to communication imbalances when one node is far away from the others because communication times
and delays are longer for the remote node.

# Unbalanced problem
As discussed in chapter 4, the underlying physical problem is not well-balanced.
In a normal run the workload per physical space stabilizes after some timesteps and is then re-partitioned in order to 
distribute the resulting workload evenly across all available processes.
There were tests with rebalancing after every timestep, which on one hand balanced the time spent on calculating the
next timestep, but on the other hand every rebalancing took longer than the timestep itself.
This is the reason for the long timesteps in figure \ref{fig:nodes.png}.

# Lack of personal contact
Due to the covid-19 pandemic and the stay at home orders imposed because of it, personal contact to experienced 
researchers and performance analysts was limited to video conferences and screen sharing.
This problem was of special concern since this was the author's first contact with performance analysis of a distributed
application.

# Problems building Vlasiator
The machine specific makefile for Vlasiator assumes that it has access to a private directory of one of the developers
where all dependencies are stored.
This lead to a large amount of time which was spent on replicating that setup as well as the inability to find out about
performance issues related to those dependencies because there were no instructions about their preferred build settings
and eventual custom modifications.
A complete build system including alle the dependencies for Vlasiator would have helped a lot with those concerns.
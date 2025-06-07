# Node level performance
The first and most important thing here is, that the provided test case only contains 4 time steps, which take 
approximately 30 seconds out of a 3-minute run.
All the remaining runtime ist spent initializing and terminating the whole system, which includes writing a restart
file of several hundred gigabytes.
Another thing to note is, that all the small functions which are called repeatedly were left out of the analysis due to
memory constraints.
Tracing them would have blown up the trace file, and the preliminary analysis showed that they hardly take any time.
So it was suspected that they already were heavily optimized.

\image{processes.png}{Timesteps per second with different numbers of processes per node.}
The code performed best with 128 processes per node and 2 threads per process as seen in 
figure \ref{fig:processes.png}.
This is unexpected, because MPI communication within one CCX (4 pyhsical, 8 logical cores) of the AMD Rome CPUs in HAWK
is expected to take longer than OpenMP communication. 
The AMD-recommended and generally faster setup would be 32 processes with 8 threads or 32 processes with 4 threads if
hyperthreading is disabled.
In the end those results lead to two conclusions.
Firstly, some parts of a timestep is not yet distributed across all available threads of one process but rather handled
sequentially, and this part takes longer than the communication overhead incurred by using MPI.
Secondly, the timestep itself is not optimised to use all available resources of an AMD Rome core, otherwise hyperthreading
wouldn't net any performance benefit.

# System level performance
\image{nodes.png}{Seconds per timestep for different numbers of nodes.}
There are two interesting things in figure \ref{fig:nodes.png}, first and foremost the problem doesn't scale well above
32 nodes, so for further analysis 32 nodes are used because that number seems to be a sweet spot for the problem.
The other thing is, that for this experiment one timestep takes approximately 3 times as long as before.
The latter problem will be adressed later on.

In depth analysis using vampir unearthed some more interesting findings, the first one being, that the simulation is not
balanced at all. 
This means that timesteps take much longer on some processes than on others.
After that problem was brought to the attention of the programmers the issue was identified as a physics problem and, from
their experience, would take a few hundred timesteps and some rebalancing to even out.
As a result of this problem, even in the best runs up to 30% of the time spent within a timestep was used on MPI waits and 
barriers as seen in figure \ref{fig:1timestep.png}.
The second issue which can be clearly seen in the vampir output is, that the problem is indeed hardly parallel within a
timestep.

Another problem with scaling tests is, that the balancing library which is used for rebalancing assumes that all
available MPI slots are used.
This leads to an out-of-bounds error when running Vlasiator with a different numbers of MPI processes in one job.
Apparently the library is querying the queue system for information about the current job and ignoring MPI information.
These scaling tests were thus done in separate jobs that may have variable performance due to running in different
partitions of the machine.
Jobs with a multiple of 64 nodes are placed in the hypercube of 4096, others are placed in an attached partition of
1500 nodes which is not a hypercube.
\image{1timestep.png}{Work done during one timestep as shown in vampir.}{Red bars are used to mark waiting time.}

In order to gather performance metrics of Vlasiator the execution of the code has to be traced and performance data has
to be gathered.
For this project score-p, cube, scalasca and vampir were used as described in chapter \ref{targets}.
Those programs and their capabilities are discussed in this chapter and thus it can be skipped if the reader is familiar
with them.

# Score-P
Score-P is a compiler wrapper and infrastructure for profiling and tracing \gls{hpc} applications.
It can be used for sequential, thread-parallel (e.g. OpenMP), multi-process (e.g. MPI) and accelerated (e.g. CUDA) code
as well as hybrids of all of the different models.
During runtime of a program compiled with Score-P, trace files are written.
The collection of this data obviously consumes runtime and memory which has to be taken into account when measuring
runtimes and looking for optimisations in the codebase.

# Scalasca
Scalasca is a tool to analyse communication patterns and wait times in the trace files written by Score-P.
It can also be used to determine the sources and destinations of communication within the program which helps identifying
flawed communication patterns.

# Cube
Cube is a visualisation software for Score-P traces and Scalasca analyses.
It is used to make all the data and insight within the gigabytes or even terabytes of data collected by Score-P and 
processed by Scalasca visible to the human eye.
Most prominently it can show which function was called how many times and how much time was spent within them as well 
as how much time was spent waiting for other processes to advance.

# Vampir
Vampir shows essentially the same data as Cube but with a per thread view.
This helps pinpointing the exact locations of imbalances in the code and not only show the total elapsed time as in 
Cube.

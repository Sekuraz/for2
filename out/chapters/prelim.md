# Workload Distribution
In order to properly analyse the performance of the code, first the best running configuration had to be found.
First, the number of nodes was kept constant at 32, and the distribution of the 8192 possible threads was varied.
The result of all those runs was, that 128 processes per node and 2 threads per process performed best.
This is a very uncommon result on the machine, so this would warrant further examination.

Secondly strong scaling aspect of the given test case was examined.
In total runtime 32 nodes proved best, using 64 did not only not provide any decrease in runtime, it even increased 
overall runtime and was thus excluded from further study.
Using fewer nodes was more efficient but also took more time as can be seen in figure \ref{fig:nodes.png}.

The last thing to check was, whether hyperthreading benefits the performance of the code, and it was found that this was
the case.
So hyperthreading was turned on for all subsequent runs of Vlasiator.

# Preparing Trace Data
The first runs with ScoreP enabled returned the result that for a full trace approximately 83 Terabytes of memory would
be needed to store those traces.
So the first task was to narrow down the amount of traces collected and thus the functions which were the shortest and 
called most often were added to a filter list and thus discounted from the traces\footnote{For example functions to 
access elements by an index or retrieve data in another format or trivial calculations from those data.}.
When this preliminary work was finished, the trace data was reduced to around 1 TB which is small enough to fit in the
main memory of one of the large postprocessing nodes.
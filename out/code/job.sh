#!/bin/bash
#PBS -N EGI
#PBS -l select=32:mpiprocs=128:ompthreads=2
#PBS -l walltime=0:25:00
#PBS -m be
#PBS -q test
#PBS -M markusb@selfnet.de
#PBS -W umask=007

set -xe
export SCOREP_FILTERING_FILE="./scorep.filt"

mkdir -p ${HOME}/pbs_nodefiles
cp ${PBS_NODEFILE} ${HOME}/pbs_nodefiles/

ulimit -c unlimited
umask 007

export SCOREP_ENABLE_TRACING=1
export SCOREP_TOTAL_MEMORY=100000000

#export PHIPROF_PRINTS=detailed
export MPI_LAUNCH_TIMEOUT=60

LIBRARY_PREFIX="$WS/../vlasiator/dependencies"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$LIBRARY_PREFIX/jemalloc/lib
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/hlrs/spack/rev-003_2020-03-03/papi/5.7.0-gcc-9.2.0-ie2ujpf4/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$LIBRARY_PREFIX/phiprof/lib

#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/hlrs/spack/rev-004_2020-06-17/trilinos/12.14.1-gcc-9.2.0-jp6yigfc/lib

module load gcc mpt papi boost scorep

echo $LD_LIBRARY_PATH

#threads per process
t=2
ht=2

export OMP_NUM_THREADS=$t

export MPI_NUM_MEMORY_REGIONS=0

#nodes=$( qstat -f $PBS_JOBID | grep   Resource_List.nodes | gawk '{print $3}' )
#cores_per_node=128
#total_units=$(echo $nodes $cores_per_node $ht | gawk '{print $1*$2*$3}')
#units_per_node=$(echo $cores_per_node $ht | gawk '{print $1*$2}')
#tasks=$(echo $total_units $t  | gawk '{print $1/$2}')
#tasks_per_node=$(echo $units_per_node $t  | gawk '{print $1/$2}')

mpiprocs=$(qstat -f $PBS_JOBID | grep   Resource_List.mpiprocs | gawk '{print $3}' )
threads_per_proc=$( qstat -f $PBS_JOBID | grep   Resource_List.select | cut -d "="  -f 4 )


# Change to the directory that the job was submitted from
cd $PBS_O_WORKDIR
rm -f restart*

#openmpi
#export OMP_PROC_BIND=close
#export OMP_PLACES=cores
#mpirun -np $tasks --bind-to core --map-by L3cache -N $tasks_per_node ../vlasiator/vlasiator --run_config=Magnetosphere.cfg #--restart.filename $( ls restart.*.vlsv | tail -n 1 )
#mpt
mpirun -np $mpiprocs omplace -nt $threads_per_proc -c 0,128,1,129,2,130,3,131,4,132,5,133,6,134,7,135,8,136,9,137,10,138,11,139,12,140,13,141,14,142,15,143,16,144,17,145,18,146,19,147,20,148,21,149,22,150,23,151,24,152,25,153,26,154,27,155,28,156,29,157,30,158,31,159,32,160,33,161,34,162,35,163,36,164,37,165,38,166,39,167,40,168,41,169,42,170,43,171,44,172,45,173,46,174,47,175,48,176,49,177,50,178,51,179,52,180,53,181,54,182,55,183,56,184,57,185,58,186,59,187,60,188,61,189,62,190,63,191,64,192,65,193,66,194,67,195,68,196,69,197,70,198,71,199,72,200,73,201,74,202,75,203,76,204,77,205,78,206,79,207,80,208,81,209,82,210,83,211,84,212,85,213,86,214,87,215,88,216,89,217,90,218,91,219,92,220,93,221,94,222,95,223,96,224,97,225,98,226,99,227,100,228,101,229,102,230,103,231,104,232,105,233,106,234,107,235,108,236,109,237,110,238,111,239,112,240,113,241,114,242,115,243,116,244,117,245,118,246,119,247,120,248,121,249,122,250,123,251,124,252,125,253,126,254,127,255 ../vlasiator/vlasiator --run_config=Magnetosphere.cfg

mv logfile.txt logfile.$PBS_JOBID.txt

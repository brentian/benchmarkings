if [ "$#" -ne 5 ]; then
  echo "Script for running Crossover for ABIP via COPT in batch mode..."
  echo "Usage: <dataset directory> <subset name> <time limit for each instance> <precision to use> <direct:1 / indirect:0>" 1>&2
  echo "Example: zsh run_all_crs_abip.sh data/netlib grb_presolved 100 6 1 &"
  exit -1
fi

# test set
set=$1
prefix=$2
timelimit=$3
precision=$4
method=$5
result=$set/abip_${method}_1e-$precision
cross=$set/crs.abip_${method}_1e-$precision

# crossover
crs_script=crossover_by_copt.py

mkdir -p $cross

logfile=$set/crs.abip_1e-$precision.log
if [ -f $logfile ]; then
  rm $logfile
fi

# no need to run scs at 1e-8
for f in $(/bin/ls $set/$prefix); do

  ff=$(basename -s .mps.gz $f)
  echo $ff >>$logfile
  primal=$result/${f}.primal.txt
  dual=$result/${f}.dual.txt
  cmd="timeout $timelimit python $crs_script $set/$prefix/$f $primal $dual $cross &>>$logfile"
  echo $cmd &>>$logfile
  eval $cmd
done

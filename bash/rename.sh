#!/bin/bash

# arguments
indir=""
outdir=""
prj=""

if [ $# -ne 3 ]
then
  echo "Usage: "$0" input_dir output_dir prj_name"
  exit -1;
else
  indir=$1
  outdir=$2
  prj=$3
fi

if [[ -z "$indir" || -z "$outdir" || -z "$prj" ]]
then
  echo "Error: wrong arguments"
fi

if [ ${indir:(-1):1} != "/" ]
then
  indir=$indir"/"
fi

if [ ${outdir:(-1):1} != "/" ]
then
  outdir=$outdir"/"
fi

suffix="wav"
find $indir -name "*.$suffix" | sort | awk '{
printf(cp "$0" "$outdir$num.$suffix");
}' > re.sh
cmd=`printf ""`
$cmd

chmod u+x re.sh
./re.sh


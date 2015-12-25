#!/bin/bash

REC=dianwang02.txt
OUT=ppl_statis.txt
LM=/home/wangjie/project/poc_select/lm/lm.arpa.gbk.picc
ORDER=3
DELTMP=0


declare -a st0
declare -a st1
declare -a st2
declare -a st3
declare -a st4
declare -a st5

function cal_st {
	local max=0

	if [ $1 -le 100 ]
	then
		max=${#st0[@]}
		st0[$max]=$2
	elif [ $1 -le 200 ]
	then
		max=${#st1[@]}
		st1[$max]=$2
	elif [ $1 -le 300 ]
	then
		max=${#st2[@]}
		st2[$max]=$2
	elif [ $1 -le 400 ]
	then
		max=${#st3[@]}
		st3[$max]=$2
	elif [ $1 -le 500 ]
	then
		max=${#st4[@]}
		st4[$max]=$2
	else
		max=${#st5[@]}
		st5[$max]=$2
	fi
}

function print_st {
	local num=0
	local rate=0.0
	local text="----PPL Statistics Result----"
	echo $text > $OUT

	num=${#st0[@]}
	rate=`echo "scale=2; 100 * $num / $file_num" | bc`
	text="ppl <= 100:	count="$num",	rate="$rate"%"
	echo $text >> $OUT

	num=${#st1[@]}
	rate=`echo "scale=2; 100 * $num / $file_num" | bc`
	text="ppl <= 200:	count="$num",	rate="$rate"%"
	echo $text >> $OUT

	num=${#st2[@]}
	rate=`echo "scale=2; 100 * $num / $file_num" | bc`
	text="ppl <= 300:	count="$num",	rate="$rate"%"
	echo $text >> $OUT

	num=${#st3[@]}
	rate=`echo "scale=2; 100 * $num / $file_num" | bc`
	text="ppl <= 400:	count="$num",	rate="$rate"%"
	echo $text >> $OUT

	num=${#st4[@]}
	rate=`echo "scale=2; 100 * $num / $file_num" | bc`
	text="ppl <= 500:	count="$num",	rate="$rate"%"
	echo $text >> $OUT

	num=${#st5[@]}
	rate=`echo "scale=2; 100 * $num / $file_num" | bc`
	text="ppl >  500:	count="$num",	rate="$rate"%"
	echo $text >> $OUT

	echo "" >> $OUT
	text="----File Distribution----"
	echo $text >> $OUT
	
	text="ppl <= 100:"
	echo $text >> $OUT
	for f in ${st0[@]};do
		echo "	"$f >> $OUT
	done

	text="ppl <= 200:"
	echo $text >> $OUT
	for f in ${st1[@]};do
		echo "	"$f >> $OUT
	done

	text="ppl <= 300:"
	echo $text >> $OUT
	for f in ${st2[@]};do
		echo "	"$f >> $OUT
	done

	text="ppl <= 400:"
	echo $text >> $OUT
	for f in ${st3[@]};do
		echo "	"$f >> $OUT
	done

	text="ppl <= 500:"
	echo $text >> $OUT
	for f in ${st4[@]};do
		echo "	"$f >> $OUT
	done

	text="ppl > 500:"
	echo $text >> $OUT
	for f in ${st5[@]};do
		echo "	"$f >> $OUT
	done
}

# make tmp dir
if [ ! -d "tmp" ]
then
	mkdir tmp
fi

# awk to split text
awk -F '\t' 'BEGIN{
	file = "";
	filelist = "tmp/txt.list";
}
{
	lf = $1;
	arr_num = split(lf, arr, "/");
	lf = arr[arr_num];
	gsub(/\.wav/, "", lf);

	lt = $2;
	gsub(/.*?:/, "", lt);
	gsub(/\(.*?\)/, " ", lt);

	if (file == lf)
	{
		print lt >> "tmp/"file".txt";
	}
	else
	{
		file = lf;
		print file >> filelist;
		print lt > "tmp/"file".txt";
	}
}
END{
	;
}' $REC

# compute ppl by ngram
file_num=`wc -l tmp/txt.list`
file_num=${file_num% *}

while read LINE
do
	ngram -order $ORDER -lm $LM -ppl tmp/$LINE.txt -debug 2 > tmp/$LINE.ppl

	ppl_str=`tail -n 1 tmp/$LINE.ppl`
	ppl_str=${ppl_str#*ppl= }
	ppl_str=${ppl_str% ppl1*}
	ppl_str=${ppl_str%.*}

	ppl_val=$[ $ppl_str + 0 ]

	cal_st $ppl_val $LINE
done < tmp/txt.list

# print statis result
print_st

# delete tmp files
if [ $DELTMP -gt 0 ]
then
	rm -rfv tmp
fi


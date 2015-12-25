#!/bin/bash

REC=dianwang02.txt
OUT1=ppl_out1.txt
OUT2=ppl_out2.txt
SRC=""
DST=""
LM=/home/wangjie/project/poc_select/lm/lm.arpa.gbk.other
ORDER=3
DELTMP=0

:<<!EOF!
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
!EOF!

# compute ppl by ngram
file_num=`wc -l tmp/txt.list`
file_num=${file_num% *}

while read LINE
do
	#ngram -order $ORDER -lm $LM -ppl tmp/$LINE.txt -debug 2 > tmp/$LINE.ppl

	ppl_str=`tail -n 1 tmp/$LINE.ppl`
	ppl_str=${ppl_str#*ppl= }
	ppl_str=${ppl_str% ppl1*}
	ppl_str=${ppl_str%.*}

	echo $ppl_str" "$LINE >> $OUT1

done < tmp/txt.list

sort -n -k 1 -t ' ' $OUT1 -o $OUT2
head -n 100 $OUT2 > $OUT1
awk '{print $2}' $OUT1 > $OUT2

#while read LINE
#do
	#cp $LINE $LINE
#done < $OUT2

#rm $OUT1 #$OUT2

# delete tmp files
if [ $DELTMP -gt 0 ]
then
	rm -rfv tmp
fi


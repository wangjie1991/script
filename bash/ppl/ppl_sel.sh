#!/bin/bash

REC=dianwang02.txt
LM=/home/wangjie/project/poc_select/lm/lm.arpa.gbk.other
SEL_SRC=/home/wangjie/project/poc_select/AM/dianwang/
SEL_DST=/home/wangjie/project/poc_select/AM/setselect/
ORDER=3
DELTMP=0


# make tmp dir
if [ ! -d "tmp" ]
then
	mkdir tmp
fi

#:<<!EOF!
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
#!EOF!

# compute ppl by ngram
while read LINE
do
	#ngram -order $ORDER -lm $LM -ppl tmp/$LINE.txt -debug 2 > tmp/$LINE.ppl

	ppl_str=`tail -n 1 tmp/$LINE.ppl`
	ppl_str=${ppl_str#*ppl= }
	ppl_str=${ppl_str% ppl1*}
	ppl_str=${ppl_str%.*}

	echo $ppl_str" "$LINE".wav" >> tmp/ppl_all.txt

done < tmp/txt.list

sort -n -k 1 -t ' ' tmp/ppl_all.txt -o tmp/ppl_all.txt
awk '{print $2}' tmp/ppl_all.txt > tmp/ppl_file.txt
head -n 100 tmp/ppl_file.txt > tmp/ppl_sel.txt

while read LINE
do
	cp ${SEL_SRC}${LINE} ${SEL_DST}${LINE}
done < tmp/ppl_sel.txt

# delete tmp files
if [ $DELTMP -gt 0 ]
then
	rm -rf tmp
fi


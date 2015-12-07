##!/bin/bash

depth=3

dst=$1
#dst="/home/jay/Desktop/"

dir=""
path=""
file=""

# cat file
find -name "*.txt" | sort > list

while read line
do
    dir=$dst"utf8/"

    for (( i=2; i<depth; i++ ))
    do
        split=`echo $line | cut -d "/" -f$i`
        dir=$dir$split"/"
    done

    if [ ! -d $dir ]
    then
        mkdir -p $dir
    fi

    split=`echo $line | cut -d "/" -f$depth`
    path=$dir$split".utf8"

    if [[ $file != $path ]]
    then
        file=$path
    fi

    cat $line >> $file

done < list

# iconv gbk
find $dst"utf8/" -name "*.utf8" | sort > list_utf8

while read line
do
    file=${line##*utf8/}
    file=${file%.utf8}
    file=$dst"gbk/"$file".gbk"
    dir=${file%/*}

    if [ ! -d $dir ]
    then
        mkdir -p $dir
    fi

    iconv -c -f utf8 -t gbk $line > $file
    #rm $line
done < list_utf8

rm list_utf8



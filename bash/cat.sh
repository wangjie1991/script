#!/bin/bash
find -name *.txt | sort > list

#depth=2
newpath=""
oldpath=""

while read line
do
    newpath="."
    for ((i=2;i<=2;i++))
    do
        split=`echo $line | cut -d "/" -f$i`
        newpath=$newpath"/"$split
    done
    #echo "oldpath = "$oldpath
    #echo "newpath = "$newpath

    if [[ $oldpath = $newpath ]]
    then
        cat $line >> $newpath".txt"
    else
        if [[ $oldpath != "" ]]
        then
            iconv -c -f utf8 -t gbk $oldpath".txt" > $oldpath".gbk" 
        fi
        oldpath=$newpath
    fi
done < list




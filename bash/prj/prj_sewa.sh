:<<EOF
project_dir
    /lm
    /rs
    /tg
        /select
            /utf16
            /utf8
        /random
            /utf16
            /utf8
        /ts
            /utf16
            /utf8
    /tl
        cutWaveSeg
        ParseInfoFromTextGrid.py
        WordSplit
        lexicon.gbk
        /HandleOriginalCorpus
    /tr
        /select
        /random
        /ts
    /wc
    /wt

tl tr
EOF


prj=/home/wangjie/project/zhonghang

# mkdir
dirs=(rs tg/select/utf16 tg/select/utf8 tg/random/utf16 tg/random/utf8 tg/ts/utf16 tg/ts/utf8 wc)
for dir in ${dirs[@]}
do
    if [ ! -d $dir ]
    then
        mkdir -p $dir
    fi
done


# corpus
dts=(select random ts)
for dt in ${dts[@]}
do
    cp tr/$dt/*.TextGrid tg/$dt/utf16/

    # iconv textgrid utf16 to utf8
    cd tg/$dt/
    ls utf16/ > utf16.list
    while read line
    do
        iconv -c -f utf16 -t utf8 utf16/$line -o utf8/$line
    done < utf16.list
    cd ../../

    # handle textgrid to text
    cd tg/$dt/
    find $prj/tg/$dt/utf8/ -name "*.TextGrid" > utf8.list
    python $prj/tl/ParseInfoFromTextGrid.py utf8.list cutwave.list textgrid.txt
    awk '{print $2}' textgrid.txt | iconv -c -f utf8 -t gbk > corpus.gbk
    cd ../../

    # handle textgrid to text
    cd tl/HandleOriginalCorpus/
    ./HandleOriginalCorpus.sh $prj/tg/$dt/corpus.gbk $prj/tg/$dt/corpus.low 
    cd ../../
    #cp tg/$dt/corpus.low lm/$dt.low
done


# ref
cd rs/
cp $prj/tg/ts/textgrid.txt ./
sed "s;^;$prj/wc/;g" textgrid.txt | awk '{print $1"\t"$2}' | iconv -c -f utf8 -t gbk -o ref.txt
rm textgrid.txt
cd ../


# cutwave
#cp tr/ts/*.wav wt/
cp tg/ts/cutwave.list wc/
sed -i "s;XXX/;$prj/wt/;g" wc/cutwave.list
tl/cutWaveSeg wc/cutwave.list 8000 wc 0



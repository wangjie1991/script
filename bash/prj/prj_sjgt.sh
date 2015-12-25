:<<EOF
project_dir
    /lm
    /rs
    /tg
        /core
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
        /core
        /ts
    /wc
    /wt

tl tr
EOF


prj=/home/wangjie/project/shijigaotong


:<<eof
# corpus
dts=(beijing shenyang shanghai shenzhen)
for dt in ${dts[@]}
do
	dt=ts/$dt

    if [ ! -d tg/$dt/utf16/ ]
    then
        mkdir -p tg/$dt/utf16/
    fi

    if [ ! -d tg/$dt/utf8/ ]
    then
        mkdir -p tg/$dt/utf8/
    fi

    cp tr/$dt/*.TextGrid tg/$dt/utf16/

    # iconv textgrid utf16 to utf8
    cd tg/$dt/
    ls utf16/ > utf16.list
    while read line
    do
        iconv -c -f utf16 -t utf8 utf16/$line -o utf8/$line
    done < utf16.list
    cd ../../../

    # handle textgrid to text
    cd tg/$dt/
    find $prj/tg/$dt/utf8/ -name "*.TextGrid" > utf8.list
    python $prj/tl/shijigaotongTextGrid.py utf8.list cutwave.list textgrid.txt
    awk '{print $2}' textgrid.txt | iconv -c -f utf8 -t gbk > corpus.gbk
    cd ../../../

    # handle textgrid to text
    cd tl/HandleOriginalCorpus/
    ./HandleOriginalCorpus.sh $prj/tg/$dt/corpus.gbk $prj/tg/$dt/corpus.low 
    cd ../../
    #cp tg/$dt/corpus.low lm/$dt.low
done
eof

# ref
dts=(beijing shenyang shanghai shenzhen)
for dt in ${dts[@]}
do
:<<eof
cd rs/$dt
cp $prj/tg/ts/$dt/textgrid.txt ./
ex - textgrid.txt << end-of-script
%s;^;$prj/wc/$dt/;g
wq
end-of-script
awk '{print $1"\t"$2}' textgrid.txt | iconv -c -f utf8 -t gbk -o ref.txt
rm textgrid.txt
cd ../../
eof

cp tg/ts/$dt/cutwave.list wc/$dt/
ex - wc/$dt/cutwave.list << end-of-script
%s;XXX/;$prj/wt/$dt/;g
wq
end-of-script
tl/cutWaveSeg wc/$dt/cutwave.list 8000 wc/$dt 0

done

# cutwave
#cp tr/ts/*.wav wt/



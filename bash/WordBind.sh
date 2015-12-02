
if [ $# -ne 2 ]
then
  echo "Usage:"$0" unigram_file dict_file"
  exit -1;
fi

awk -F '\t' '{
  if (NF == 2)
  {
    c = substr($2, 1, 1)
    if (c != "<")
    {
      print $2"\t"$1
    }
  }
}' $1 > unigram.dic

./WordBind unigram.dic $2
rm unigram.dic


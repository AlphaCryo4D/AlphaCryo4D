#!/bin/bash
th=2

for f in ./u*b*c*.star;do

f2=`basename $f ".star"`
cp head.star ${f2}_post_and.star

while read line;do
p=`echo ${line}|awk '{if(NF>5) print $10}'`
echo $p
n=`grep $p u*b*c*.star|wc -l`
#echo $n
if [ $n -ge $th ];then
echo ${line} >> ${f2}_post_and.star
#echo ${line}
fi
done < $f

done

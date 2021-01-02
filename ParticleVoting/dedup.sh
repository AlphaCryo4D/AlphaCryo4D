#!/bin/bash

x=`ls *.star`

nproc=28
Pfifo="./tmp.fifo"
mkfifo $Pfifo
exec 6<>$Pfifo
rm -f $Pfifo
for((i=1; i<=$nproc; i++));do
echo
done >&6

wc -l $x | sort -nr -k1 |while read line;do
f=`echo ${line}|awk '{print $2}'`
if [ -f "$f" ];then
f2=`basename $f ".star"`
echo $f2
ptcl=`grep '_rlnImageName' $f | awk '{print substr($2,2)}'`

while read line;do
read -u6
{
{
p=`echo ${line} | awk '{if(NF>5) print $'${ptcl}'}'`
n=`grep " $p " $x|wc -l`
if [[ -n $p && $n -eq 1 ]];then
#echo $n,$p
#sed -i 's#'${line}'#EEEXXX#g;/EEEXXX/d' $f
echo ${line} >> ${f2}.tmp
fi
}
sleep 1
echo >&6
} &
done < $f
wait

cat head.star ${f2}.tmp > ${f2}_dedup.star
rm ${f2}.tmp
fi
done
exec 6>&-

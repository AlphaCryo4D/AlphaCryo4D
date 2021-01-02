#!/bin/bash

th=2

ptcl=`grep '_rlnImageName' head.star | awk '{print substr($2,2)}'`

nproc=28
Pfifo="./tmp.fifo"
mkfifo $Pfifo
exec 6<>$Pfifo
rm -f $Pfifo
for((i=1; i<=$nproc; i++));do
echo
done >&6


for f in ./u*b*c*.star;do

while read line;do
read -u6
{
{
p=`echo ${line}|awk '{if(NF>5) print $'${ptcl}'}'`
n=`grep " $p " u*b*c*.star|wc -l`
#echo $n
if [[ -n $p && $n -ge $th ]];then
echo $n,$p
echo ${line} >> post_and.tmp
#echo ${line}
fi
}
sleep 1
echo >&6
} &
done < $f
wait

done

exec 6>&-
cp head.star post_and.star
sort -k $ptcl,$ptcl -u post_and.tmp >> post_and.star
rm post_and.tmp

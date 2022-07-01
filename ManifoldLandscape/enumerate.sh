#!/bin/bash

datafile='data.log'
numberfile='num.txt'

while read line;do
u=`echo $line | awk -v head="u" -v tail="_b" '{print substr($0, index($0,head)+length(head),index($0,tail)-index($0,head)-length(head))}'`
b=`echo $line | awk -v head="b" -v tail="_c" '{print substr($0, index($0,head)+length(head),index($0,tail)-index($0,head)-length(head))}'`
c=`echo $line | awk -v head="c" -v tail="_a" '{print substr($0, index($0,head)+length(head),index($0,tail)-index($0,head)-length(head))}'`

l=$[`grep mrcs stars/u${u}_b${b}_c${c}.star | wc -l`]
echo $l >> $numberfile
done < $datafile

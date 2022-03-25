#!/bin/bash

datafile='data.log'
numberfile='num.txt'

while read -r line;do
u=`echo $line | awk -v head="u" -v tail="_b" '{print substr($0, index($0,head)+length(head),index($0,tail)-index($0,head)-length(head))}'`
b=`echo $line | awk -v head="_b" -v tail="_c" '{print substr($0, index($0,head)+length(head),index($0,tail)-index($0,head)-length(head))}'`
#c=`echo $line | awk -v head="c" -v tail="_a" '{print substr($0, index($0,head)+length(head),index($0,tail)-index($0,head)-length(head))}'`
c=`echo $line | awk -v head="_c" -v tail=".m" '{print substr($0, index($0,head)+length(head),index($0,tail)-index($0,head)-length(head))}'`

#l=$[`awk '{if(NF>3) print $0}' stars/u${u}_b${b}_c${c}.star | wc -l`]
l=$[`grep mrcs stars/u${u}_b${b}_c${c}.star | wc -l`]
echo $l >> $numberfile
done < $datafile

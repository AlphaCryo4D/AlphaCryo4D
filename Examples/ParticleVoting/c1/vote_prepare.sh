#!/bin/bash

datafile='../../Resample/data.log'

while read line;do

#sed -n "${line}p" $datafile
n=`echo ${line}|awk '{print $1}'`

u=`sed -n "${n}p" $datafile | awk -v head="u" -v tail="_b" '{print substr($0, index($0,head)+length(head),index($0,tail)-index($0,head)-length(head))}'`
b=`sed -n "${n}p" $datafile | awk -v head="b" -v tail="_c" '{print substr($0, index($0,head)+length(head),index($0,tail)-index($0,head)-length(head))}'`
c=`sed -n "${n}p" $datafile | awk -v head="c" -v tail="_a" '{print substr($0, index($0,head)+length(head),index($0,tail)-index($0,head)-length(head))}'`

ln -s ../../Resample/stars/u${u}_b${b}_c${c}.star .

done < $1

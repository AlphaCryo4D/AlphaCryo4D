#!/bin/bash

mkdir maps
mkdir stars

#set as you need
ur=`eval echo {234,134,124,123}`
br=30
cr=10

for u in $ur;do
for b in `seq 1 $br`;do
for c in `seq 1 $cr`;do
ln -s your_path/batch${b}/union${u}/run_it030_class0$(printf '%02d' $c).mrc maps/u${u}_b${b}_c${c}.mrc
#echo $u
#echo $b
#echo $c
ln -s your_path/batch${b}/union${u}/run_it030_data_class${c}.star stars/u${u}_b${b}_c${c}.star   #starfile should be split into different 3D classes
done
done
done


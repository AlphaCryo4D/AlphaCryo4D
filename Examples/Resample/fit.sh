#!/bin/bash
mkdir -p maps_aligned

for f in maps/*mrc;do

f2=`basename $f .mrc`
#echo $f2

if [ ! -f "${f2}_aligned.mrc" ];then
e2proc3d.py $f maps_aligned/${f2}_aligned.mrc --alignref maps/refs/ref.mrc --align rotate_translate_3d_tree -v 2
echo $f2
fi

done

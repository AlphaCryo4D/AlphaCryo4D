#!/bin/bash

mkdir -p maps
mkdir -p maps_bf
for i in {1..20}
do

e2pdb2mrc.py -R 1.68 -A 0.84 -B 200 --center States/Conformer${i}.pdb maps/C${i}.mrc

sed -i "s/Conformer/C${i}/g" bfactor.com

./bfactor.com

sed -i "s/C${i}/Conformer/g" bfactor.com

done

#!/bin/bash
module load relion/4.0-cpu-intel-2018.1
mkdir maps
mkdir stars

#set as you need
#ur=`eval echo {234,134,124,123}`
br=2
cr=8

#for u in $ur;do
for b in `seq 1 $br`;do
#	for ur in batch${b}/union*[0-9]; do
        for urstar in batch${b}/union*.star; do
                ur=${urstar%%.star}
                u=${ur##*union}
		for c in `seq 1 $cr`;do
			relion_star_handler --i $ur/run01_it080_data.star --select rlnClassNumber --minval $c --maxval $c --o ${ur}/run01_it080_data_class${c}.star
			#relion-3.1-beta
			#relion_star_handler --i $ur/run01_it080_data.star --select rlnClassNumber --minval $((c-1)) --maxval $((c+1)) --o ${ur}/run01_it080_data_class${c}.star
			
			num=`grep mrcs $PWD/$ur/run01_it080_data_class${c}.star |wc -l`
			if [[ $num != 0 ]]; then
				ln -s $PWD/$ur/run01_it080_data_class${c}.star stars/u${u}_b${b}_c${c}.star   #starfile should be split into different 3D classes
				ln -s $PWD/$ur/run01_it080_class0$(printf '%02d' $c).mrc maps/u${u}_b${b}_c${c}.mrc
			fi
		done
	done
done


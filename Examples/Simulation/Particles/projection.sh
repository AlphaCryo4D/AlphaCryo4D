#!/bin/bash
#relion/3.0-beta-cpu-intel-2018.0

# snr = 0.01
mkdir -p SNR001
for i in {1..20}
do

relion_project --i ../maps_bf/C${i}_bf100.mrc --o SNR001/C${i} --ctf --angpix 0.84 --ang params_C${i}.star --add_noise --white_noise 10

done

# snr=0.05
mkdir -p SNR005
for i in {1..20}
do

relion_project --i ../maps_bf/C${i}_bf100.mrc --o SNR005/C${i} --ctf --angpix 0.84 --ang params_C${i}.star --add_noise --white_noise 4.47

done

# snr=0.005
mkdir -p SNR0005
for i in {1..20}
do

relion_project --i ../maps_bf/C${i}_bf100.mrc --o SNR0005/C${i} --ctf --angpix 0.84 --ang params_C${i}.star --add_noise --white_noise 14.14

done


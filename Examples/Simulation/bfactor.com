#!/bin/csh
#
./bfactor.exe << eof
M
maps/Conformer.mrc
maps_bf/Conformer_bf100.mrc
0.84		!Pixel size
3.36,1.68 	!Resolution range to fut B-factor (low, high)
100.0		!B-factor to be applied
2		!Low-pass filter option (1=Gaussian, 2=Cosine edge)
3.36		!Filter radius
5		!Width of cosine edge (if cosine edge used)
eof
#

AlphaCryo4D v0.1.0-lite Development Version

Simplified version of AlphaCryo4D

==================================================

AlphaCryo4D is an open-source free software released under GNU General Public LICENSE that implements 3D classification of single-particle cryo-EM data using deep manifold learning and novel energy-based particle voting methods (originally proposed in the following bioRxiv preprint by the Mao laboratory). AlphaCryo4D v0.1.0c is currently a development version, NOT a stable released version. The authors are currently optimizing the code architecture and adding novel features to the system. The future version of this open-source software will be updated with a user-friendly interface. Users are free to use and modify the source code, providing their compliance with the GPL and that any publication making use of this software shall cite the following reference or its formally published form:

Reference:

Zhaolong Wu, Enbo Chen, Shuwen Zhang, Yinping Ma, Congcong Liu, Chang-Cheng Yin, Youdong Mao. Visualizing conformational space of functional biomolecular complexes by deep manifold learning. bioRxiv preprint doi: https://doi.org/10.1101/2021.08.09.455739.

References of potentially used software:

EMAN2:
Tang, G., Peng, L., Baldwin, P. R., Mann, D. S., Jiang, W., Rees, I., & Ludtke, S. J. (2007). EMAN2: an extensible image processing suite for electron microscopy. J Struct Biol, 157(1), 38-46. doi:10.1016/j.jsb.2006.05.009

RELION:
Scheres, S. H. (2012). RELION: implementation of a Bayesian approach to cryo-EM structure determination. J Struct Biol, 180(3), 519-530. doi:10.1016/j.jsb.2012.09.006

==================================================

Installation:

It is recommended to install EMAN2 and RELION before using AlphaCryo4D according to the websites https://github.com/cryoem/eman2 and https://github.com/3dem/relion respectively.

1.  Download the source code: 

git clone https://github.com/AlphaCryo4D/AlphaCryo4D.git

cd AlphaCryo4D/

2.  Create the conda environment: 

conda create -n AlphaCryo4D python=3.7.1

3.  Activate the environment: 

source activate AlphaCryo4D

4.  Install the dependencies: 

conda install --yes --file EnvConda.txt 

pip install -r EnvPip.txt

==================================================

Documentation:

Programs and scripts are described in Docs/documentation_alphacryo4d.pdf. An example tutorial is provied in Docs/tutorial_alphacryo4d.pdf. The procedures are tested on the operating system of CentOS Linux release 7.6.1810. Please do not hesitate to reach our team should you encounter issues in using this system.

==================================================

The AlphaCryo4D Development Team:

Youdong Mao (PI), Zhaolong Wu, Shuwen Zhang, Yinping Ma, Wei Li Wang, Deyao Yin. (June 2021).

==================================================

Copyright ©2021 | The AlphaCryo4D Development Team

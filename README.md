AlphaCryo4D v0.1.0c Prototype System

==================================================

AlphaCryo4D is an open-source free software released under GNU General Public LICENSE that implements 3D classification of single-particle cryo-EM data using deep manifold learning and novel energy-based particle voting methods (originally proposed in the following bioRxiv preprint by the Mao laboratory). AlphaCryo4D v0.1beta is currently a prototype, NOT a stable released version, which is still under development. The authors wish to adopt the community development model to advance the future version of this open-source software with a more user-friendly interface. Users are free to use and modify the source code, providing their compliance with the GPL and that any publication making use of this software shall cite the following reference or its formally published form:

Zhaolong Wu, Shuwen Zhang, Wei Li Wang, Yinping Ma, Yuanchen Dong, Youdong Mao. Deep manifold learning reveals hidden dynamics of proteasome autoregulation. bioRxiv preprint doi: https://doi.org/10.1101/2020.12.22.423932.

==================================================

Installation:
1. Create the conda environment:
conda create -n AlphaCryo4D python=3.7.1

2. Activate the environment:
source activate AlphaCryo4D

3. Install the dependencies:
conda install --yes --file EnvConda.txt
pip install -r EnvPip.txt

==================================================

Programs and scripts are described in Docs/documentation_alphacryo4d.pdf. An example tutorial is provied in Docs/tutorial_alphacryo4d.pdf. Please do not hesitate to reach our team should you encounter issues in using this system.

==================================================

Copyright ©2021 | The AlphaCryo4D Development Team

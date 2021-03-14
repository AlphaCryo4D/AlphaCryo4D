AlphaCryo4D v0.1beta Prototype System

AlphaCryo4D is an open-source free software released under GNU General Public LICENSE that implements 3D classification of single-particle cryo-EM data using deep manifold learning and novel energy-based particle voting methods (originally proposed in the following bioRxiv preprint by the Mao laboratory). AlphaCryo4D v0.1beta is currently a prototype, NOT a stable released version, which is still under development. The authors wish to adopt the community development model to advance the future version of this open-source software with a more user-friendly interface. Users are free to use and modify the source code, providing their compliance with the GPL and that any publication making use of this software shall cite the following reference or its formally published form:

Zhaolong Wu, Shuwen Zhang, Wei Li Wang, Yinping Ma, Yuanchen Dong, Youdong Mao. Deep manifold learning reveals hidden dynamics of proteasome autoregulation. bioRxiv preprint doi: https://doi.org/10.1101/2020.12.22.423932.

Installation:
1. Create the conda environment:
conda create -n AlphaCryo4D python=3.7.1

2. Activate the environment:
source activate AlphaCryo4D

3. Install the dependencies:
conda install --yes --file EnvConda.txt
pip install -r EnvPip.txt


Programs and scripts in AlphaCryo4D v0.1beta are briefly described in the following.

Bootstrap Directory: 3D bootstrap with M-fold data augmentation and particle shuffling
1. randsf.py: split the star file of all particles into several sub-datasets.
2. bootstrap.py: augment each sub-dataset M times by particle shuffling.
3. link.sh: link the star and mrc files of 3D bootstrapping into two folders.
4. fit.sh: align all 3D density maps to a reference map to bring all volumes to the same frame of reference.
5. bigdata.py: prepare the 3D volume dataset after bootstrapping.

DeepFeature Directory: extract 3D feature by 3D deep residual autoencoder
6. run_prepare.py: preprocess the input data for deep neural network.
7. run_resnet.py: train the 3D residual autoencoder network.
8. run_predict.py: calculate the 3D feature by the autoencoder.

ManifoldLandscape Directory: manifold embedding of 3D volume data for free-energy landscape reconstitution
9. tsne_prepare.py: preprocess the 3D density maps and their feature maps for manifold learning.
10. tsne_rd.py: map the two-dimensional manifold embedding of input volume data by t-SNE.
11. enumerate.sh: count the particle number of each data point.
12. string_method.py: compute the free energy landscape and find the minimum energy path by the string method.

ParticleVoting Directory: 3D classification with particle voting on the free energy landscape
13. clustering.py: find the ID and distance to the nearest clustering center of the data points within one cluster.
14. vote_prepare.sh: prepare the star files of the points of one cluster.
15. gethead.py: get the header lines of these star files.
16. post_vote_and.sh: vote on particles by the energy-based algorithm.
17. post_and_parallel.sh: classify particles by the energy-based particle-voting algorithm in parallel.
18. post_or_parallel.sh: classify particles by the distance-based algorithm in parallel.
19. dedup.sh: remove the duplication of particles when using the distance-based algorithm.

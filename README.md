# neuronforest-analysis-scripts
Scripts to increase accuracy and speed of image segmentation evaluation and malis training objective calculation for affinity graphs of connectomes.  Intended for use with https://github.com/csinva/neuronforest-spark 

**Descriptions of Directories**

Note: Each major directory contains its own README.
* python: Contains python scripts and cython wrappers for C++ methods to calculate and visualize statistics from an image segmentation algorithm.
* matscripts: Contains matlab code to compare against python for calculating and visualizing statistics.
* src: Contains code for calculating the MALIS training objective using wrappers for C++ code.
* launchScripts: Scripts for starting a spark job on the Janelia cluster.

**Cloning The Repo**

To get all files for matlab, use ```git clone --recursive``` when cloning the repo.

**Dependencies**

This project requires Java SDK (reccomended 1.7), Scala SDK (reccomended 2.10), and Apache Spark to be installed.  IntelliJ is reccomended for development.  In order to add libraries to IntelliJ, put jar files into the *lib* directory, right click them, and click *Add as Library*.  Do the same for the jar files that are already in the *lib* folder.

**Compiling and Running**

There are separate bash files for compiling different parts of the project.  If any give a *Permission Denied* error, cd into the containing direcory and type ```chmod +rwx file.sh```.

In order to run on the Janelia Cluster, see instructions at https://github.com/csinva/neuronforest-spark 
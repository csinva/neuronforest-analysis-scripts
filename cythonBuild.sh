#!/usr/bin/env bash
echo "STARTING BUILD"
cd connectedComponents
pwd
python setup.py build_ext --inplace
cd ..
cd randStats
pwd
python setup.py build_ext --inplace
cd ..
cd watershed
pwd
python setup.py build_ext --inplace
cd ..
echo "FINISHED BUILD"
#!/usr/bin/env bash
echo "STARTING BUILD"
cd connectedComponents
printf "\n${PWD##*/}\n"
python setup.py build_ext --inplace
cd ..
cd randStats
printf "\n${PWD##*/}\n"
python setup.py build_ext --inplace
cd ..
cd pixelStats
printf "\n${PWD##*/}\n"
python setup.py build_ext --inplace
cd ..
cd watershed
printf "\n${PWD##*/}\n"
python setup.py build_ext --inplace
cd ..
printf "\nFINISHED BUILD\n"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:'/groups/turaga/home/singhc/analysis-scripts/src/test/libctest.so'
launchScripts/inflame.sh 1 out/artifacts/main.jar Main
sleep 2s
qstat
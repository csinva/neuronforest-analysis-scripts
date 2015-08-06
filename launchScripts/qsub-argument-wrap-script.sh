#$ -S /bin/bash

wait_for_job_file () {
    COUNT=1
    MAX_COUNT=100
    SUCCESS=1
    while [ ! -f "$1" ]; do
        printf "sleeping for 2 seconds... %02d/100\n" "$COUNT" >&2
        sleep 2
        if [ "$COUNT" -eq "5" ]; then
            echo "Could not find job file after 200s, killing job." >&2
            SUCCESS=0
            break
        fi
        COUNT=$(($COUNT+1))
    done
    if [ $SUCCESS -eq 1 ]; then
        exit 0
    else
        exit 1
    fi
}

JOB_ID_FILE="$1"
shift
SCRIPT_FILE="$1"
shift

`wait_for_job_file "$JOB_ID_FILE"`
JOB_ID_FILE_EXISTS=$?
if [ $JOB_ID_FILE_EXISTS -eq 0 ]; then
    JOB=`cat "$JOB_ID_FILE"`
    rm "$JOB_ID_FILE"
else
    echo "Could not find tmp file with job id." >&2
    exit 1
fi


echo "starting master..."
export PATH=/usr/local/spark-current/bin:/usr/local/spark-current/sbin:/usr/local/python-2.7.6/bin:$PATH
export SPARK_HOME=/usr/local/spark-current
/usr/local/spark-current/sbin/start-master.sh



export PATH=/sge/current/bin/lx-amd64:$PATH

JOB_INFO=`qstat | grep $JOB`
HOST=`echo $JOB_INFO | awk '{print $8}' | cut -d@ -f2`
N_NODES=`echo $JOB_INFO | awk '{print $10}'`
N_NODES=$(($N_NODES - 1))
N_CORES_PER_MACHINE=16

export PARALLELISM=$(($N_NODES * $N_CORES_PER_MACHINE * 3))
#export MASTER="spark://h01u25.int.janelia.org:7077"
export MASTER=spark://$HOSTNAME:7077
echo $MASTER

"$SCRIPT_FILE" $@

    

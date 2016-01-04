# python evaluation scripts
The subdirectories of this folder contain code that has been wrapped with Cython.  If they are changed, cythonBuild.sh must be run in order to compile those changes.  To test if everything is running run: ```python mainTest.py ```  In order to calculate statistics on new data, set your number of threads and data locations in main.py and run it.  To view the output call makeErrorCurves.py.  An example of this is shown in visualizeStats.py To view your labels and predictions use ImageScan.py.
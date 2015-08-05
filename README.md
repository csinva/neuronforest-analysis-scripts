# neuronforest-analysis-scripts
Python scripts to replace Matlab for evaluation of error in connectome images and affinity graphs.

**Building cpp methods**
In order to build all the cpp files into workable python modules, run the cythonBuild.sh script.

**Setting Up Spark**
Download and save a spark binary.  Make sure your python path points to it.
Make sure your JAVA_HOME points to a valid jdk.

**Setting Up Bridj**
Download the Bridj jar from http://search.maven.org/#artifactdetails|com.nativelibs4java|bridj|0.7.0|bundle and include it as a library in the lib folder.

**Setting Up JNA**
Download jnaerator.jar (get a version with -shaded) and run the following on C++ files:
java -jar jnaerator.jar -library Test Test.h -o . -v -noJar -noComp
Include it as a lib in the lib folder.

If you're in the top directory:
java -jar ../lib/jnaerator.jar main/cpp/clib.h -v -noJar -noComp -package main.java  -f -convertBodies -forceNames -runtime BridJ

**Compliling clib**
In the src directory:
g++ -Wall -shared -fPIC -o main/cpp/clib.so main/cpp/clib.cpp
(libctest.so must be under src)
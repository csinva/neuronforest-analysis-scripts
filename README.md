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

If you're in the top directory:
java -jar jnaFull.jar Test.h -v -noJar -noComp -package main.scala.jnahello.test -f -convertBodies -forceNames -runtime BridJ

**Hello World c**
g++ -Wall -shared -fPIC -o libctest.so ctest.c
javac -classpath jnaFull.jar HelloWorld.java
java -classpath jnaFull.jar:. HelloWorld
libctest.so must be under src
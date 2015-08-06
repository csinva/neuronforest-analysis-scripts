# malis wrappers
Set of C++ wrappers for MALIS in different languages.  The matlab implementation is working (run calcGrads.m) and the Scala implementation is working, but is not parallelizable.  In order to make changes to the raw C++ being called, the clib.cpp and clib.h files in the cpp directory must be altered.  Then, the compileClib.sh script must be run.

The main changes should be made to Main.scala.  This loads some inputs, calculates their MALIS loss, and saves them.  The goal is to do this in parallel.

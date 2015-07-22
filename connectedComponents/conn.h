#ifndef TESTLIB_H
#define TESTLIB_H

#include <iostream>
#include <list>

std::list<int> connectedComponentsCPP(double * conn, double * nhood, int dimX, int dimY, int dimZ, double * outputComp, std::list<int> * l);

#endif
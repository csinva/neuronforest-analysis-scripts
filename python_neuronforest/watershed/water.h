#ifndef TESTLIB_H
#define TESTLIB_H

#include <iostream>
#include <list>

void watershed(double * conn, double * nhood,double * comp, double* growMask, double lowThreshold, int dimX,int dimY,int dimZ, double * outputComp);
#endif
/* ctest.c */
#include "clib.h"
#include <iostream>
#include <cstdlib>
#include <cmath>
#include <boost/pending/disjoint_sets.hpp>
#include <vector>
#include <queue>
#include <map>
using namespace std;

extern "C"
{
    void helloFromC() {
        cout << "C++ is working" << endl;
    }

    int arrTest(int size){
        cout << "arrTest" << endl;
        cout << "size: " << size << endl;
        return size;
    }
    int arrDouble(int* arr, int* arr2, int size){
        for(int i=0;i<10;i++){
            for(int j=0;j<10;j++){
                arr2[i]=arr[i]*2;
            }
        }
        return 0;
    }
    /*
     * Compute the MALIS loss function and its derivative wrt the affinity graph
     * MAXIMUM spanning tree
     * Author: Srini Turaga (sturaga@mit.edu)
     * All rights reserved
     */
     void malisLoss(const int* dims, const float* conn, const double* nhood, const int* seg, const double marginArg, const bool posArg, float* losses, double loss, double classErr, double randIndex){
     	/* input arrays */
     	cout << "dims: "<<dims[0]<<" "<<dims[1]<<" "<<dims[2]<<" "<<dims[3]<<endl;
         // 4d connectivity graph [y * x * z * #edges]
     	const int	conn_num_dims		= 4;
     	const int*	conn_dims			= dims;
     	const int	conn_num_elements	= dims[0]*dims[1]*dims[2]*dims[3];
     	const float*	conn_data		= conn;
         // graph neighborhood descriptor [3 * #edges]
     	const int	nhood_num_dims		= dims[3]*dims[3];
     	const int nhoodDims[2]          = {dims[3],dims[3]};
     	const int*	nhood_dims			= &nhoodDims[0];
     	const double*	nhood_data		= nhood;
         // true target segmentation [y * x * z]
     	const int	seg_num_dims		= 3;
     	const int*	seg_dims			= dims;
     	const int	seg_num_elements	= dims[0]*dims[1]*dims[2];
     	const int*	seg_data			= seg;
         // sq-sq loss margin [0.3]
         const double    margin         = marginArg;
         // is this a positive example pass [true] or a negative example pass [false] ?
         const bool      pos            = posArg;

         /*
            seg uint16_t -> int
            seg_dims -> 4 dims instead of 3

         */
     }
}

/* Connected components
 * developed and maintained by Srinivas C. Turaga <sturaga@mit.edu>
 * do not distribute without permission.
 */
#include "conn.h"
#include <iostream>
#include <cstdlib>
#include <vector>
#include <stack>
using namespace std;


// zero-based sub2ind
int sub2ind(const int * sub,const int num_dims,const int * dims)
{
	int ind = 0;
	int prod = 1;
	for (int d=0; d<num_dims; d++) {
		ind += sub[d] * prod;
		prod *= dims[d];
	}
	return ind;
}

// zero-based ind2sub
void ind2sub(int ind,const int num_dims,const int * dims,int * sub)
{
	for (int d=0; d<num_dims; d++) {
		sub[d] = (ind % dims[d]);
		ind /= dims[d];
	}
	return;
}


void printlist(list<int> &l){
    for(list<int>::const_iterator i = l.begin(); i != l.end(); i++)
    cout << *i << ' ';
    cout << endl;}

int printArr(double * conn, double * nhood, int dimX, int dimY, int dimZ){
    cout << "printing conn..." << endl;
    for(int i=0;i<20;i++){
        cout << conn[i] << " ";
    }
    cout << endl;

    cout << "printing nhood..." << endl;
    for(int i=0;i<3;i++){
        cout << nhood[i] << " ";
    }
    cout << endl;

    cout << "printing dims..." << endl;
    cout << dimX << " " << dimY << " " << dimZ << endl;
    return 3;
}

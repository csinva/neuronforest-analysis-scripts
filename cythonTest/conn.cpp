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

list<int> printArr(double * conn, double * nhood, int dimX, int dimY, int dimZ, double * outputComp, list<int> * cmpSz){
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

    //const mxArray * conn = prhs[0];
    const int conn_num_dims = 4;
    int dims[4] = {dimX,dimY,dimZ,3};
    const int * conn_dims = &dims[0];
    cout << "dims again..." << endl;
    cout << conn_dims[0] << " " << conn_dims[1] << " " << conn_dims[2] << endl;
    const int conn_num_elements = conn_dims[0]*conn_dims[1]*conn_dims[2];
    //const mxLogical * conn_data = mxGetLogicals(conn);
    const double* conn_data = conn;
    //const mxArray * nhood1 = prhs[1];

    const int nhood1_num_dims = 2;
    int nhoodDims[2] = {3,3};
    const int * nhood1_dims = &nhoodDims[0];
    const double * nhood1_data = nhood;


    outputComp[0] = 3;
    (*cmpSz).push_back(5);

    cout << "finished, returning..." << endl;
    return *cmpSz;

}

/*
// input mapping
	const mxArray * conn = prhs[0];
	const mwSize conn_num_dims = mxGetNumberOfDimensions(conn);
	const mwSize * conn_dims = mxGetDimensions(conn);
	const mwSize conn_num_elements = mxGetNumberOfElements(conn);
	const mxLogical * conn_data = mxGetLogicals(conn);
	const mxArray * nhood1 = prhs[1];
	const mwSize nhood1_num_dims = mxGetNumberOfDimensions(nhood1);
	const mwSize * nhood1_dims = mxGetDimensions(nhood1);
	const double * nhood1_data = mxGetPr(nhood1);
	if (nhood1_num_dims != 2) {
		mexErrMsgTxt("wrong size for nhood1");
	}
	if ((nhood1_dims[1] != (conn_num_dims-1))
		|| (nhood1_dims[0] != conn_dims[conn_num_dims-1])){
		mexErrMsgTxt("nhood1 and conn dimensions don't match");
	}
	//nhood 2 is completely ignored

	// output mapping
	mxArray * label;
	mwSize label_num_dims = conn_num_dims-1;
	mwSize label_dims[conn_num_dims - 1];
	for (mwSize i=0; i<(conn_num_dims-1); i++){
		label_dims[i] = conn_dims[i];
	}
	plhs[0] = mxCreateNumericArray(label_num_dims,label_dims,mxUINT32_CLASS,mxREAL);
	if (plhs[0] == NULL) {
		mexErrMsgTxt("Unable to create output array");
		return;
	}

	label=plhs[0];
	uint32_t * label_data = (uint32_t *) mxGetData(label);
	mwSize label_num_elements = mxGetNumberOfElements(label);

	// initialize colors (a node is either discovered or not), maybe change to integer?
	//bool discovered[label_num_elements];
	bool * discovered = (bool *) mxMalloc(label_num_elements*sizeof(bool));
	for (mwSize i=0; i<label_num_elements; i++){
		discovered[i]=false;
	}
*/
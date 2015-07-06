/* Marker-based watershed segmentation
 * developed and maintained by Srinivas C. Turaga <sturaga@mit.edu>
 * do not distribute without permission.
 */


#include "water.h"
#include <iostream>
#include <cstdlib>
#include <boost/pending/disjoint_sets.hpp>
#include <vector>
#include <map>
#include <queue>
using namespace std;

// zero-based sub2ind (column-major order)
int sub2ind(const int * sub,const int num_dims,const int * dims){
	int ind = 0;
	int prod = 1;
	for (int d=0; d<num_dims; d++) {
		ind += sub[d] * prod;
		prod *= dims[d];
	}
	return ind;
}

// zero-based ind2sub
void ind2sub(int ind,const int num_dims,const int * dims,int * sub){
	for (int d=0; d<num_dims; d++) {
		sub[d] = (ind % dims[d]);
		ind /= dims[d];
	}
	return;
}



class mycomp{
    const double * conn_data;
    public:
        mycomp(const double * conn_data_param){
            conn_data = conn_data_param;
        }
        bool operator() (const int& ind1, const int& ind2) const {
            return conn_data[ind1]<conn_data[ind2];
        }
};
    
//MAXIMUM spanning tree
void watershed(double * conn, double * nhood,double * comp, double* growMask, double lowThreshold, int dimX,int dimY,int dimZ, double * outputComp){

//void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[]){
		//    const mxArray * conn = prhs[0];
	const int conn_num_dims = 4;	//mxGetNumberOfDimensions(conn);
	int connDims[4]={dimX,dimY,dimZ,3};
    const int * conn_dims  =&connDims[0];
		//const int * conn_dims = mxGetDimensions(conn);
	const int conn_num_elements = dimX*dimY*dimZ*3;		//mxGetNumberOfElements(conn);
		//const float * conn_data =(const float *)mxGetData(conn);
	const double * conn_data = conn;	 //conn_data changed to double *
		//const mxArray * nhood = prhs[1];
	const int nhood_num_dims = 2;//mxGetNumberOfDimensions(nhood);
	int nhoodDims[2] = {3,3};
	const int * nhood_dims=&nhoodDims[0];
		//const int * nhood_dims = mxGetDimensions(nhood);

	const double * nhood_data = nhood;//(const double *)mxGetData(nhood);
    	//const mxArray * marker = prhs[2];
	const int marker_num_dims = 3;//mxGetNumberOfDimensions(marker);
		//const int * marker_dims = mxGetDimensions(marker);

	int markerDims[3]={dimX,dimY,dimZ};
	const int * marker_dims  =&markerDims[0];
	const int num_vertices = dimX*dimY*dimZ;//mxGetNumberOfElements(marker);

	const double * marker_data = comp;//(const uint32_t *)mxGetData(marker);
    	//const mxArray * grow_mask = prhs[3];
	const int grow_mask_num_dims = 3;//mxGetNumberOfDimensions(grow_mask);
		//const int * grow_mask_dims = mxGetDimensions(grow_mask);
		//const mxLogical * grow_mask_data = growMask;//(const mxLogical *)mxGetLogicals(grow_mask);
	const double * grow_mask_data = growMask;
	const double low_threshold = lowThreshold;//(const double) mxGetScalar(prhs[4]);

	/*CHANDAN changes:
		conn_data (float * -> double *)
		marker_data (const uint32_t * -> double *)
		growMask (mxLogical * -> double *)
		later: label_data (uint32* -> double*)
			check cast on v2array
			cast on label_of_set
	*/

	/*
    if (!mxIsSingle(conn)){
        mexErrMsgTxt("Conn array must be floats (singles)");
    }
    if (nhood_num_dims != 2) {
		mexErrMsgTxt("wrong size for nhood");
	}
	if ((nhood_dims[1] != (conn_num_dims-1))
		|| (nhood_dims[0] != conn_dims[conn_num_dims-1])){
		mexErrMsgTxt("nhood and conn dimensions don't match");
	}
	*/

	// create disjoint sets
	//   int num_vertices = marker_num_elements;	//conn_dims[0]*conn_dims[1]*conn_dims[2];
    std::vector<int> rank(num_vertices);
    std::vector<int> parent(num_vertices);
    boost::disjoint_sets<int*, int*> dsets(&rank[0],&parent[0]);
    for (int i=0; i<num_vertices; i++){
        dsets.make_set(i);
    }

	// output array
    //mxArray * label;
    int label_num_dims=marker_num_dims;
    int label_dims[label_num_dims];
    for (int i=0; i<label_num_dims; i++){
        label_dims[i]=marker_dims[i];
    }

	//plhs[0] = mxCreateNumericArray(label_num_dims,label_dims,mxUINT32_CLASS,mxREAL);
    //label=outputComp;//plhs[0];
	//uint32_t * label_data = (uint32_t *) mxGetData(label);
	double * label_data = outputComp;
    int label_num_elements= dimZ*dimY*dimX;	//mxGetNumberOfElements(label);

	// initialize output array and find representatives of each class
	std::map<double,int> components;
    for (int i=0; i<label_num_elements; i++){
        label_data[i]=marker_data[i];
		if (label_data[i] > 0){
			components[label_data[i]] = i;
		}
    }

	// merge vertices labeled with the same marker
    for (int i=0; i<label_num_elements; i++){
		if (label_data[i] > 0){
			dsets.union_set(components[label_data[i]],i);
		}
    }

	// sort the list of edges
    std::priority_queue <double, vector<double>, mycomp > pqueue (conn_data);

    for (int iEdge=0; iEdge<conn_num_elements; iEdge++){
		if (conn_data[iEdge] > low_threshold){

			// check to see if either vertex attached to this edge is grow-able
			int edge_array[conn_num_dims];

			ind2sub(iEdge,conn_num_dims,conn_dims,edge_array);
			int v1, v2;
			int v1_array[conn_num_dims-1], v2_array[conn_num_dims-1];
			for (int i=0; i<conn_num_dims-1; i++){
				v1_array[i]=edge_array[i];
				v2_array[i]=edge_array[i];
			}

			for (int i=0; i<nhood_dims[1]; i++){
				v2_array[i]+= (int) nhood_data[nhood_dims[0]*i+edge_array[conn_num_dims-1]];
			}
            v1=sub2ind(v1_array, conn_num_dims-1, conn_dims);
            v2=sub2ind(v2_array, conn_num_dims-1, conn_dims);
			if (grow_mask_data[v1] || grow_mask_data[v2]){
		        pqueue.push(iEdge);
			}

		}
    }


    while (!pqueue.empty()){

        int cur_edge=pqueue.top();
        pqueue.pop();
        int edge_array[conn_num_dims];
        ind2sub(cur_edge,conn_num_dims,conn_dims,edge_array);

        int v1, v2;
        int v1_array[conn_num_dims-1], v2_array[conn_num_dims-1];
        for (int i=0; i<conn_num_dims-1; i++){
            v1_array[i]=edge_array[i];
            v2_array[i]=edge_array[i];
        }
        for (int i=0; i<nhood_dims[1]; i++){
            v2_array[i]+= (int) nhood_data[nhood_dims[0]*i+edge_array[conn_num_dims-1]];
        }

        bool OOB=false;
        for (int i=0; i<conn_num_dims-1; i++){
            if (v2_array[i]<0 || v2_array[i]>=conn_dims[i]){
                OOB=true;
            }
        }

        if (!OOB){
            v1=sub2ind(v1_array, conn_num_dims-1, conn_dims);
            v2=sub2ind(v2_array, conn_num_dims-1, conn_dims);

            int set1=dsets.find_set(v1);
            int set2=dsets.find_set(v2);
			int label_of_set1 = label_data[set1]; //why doesn't this throw casting error?
			int label_of_set2 = label_data[set2];

			if ((set1!=set2)
					&& (((label_of_set1 == 0) && grow_mask_data[set1])
						|| ((label_of_set2 == 0) && grow_mask_data[set2]))
					){
				dsets.link(set1, set2);
				// funkiness: either label_of_set1 is 0 or label_of_set2 is 0.
				// so the sum of the two values should the value of the non-zero
				// using this trick to find the new label
				label_data[dsets.find_set(set1)] = label_of_set1+label_of_set2;
            }

        }

    }

	// write out the final coloring
	for (int i=0; i<label_num_elements; i++){
		label_data[i] = label_data[dsets.find_set(i)];
	}

}

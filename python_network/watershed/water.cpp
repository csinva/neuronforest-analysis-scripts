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

// zero-based ind2sub for doubles
void ind2subdub(int ind,const int num_dims,const int * dims,double * sub){
	for (int d=0; d<num_dims; d++) {
		sub[d] = (ind % dims[d]);
		ind /= dims[d];
	}
	return;
}
// zero-based sub2ind for doubles
int sub2inddub(const double * sub,const int num_dims,const int * dims){
	int ind = 0;
	int prod = 1;
	for (int d=0; d<num_dims; d++) {
		ind += sub[d] * prod;
		prod *= dims[d];
	}
	return ind;
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
	const int conn_num_dims = 4;
	int connDims[4]={dimX,dimY,dimZ,3};
    const int * conn_dims  =&connDims[0];
	const int conn_num_elements = dimX*dimY*dimZ*3;
	const double * conn_data = conn;

	const int nhood_num_dims = 2;
	int nhoodDims[2] = {3,3};
	const int * nhood_dims=&nhoodDims[0];
	const double * nhood_data = nhood;

	const int marker_num_dims = 3;
	int markerDims[3]={dimX,dimY,dimZ};
	const int * marker_dims  =&markerDims[0];
	const int num_vertices = dimX*dimY*dimZ;

	const double * marker_data = comp;
	const int grow_mask_num_dims = 3;

	const double * grow_mask_data = growMask;
	const double low_threshold = lowThreshold;

	/*CHANDAN changes:
		conn_data (float * -> double *)
		marker_data (const uint32_t * -> double *)
		growMask (mxLogical * -> double *)
		later: label_data (uint32* -> double*)
			check cast on v2array
			cast on label_of_set
	*/

	// create disjoint sets
    std::vector<double> rank(num_vertices);
    std::vector<double> parent(num_vertices);
    boost::disjoint_sets<double*, double*> dsets(&rank[0],&parent[0]);
    for (int i=0; i<num_vertices; i++){
        dsets.make_set(i);
    }

	// output array

    int label_num_dims=marker_num_dims;
    int label_dims[label_num_dims];
    for (int i=0; i<label_num_dims; i++){
        label_dims[i]=marker_dims[i];
    }

	double * label_data = outputComp;
    int label_num_elements= dimZ*dimY*dimX;

	// initialize output array and find representatives of each class
	std::map<double,int> components;
    for (int i=0; i<label_num_elements; i++){
        label_data[i]=marker_data[i];
		if (label_data[i] > 0){
			components[label_data[i]] = (double) i;
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
			double edge_array[conn_num_dims];

			ind2subdub(iEdge,conn_num_dims,conn_dims,edge_array);
			int v1, v2;
			double v1_array[conn_num_dims-1], v2_array[conn_num_dims-1];
			for (int i=0; i<conn_num_dims-1; i++){
				v1_array[i]=edge_array[i];
				v2_array[i]=edge_array[i];
			}

			for (int i=0; i<nhood_dims[1]; i++)
				v2_array[i]+= (int) nhood_data[(int)(nhood_dims[0]*i+edge_array[conn_num_dims-1])];

            v1=sub2inddub(v1_array, conn_num_dims-1, conn_dims);
            v2=sub2inddub(v2_array, conn_num_dims-1, conn_dims);
			if (grow_mask_data[v1] || grow_mask_data[v2])
		        pqueue.push(iEdge);


		}
    }

    while (!pqueue.empty()){
        int cur_edge=pqueue.top();
        pqueue.pop();
        double edge_array[conn_num_dims];
        ind2subdub(cur_edge,conn_num_dims,conn_dims,edge_array);

        int v1, v2;
        double v1_array[conn_num_dims-1], v2_array[conn_num_dims-1];
        for (int i=0; i<conn_num_dims-1; i++){
            v1_array[i]=edge_array[i];
            v2_array[i]=edge_array[i];
        }
        for (int i=0; i<nhood_dims[1]; i++){
            v2_array[i]+= (int) nhood_data[(int)(nhood_dims[0]*i+edge_array[conn_num_dims-1])];
        }


        bool OOB=false;
        for (int i=0; i<conn_num_dims-1; i++){
            if (v2_array[i]<0 || v2_array[i]>=conn_dims[i]){
                OOB=true;
            }
        }


        if (!OOB){
            v1=sub2inddub(v1_array, conn_num_dims-1, conn_dims);
            v2=sub2inddub(v2_array, conn_num_dims-1, conn_dims);

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
	for (int i=0; i<label_num_elements; i++)
		label_data[i] = label_data[dsets.find_set(i)];



}

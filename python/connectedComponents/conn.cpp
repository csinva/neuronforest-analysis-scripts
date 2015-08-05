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

list<int> connectedComponentsCPP(double * conn, double * nhood, int dimX, int dimY, int dimZ, double * outputComp, list<int> * cmpSz){

    //reading inputs //todo: check for different number of affinities
    const int conn_num_dims = 4;
    int dims[4] = {dimX,dimY,dimZ,3};
    const int * conn_dims = &dims[0];
    const int conn_num_elements = dimX*dimY*dimZ*3;
    const double* conn_data = conn;
    const int nhood1_num_dims = 2;
    int nhoodDims[2] = {3,3};
    const int * nhood1_dims = &nhoodDims[0];
    const double * nhood1_data = nhood;

    // output mapping
    double* label = outputComp;
    int label_num_dims = conn_num_dims-1;
    int label_dims[conn_num_dims - 1];
    for (int i=0; i<(conn_num_dims-1); i++){
        label_dims[i] = conn_dims[i];
    }
    double* label_data = (double *)  label;
    int label_num_elements = dimX*dimY*dimZ;

    // initialize colors (a node is either discovered or not), maybe change to integer?
    bool discovered[label_num_elements];
    //bool * discovered = (bool *) mxMalloc(label_num_elements*sizeof(bool));
    for (int i=0; i<label_num_elements; i++){
        discovered[i]=false;
    }

    // run algorithm
    std::stack<int> S;
    std::vector<int> component_sizes;
    for (int ind=0; ind<label_num_elements; ind++){
        if (discovered[ind]==false){
            S.push(ind);
            component_sizes.push_back(1);
            label_data[ind]=component_sizes.size();
            discovered[ind]=true;
            int current;
            while (!S.empty()){
                current=S.top();
                int cur_pos[label_num_dims];
                ind2sub(current, label_num_dims, label_dims, cur_pos);
                S.pop();
                int nbor[conn_num_dims];
                int nbor_ind;
                int new_pos[label_num_dims];
                int new_ind;
                for (int i=0; i<label_num_dims; i++){
                    nbor[i]=cur_pos[i];
                }
                for (int i=0; i<nhood1_dims[0]; i++){
                    nbor[conn_num_dims-1]=i;
                    nbor_ind=sub2ind(nbor,conn_num_dims,conn_dims);
                    if (conn_data[nbor_ind]){
                        bool OOB=false;
                        for (int j=0; j<label_num_dims; j++){
                            int check=cur_pos[j]+(int) nhood1_data[i+j*nhood1_dims[0]];
                            if (check<0 || check>=label_dims[j]){
                                OOB=true;
                            }
                            new_pos[j]=check;
                        }
                        if (!OOB){
                            new_ind=sub2ind(new_pos,label_num_dims,label_dims);
                            if (!discovered[new_ind]){
                                S.push(new_ind);
                                label_data[new_ind]=component_sizes.size();
                                discovered[new_ind]=true;
                                component_sizes.back()+=1;
                            }
                        }
                    }
                }
                for (int i=0; i<nhood1_dims[0]; i++){
                    bool OOB=false;
                    for (int j=0; j<label_num_dims; j++){
                        int check=cur_pos[j]- (int) nhood1_data[i+j*nhood1_dims[0]];
                        if (check<0 || check>=label_dims[j]){
                            OOB=true;
                        }
                        new_pos[j]=check;
                    }
                    if (!OOB){
                        for (int j=0; j<label_num_dims; j++){
                            nbor[j]=new_pos[j];
                        }
                        nbor[conn_num_dims-1]=i;
                        nbor_ind=sub2ind(nbor, conn_num_dims, conn_dims);
                        if (conn_data[nbor_ind]){
                            new_ind=sub2ind(new_pos, label_num_dims, label_dims);
                            if (!discovered[new_ind]){
                                S.push(new_ind);
                                label_data[new_ind]=component_sizes.size();
                                discovered[new_ind]=true;
                                component_sizes.back()+=1;
                            }
                        }
                    }
                }
            }
        }
    }

    // return component sizes
    list<int> compSizes = *cmpSz;
    for (int i=0; i<(int)component_sizes.size(); i++){
        compSizes.push_back(component_sizes[i]);
        //psizes[i]=(uint32_t)component_sizes[i];
    }

    // return outputComp
    //outputComp=(double*)label_data;
    //outputComp[0] = 3;

    int sum=0;
    //for (int i=0; i<label_num_elements; i++){
        //outputComp[i]=label_data[i];
        //cout << label_data[i] << " ";
        //psizes[i]=(uint32_t)component_sizes[i];
      //  sum+=label_data[i];
    //}
    //cout << "very initial sum: " << sum << endl;
    outputComp = (double *) label_data;


    //(*cmpSz).push_back(5);
    return compSizes;

}
/* ctest.c */
#include "clib.h"
#include <iostream>
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
    int arrSum(int* arr, int size){
        int sum=0;
        for(int i=0;i<size;i++){
            sum+=arr[i];
        }
        return sum;
    }
}

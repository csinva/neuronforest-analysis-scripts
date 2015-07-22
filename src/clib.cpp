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
    int arrDouble(int* arr, int* arr2, int size){
        for(int i=0;i<size;i++){
            arr2[i]=arr[i]*2;
        }
        return 0;
    }
}

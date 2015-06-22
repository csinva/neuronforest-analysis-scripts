#include "conn.h"

using namespace std;

void printlist(list<int> &l){
    for(list<int>::const_iterator i = l.begin(); i != l.end(); i++)
    cout << *i << ' ';
    cout << endl;}

int printArr(double * conn){
    cout << "works" << endl;
    cout << conn[0];
    cout << conn[1];
    cout << conn[2] << endl;
    return 3;
}

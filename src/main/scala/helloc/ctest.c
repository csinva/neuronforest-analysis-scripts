/* ctest.c */

#include <stdio.h>
extern "C"
    {
    void helloFromC() {
        printf("Hello from C!\n");
    }
}
int main(){}

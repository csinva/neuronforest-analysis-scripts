
#define PAIRS_COUNT 10
#define EXPRESSION (1 << 10) | (1 << 5)

// Be careful with that one : intArray and source are const, dest is not
void CopyBytes(char* dest, const char* source, int n, const int* intArray);

// These are test comments
int testFunc(int x);
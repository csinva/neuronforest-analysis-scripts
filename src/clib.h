extern "C"
{
    void helloFromC();
    int arrTest(int size);
    int arrSum(int* arr, int size);
    void malisLoss(const int* dims, const float* conn, const double* nhood, const int* seg, const double margin, const bool pos, float* losses, double *loss, double *randIndex);
}
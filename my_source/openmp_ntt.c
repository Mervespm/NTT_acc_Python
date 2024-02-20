#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

#define N 256
#define QINV -3327
#define KYBER_Q 3329

const int16_t zetas[128] = {
  -1044,  -758,  -359, -1517,  1493,  1422,   287,   202,
   -171,   622,  1577,   182,   962, -1202, -1474,  1468,
    573, -1325,   264,   383,  -829,  1458, -1602,  -130,
   -681,  1017,   732,   608, -1542,   411,  -205, -1571,
   1223,   652,  -552,  1015, -1293,  1491,  -282, -1544,
    516,    -8,  -320,  -666, -1618, -1162,   126,  1469,
   -853,   -90,  -271,   830,   107, -1421,  -247,  -951,
   -398,   961, -1508,  -725,   448, -1065,   677, -1275,
  -1103,   430,   555,   843, -1251,   871,  1550,   105,
    422,   587,   177,  -235,  -291,  -460,  1574,  1653,
   -246,   778,  1159,  -147,  -777,  1483,  -602,  1119,
  -1590,   644,  -872,   349,   418,   329,  -156,   -75,
    817,  1097,   603,   610,  1322, -1285, -1465,   384,
  -1215,  -136,  1218, -1335,  -874,   220, -1187, -1659,
  -1185, -1530, -1278,   794, -1510,  -854,  -870,   478,
   -108,  -308,   996,   991,   958, -1460,  1522,  1628
};

int16_t new_zetas[256][7]; // Make sure to initialize this array with the appropriate values

int16_t montgomery_reduce(int32_t a) {
    int16_t t = (int16_t)(a * QINV);
    t = (int16_t)((a - t * KYBER_Q) >> 16);
    return t;
}

void zeta_init() {
    int k = 1;
    int len_ = 128;
    int col = 0;
    while (len_ >= 2) {
        int start = 0;
        int row = 1;
        while (start < N) {
            int16_t zeta = zetas[k];
            k += 1;
            int j = start;
            while (j < start + len_) {
                j += 1;
                new_zetas[row][col] = zeta;
                row += 2;
            }
            start = j + len_;
        }
        len_ >>= 1;
        col += 1;
    }
}

void ntt(int16_t r[N]) {
    int k = 1;
    int len_ = 128;
    while (len_ >= 2) {
        int start = 0;
        #pragma omp parallel for
        for (start = 0; start < N; start += 2 * len_) {
            int16_t zeta = zetas[k];
            k += 1;
            for (int j = start; j < start + len_; j++) {
                int32_t t = montgomery_reduce(zeta * r[j + len_]);
                r[j + len_] = r[j] - t;
                r[j] = r[j] + t;
            }
        }
        len_ >>= 1;
    }
}

int main() {
    int16_t poly[N];
    // Initialize poly with your values or a random function

    // Initialize new_zetas using zeta_init function
    zeta_init();

    // Measure the execution time of the ntt function
    clock_t start, end;
    double cpu_time_used;

    start = clock();
    for (int i = 0; i < 1000; i++) {
        // Assuming poly is already initialized with values
        ntt(poly);
    }
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;

    printf("Execution time: %lf seconds\n", cpu_time_used);

    return 0;
}

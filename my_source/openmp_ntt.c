#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

#define N 256
#define QINV -3327
#define KYBER_Q 3329

int16_t zetas[128] = {0}; // assuming this array is initialized elsewhere



void zeta_init(int32_t new_zetas[128][256], int16_t zetas[][256]) {
    int16_t k = 0;
    int16_t len_ = 128;
    int16_t col = 0;
    while (len_ >= 2) {
        int16_t start = 0;
        int16_t row = 1;
        while (start < 256) {
            int16_t *zeta = zetas[k++];
            int16_t j = start;
            while (j < start + len_) {
                new_zetas[row][col] = (int32_t)zeta[j];
                row += 2;
                j++;
            }
            start = j + len_;
        }
        len_ >>= 1;
        col++;
    }
}

int16_t montgomery_reduce_new(int32_t a) {
    int32_t t = ((int64_t)a * QINV) >> 16;
    t *= KYBER_Q;
    int16_t res = (int16_t)(a - t);
    return res;
}
void ntt_new(int16_t r[256]) {
    int16_t len_ = 128;
    int16_t cnt = 0;
    while (len_ >= 2) {
        int16_t start = 0;
        #pragma omp parallel for
        for (int16_t i = 0; i < 256; ++i) {
            int32_t a = (int32_t)new_zetas[cnt][i] * r[i];
            r[i] = (int16_t)a;
        }
        while (start < 256) {
            #pragma omp parallel for
            for (int16_t j = start; j < start + len_; ++j) {
                int32_t t = montgomery_reduce_new((int32_t)new_zetas[cnt][j + len_] * r[j + len_]);
                r[j + len_] = (int16_t)(r[j] - t);
                r[j] = (int16_t)(r[j] + t);
            }
            start += 2 * len_;
        }
        len_ >>= 1;
        cnt += 1;
    }
}


int main() {
    int16_t poly[N];
    
    
    int res = 0;
    double time_spent =0;
    clock_t begin = clock();
    clock_t end = clock();
    int i, j;


    for (i=0; i<1000; i++){
		for (j=0; j<256; j++)
			poly[j]= rand()%0x10000;
		begin = clock();
		ntt_new(poly);
		end = clock();
		time_spent += (double)(end - begin)/CLOCKS_PER_SEC;
    
	}
	printf("Time in ms is %lf \n",time_spent/1000);

    

    return 0;
}
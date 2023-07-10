
import numpy as np
import random

zetas = [-1044, -758, -359, -1517, 1493, 1422, 287, 202,
         -171, 622, 1577, 182, 962, -1202, -1474, 1468,
         573, -1325, 264, 383, -829, 1458, -1602, -130,
         -681, 1017, 732, 608, -1542, 411, -205, -1571,
         1223, 652, -552, 1015, -1293, 1491, -282, -1544,
         516, -8, -320, -666, -1618, -1162, 126, 1469,
         -853, -90, -271, 830, 107, -1421, -247, -951,
         -398, 961, -1508, -725, 448, -1065, 677, -1275,
         -1103, 430, 555, 843, -1251, 871, 1550, 105,
         422, 587, 177, -235, -291, -460, 1574, 1653,
         -246, 778, 1159, -147, -777, 1483, -602, 1119,
         -1590, 644, -872, 349, 418, 329, -156, -75,
         817, 1097, 603, 610, 1322, -1285, -1465, 384,
         -1215, -136, 1218, -1335, -874, 220, -1187, -1659,
         -1185, -1530, -1278, 794, -1510, -854, -870, 478,
         -108, -308, 996, 991, 958, -1460, 1522, 1628]

# QINV = np.int16(-3327)
# KYBER_Q = np.int16(3329)
QINV = -3327
KYBER_Q = 3329
new_zetas = np.ones((256, 7), dtype=np.int32)


def montgomery_reduce(a):
    t = np.int16(a * QINV)
    t = np.int32(np.int32(a) - np.int32(t * KYBER_Q) >> 16)
    t = np.int16(t)
    return t


def zeta_init():
    k = 1
    len_ = 128
    col = 0
    while len_ >= 2:
        start = 0
        row = 1
        while start < 256:
            zeta = zetas[k]
            k += 1
            j = start
            while j < start + len_:
                j += 1
                new_zetas[row, col] = np.int32(zeta)
                row += 2
            start = j + len_
        len_ >>= 1
        col += 1


def ntt(r):
    k = 1
    len_ = 128
    while len_ >= 2:
        start = 0
        while start < 256:
            zeta = zetas[k]
            k += 1
            j = start
            while j < start + len_:
                t = montgomery_reduce(np.int32(zeta * np.int16(r[j + len_])))
                r[j + len_] = np.int16(r[j] - t)
                r[j] = np.int16(r[j] + t)
                j += 1
            start = j + len_
        len_ >>= 1

    return r


# poly = np.random.randint(low=0, high=(2**16)-1, size=256)
poly = [-1044, -758, -359, -1517, 1493, 1422, 287, 202,
        -171, 622, 1577, 182, 962, -1202, -1474, 1468,
        573, -1325, 264, 383, -829, 1458, -1602, -130,
        -681, 1017, 732, 608, -1542, 411, -205, -1571,
        1223, 652, -552, 1015, -1293, 1491, -282, -1544,
        516, -8, -320, -666, -1618, -1162, 126, 1469,
        -853, -90, -271, 830, 107, -1421, -247, -951,
        -398, 961, -1508, -725, 448, -1065, 677, -1275,
        -1103, 430, 555, 843, -1251, 871, 1550, 105,
        422, 587, 177, -235, -291, -460, 1574, 1653,
        -246, 778, 1159, -147, -777, 1483, -602, 1119,
        -1590, 644, -872, 349, 418, 329, -156, -75,
        817, 1097, 603, 610, 1322, -1285, -1465, 384,
        -1215, -136, 1218, -1335, -874, 220, -1187, -1659,
        -1185, -1530, -1278, 794, -1510, -854, -870, 478,
        -108, -308, 996, 991, 958, -1460, 1522, 1628,
        -1044, -758, -359, -1517, 1493, 1422, 287, 202,
        -171, 622, 1577, 182, 962, -1202, -1474, 1468,
        573, -1325, 264, 383, -829, 1458, -1602, -130,
        -681, 1017, 732, 608, -1542, 411, -205, -1571,
        1223, 652, -552, 1015, -1293, 1491, -282, -1544,
        516, -8, -320, -666, -1618, -1162, 126, 1469,
        -853, -90, -271, 830, 107, -1421, -247, -951,
        -398, 961, -1508, -725, 448, -1065, 677, -1275,
        -1103, 430, 555, 843, -1251, 871, 1550, 105,
        422, 587, 177, -235, -291, -460, 1574, 1653,
        -246, 778, 1159, -147, -777, 1483, -602, 1119,
        -1590, 644, -872, 349, 418, 329, -156, -75,
        817, 1097, 603, 610, 1322, -1285, -1465, 384,
        -1215, -136, 1218, -1335, -874, 220, -1187, -1659,
        -1185, -1530, -1278, 794, -1510, -854, -870, 478,
        -108, -308, 996, 991, 958, -1460, 1522, 1628]
# print(poly[128])
import time
from numba import njit
import cProfile

zeta_init()
# st = time.perf_counter()
# r = ntt(poly)
# et = time.perf_counter()
# res = et - st
# final_res = res * 1000
# # print(new_zetas)
# print('Execution time:', final_res, 'milliseconds')
# # print(r)
# # print((-758*-1044) % KYBER_Q)
# res = 0
# for i in range(0, 1000):
#     poly = np.random.randint(low=0, high=(2 ** 16) - 1, size=256)
#     st = time.time()
#     r_new = ntt(poly)
#     et = time.time()
#     res += et - st
#
# print('Execution time:', res, 'milliseconds')

# poly2 = np.array([-1044, -758, -359, -1517, 1493, 1422, 287, 202,
#                   -171, 622, 1577, 182, 962, -1202, -1474, 1468,
#                   573, -1325, 264, 383, -829, 1458, -1602, -130,
#                   -681, 1017, 732, 608, -1542, 411, -205, -1571,
#                   1223, 652, -552, 1015, -1293, 1491, -282, -1544,
#                   516, -8, -320, -666, -1618, -1162, 126, 1469,
#                   -853, -90, -271, 830, 107, -1421, -247, -951,
#                   -398, 961, -1508, -725, 448, -1065, 677, -1275,
#                   -1103, 430, 555, 843, -1251, 871, 1550, 105,
#                   422, 587, 177, -235, -291, -460, 1574, 1653,
#                   -246, 778, 1159, -147, -777, 1483, -602, 1119,
#                   -1590, 644, -872, 349, 418, 329, -156, -75,
#                   817, 1097, 603, 610, 1322, -1285, -1465, 384,
#                   -1215, -136, 1218, -1335, -874, 220, -1187, -1659,
#                   -1185, -1530, -1278, 794, -1510, -854, -870, 478,
#                   -108, -308, 996, 991, 958, -1460, 1522, 1628,
#                   -1044, -758, -359, -1517, 1493, 1422, 287, 202,
#                   -171, 622, 1577, 182, 962, -1202, -1474, 1468,
#                   573, -1325, 264, 383, -829, 1458, -1602, -130,
#                   -681, 1017, 732, 608, -1542, 411, -205, -1571,
#                   1223, 652, -552, 1015, -1293, 1491, -282, -1544,
#                   516, -8, -320, -666, -1618, -1162, 126, 1469,
#                   -853, -90, -271, 830, 107, -1421, -247, -951,
#                   -398, 961, -1508, -725, 448, -1065, 677, -1275,
#                   -1103, 430, 555, 843, -1251, 871, 1550, 105,
#                   422, 587, 177, -235, -291, -460, 1574, 1653,
#                   -246, 778, 1159, -147, -777, 1483, -602, 1119,
#                   -1590, 644, -872, 349, 418, 329, -156, -75,
#                   817, 1097, 603, 610, 1322, -1285, -1465, 384,
#                   -1215, -136, 1218, -1335, -874, 220, -1187, -1659,
#                   -1185, -1530, -1278, 794, -1510, -854, -870, 478,
#                   -108, -308, 996, 991, 958, -1460, 1522, 1628])



@njit
def montgomery_reduce_new(a):
    a = np.int32(a)
    t = (a * QINV)
    t = ((a - t * KYBER_Q) >> 16)
    return np.int16(t)




@njit(parallel=True)
def ntt_new(r):
    len_ = 128
    cnt = 0
    while len_ >= 2:
        start = 0
        a = np.multiply(new_zetas[:, cnt], r)
        while start < 256:
            j = start
            while j < start + len_:
                # t = r[j + len_]
                t = montgomery_reduce_new(a[j + len_])
                r[j + len_] = np.int16(r[j] - t)
                r[j] = np.int16(r[j] + t)
                j += 1
            start = j + len_
        len_ >>= 1
        cnt += 1

    return r

poly = np.random.randint(low=0, high=(2 ** 16) - 1, size=256)

r_new = ntt_new(poly)
# res = 0
# st = time.perf_counter()
# r_new = ntt_new(poly2)
# et = time.perf_counter()
# res = et - st
# final_res = res * 1000
# print('Execution time1:', final_res, 'milliseconds')
# print(r)
#
#
# st = time.perf_counter()
# r_new2 = ntt_new(r_new)
# et = time.perf_counter()
# res2 = et - st
# final_res = res2 * 1000
# print('Execution time1:', final_res, 'milliseconds')
# print(r_new2)

res = 0
for i in range(0, 1000000):
    poly2 = np.random.randint(low=0, high=(2 ** 16) - 1, size=256)
    st = time.perf_counter()
    r_new = ntt_new(poly2)
    et = time.perf_counter()
    res += et - st

print('Execution time2:', res/1000, 'milliseconds')

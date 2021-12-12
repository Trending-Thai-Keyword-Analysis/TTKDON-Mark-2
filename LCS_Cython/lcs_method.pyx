# distutils: language=c++
from libc.string cimport strlen, strcmp
from libc.stdlib cimport malloc, free
from libc.stdio cimport printf

from collections import Counter
from tqdm.auto import tqdm
tqdm.pandas()

cdef extern from "Python.h":
    const char* PyUnicode_AsUTF8(object unicode)
    object PyUnicode_DecodeUTF8(const char* utf8string, Py_ssize_t size, const char *errors)

cdef const char ** to_cstring_array(list_str, int length):
    cdef const char **ret = <const char **>malloc(length * sizeof(char *))
    for i in xrange(length):
        ret[i] = PyUnicode_AsUTF8(list_str[i])
    return ret

cpdef lcs_algo(S1, S2, int m, int n):
    cdef int i = 0
    cdef int j = 0
    cdef int k = 0
    cdef int len = 0
    cdef int *L = <int *>malloc(((m+1) * (n+1)) * sizeof(int))
    for i in range((m+1) * (n+1)):
        L[i] = 0
    cdef const char **c_arr1 = to_cstring_array(S1,m)
    cdef const char **c_arr2 = to_cstring_array(S2,n)

    result = []
    i = 1

    try:
        for i in range(1,m+1):
            j = 1
            for j in range(1,n+1):
                if strcmp(c_arr1[i-1],c_arr2[j-1]) == 0:
                    L[i*(n+1) + j] = L[i*(n+1) + j - n - 2] + 1
                    if len < L[i*(n+1) + j]:
                        if 2 < L[i*(n+1) + j] < 9:
                            len = L[i*(n+1) + j]
                            result = []
                            k = 0
                            LCS = ""
                            for k in range(len):
                                LCS = PyUnicode_DecodeUTF8(c_arr1[i-1-k],strlen(c_arr1[i-1-k]),"surrogateescape") + LCS
                            if LCS not in result:
                                result.append(LCS)
                    elif len == L[i*(n+1) + j]:
                        k = 0
                        LCS = ""
                        for k in range(len):
                            LCS = PyUnicode_DecodeUTF8(c_arr1[i-1-k],strlen(c_arr1[i-1-k]),"surrogateescape") + LCS
                        if LCS not in result:
                            result.append(LCS)

        return result,len
    finally:
        free(L)
        free(c_arr1)
        free(c_arr2)

cpdef find_lcs(atta_list, newmm_list):
    cdef int l = <int>len(atta_list)
    cdef int i, j, len_w1_atta, len_w2_atta, maxl_atta, len_w1_newmm, len_w2_newmm, maxl_newmm
    lcs_atta = []
    lcs_newmm = []
    for i in tqdm(range(l-1)):
        j = i + 1
        w1_atta, w1_newmm = atta_list[i], newmm_list[i]
        len_w1_atta, len_w1_newmm = <int>len(w1_atta), <int>len(w1_newmm)
        for j in range(i+1,l):
            w2_atta, w2_newmm = atta_list[j], newmm_list[j]
            len_w2_atta, len_w2_newmm = <int>len(w2_atta), <int>len(w2_newmm)
            lcs_atta_list,maxl_atta = [],0
            lcs_newmm_list,maxl_newmm = [],0
            if i != j:
                lcs_atta_list,maxl_atta = lcs_algo(w1_atta,w2_atta,len_w1_atta,len_w2_atta)
                lcs_newmm_list,maxl_newmm = lcs_algo(w1_newmm,w2_newmm,len_w1_newmm,len_w2_newmm)
                if lcs_atta_list != []:
                    lcs_atta.extend(lcs_atta_list)
                if lcs_newmm_list != []:
                    lcs_newmm.extend(lcs_newmm_list)

    lcs_atta_counter = Counter(lcs_atta)
    lcs_newmm_counter = Counter(lcs_newmm)
    return lcs_atta_counter, lcs_newmm_counter
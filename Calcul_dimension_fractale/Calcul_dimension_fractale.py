import os.path
import sys
import numpy as np
import math

def Import_dessinBitmap(file):
    array = np.load(file + '.npy')
    return array.tolist()
    # return array


def Afficher_Array(y):
    space = ' '  # <--- Pour modifier les espaces
    N1=len(y)
    for i in range(N1):
        N2=len(y[i])
        for j in range(N2):
            if y[i][j]:
                print(str(y[i][j]), end=space)
            else:
                print(' ', end=space)
        print("")


def Dim(Count, Size):
    return np.log(Count) / np.log(Size)


def Calcul_dim(y, n=0):
    L = 2 ** n
    dim = 1
    
    N1 = len(y)
    for i in range(0, N1, L):
        N2 = len(y[i])
        for j in range(0, N2, L):
            Trouver = False
            for i2 in range(i, i+L):
                for j2 in range(j, j+L):
                    if y[i2][j2] == 1.0 and i2 != (N1-1) and not(Trouver):
                        dim += 1
                        Trouver = True
    return Dim(dim, N1//L)
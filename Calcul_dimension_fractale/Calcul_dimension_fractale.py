import os.path
import sys
import glob
import numpy as np
import math

def Import_dessinBitmap(file):
    array = np.load(file)
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

def Calcul_Dossier(folder=".\\", n=0):
    npy_list = [f for f in glob.glob(folder + "*.npy")]
    S=[]

    for i in range(len(npy_list)):
        file=npy_list[i]
        y = Import_dessinBitmap(file)
        dim = Calcul_dim(y, n)
        print(str(i+1) + "\t" + file + " :\t" + str(dim))
        S.append(dim)

    print("\n---")
    N = len(S)
    Moyenne = 0
    Ecart = 0
    for i in S:
        Moyenne += i
        Ecart += i ** 2
    Moyenne = Moyenne / N
    Ecart = math.sqrt((Ecart / N - Moyenne ** 2) * N / (N - 1))
    print("Moyenne :\t\t" + str(Moyenne))
    print("Ecart type empirique :\t" + str(Ecart))
    
    return (Moyenne, Ecart)

def main(folder=".", n=0):
    # folder_list = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, d))]
    folder_list = [f for f in glob.glob(folder + "\\*\\")]

    Resultat = []
    for dossier in folder_list:
        print("\t--- " + dossier + " ---")
        Resultat.append(Calcul_Dossier(dossier))
        print("")
        print("")
    return Resultat

main("..\\Image")
# input()
import os.path
import sys
import glob
import numpy as np
import math
import matplotlib.pyplot as plt


def Import_dessinBitmap(file):
    array = np.load(file)
    return array.tolist()


def Afficher_Array(y):
    space = ' '  # <--- Pour modifier les espaces
    N1 = len(y)
    for i in range(N1):
        N2 = len(y[i])
        for j in range(N2):
            if y[i][j]:
                print(str(y[i][j]), end=space)
            else:
                print(' ', end=space)
        print("")


def Print_plt(Mat, fichier, rep=".\\", afficher=False, save=True):
    x = []
    y = []
    c = "blue"                    # <--- Couleur des icones
    mk = "o"                      # <--- Motifs des icones ("o", "x", "1")
    size = 30                     # <--- Taille des icones
    N1 = len(Mat)
    for i in range(1, N1 - 1):
        N2 = len(Mat[i])
        for j in range(1, N2-1):
            if Mat[i][j]:
                x.append(j)
                y.append(N1-i)
    plt.scatter(x, y, color=c, label=fichier, s=size, marker=mk)
    plt.title("Simulation de foudre")
    plt.legend(loc='upper left')
    plt.axis([0, N1, 0, N2])
    if save:
        plt.savefig(rep+fichier+".png")
    if afficher:
        plt.show()
    plt.close()

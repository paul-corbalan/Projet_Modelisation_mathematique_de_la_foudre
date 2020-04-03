#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
 
import sys 
import random 
import matplotlib.pyplot as plt 
import numpy as np 
import math as m 
from datetime import datetime 
 
# précalcul du potentiel qui est linéaire 
RAPINIT = True 
# sous partie à mettre à jour à un nouveau pixel de taille 2S+1x2S+1 
S = 10 
MAJPETITE = False 
 
if len(sys.argv) != 3: 
    N = 64 
    eta = 6 
else: 
    # dimension de la grille NxN 
    N=int(sys.argv[1]) 
    # paramètre de croissance de la structure 
    eta=float(sys.argv[2]) 
 
partMax = 50000 
 
def init(): 
    # ligne du bas en charge positives et trois charges supperposées en haut au milieu 
    # ligne du bas en charge positives et ligne du haut en charges négatives (nuage) 
    for i in range(N): 
        condInitBitmap[i][N-1] = 1 
        potentielsBitmap[i][N-1] = 1 
        dessinBitmap[N-1][i] = 1 
    for i in range(N): 
        condInitBitmap[i][0] = -1 
        potentielsBitmap[i][0] = 0 
        dessinBitmap[0][i] = 0.5 
    if RAPINIT: 
        # calcul analytique initial du potentiel entre deux plaques: potentiel linéaire en y 
        for j in range(1,N-1): 
            pot = 0.0+j*1.0/(N-1) 
            for i in range(N): 
                potentielsBitmap[i][j] = pot 

# paramètre de relaxation pour accélérer la convergence 
omega = 1.6 
 
def majPotentielRapide(i,j): 
    delta = 0.0 
    nb = 1 
    if abs(condInitBitmap[i][j]) != 1: 
        if i == 0: 
            delta = potentielsBitmap[i+1][j] + potentielsBitmap[i][j-1] + potentielsBitmap[i][j+1] - 3 * potentielsBitmap[i][j] 
            nb = 3 
        elif i == N-1: 
            nb = 3 
            delta = potentielsBitmap[i-1][j] + potentielsBitmap[i][j-1] + potentielsBitmap[i][j+1] - 3 * potentielsBitmap[i][j] 
        else: 
            delta = potentielsBitmap[i-1][j] + potentielsBitmap[i+1][j] + potentielsBitmap[i][j-1] + potentielsBitmap[i][j+1] - 4 * potentielsBitmap[i][j] 
            nb = 4 
             # on ne met à jour que les points qui ne sont pas des contraintes initiales ou qui ne continnent pas des charges 
            potentielsBitmap[i][j] = potentielsBitmap[i][j] + omega * delta / nb 
        return abs(delta/potentielsBitmap[i][j]/nb) 
    else:
        return 0.0 

def majPotentielsSousBitmapRapide(x,y,k): 
    # mise à jour de la sous partie centrée sur x,y de taille 2k+1 x 2k+1 
    maxdelta = 0 
    # parcours de bas en haut et de gauche à droite 
    # il ne faut pas dépasser le bord: on s'arrête avant 
    Ix = max(0,x-k) 
    Sx = min(N-1,x+k) 
    Iy = max(0,y-k) 
    Sy = min(N-1,y+k) 
    # N-1 à 0 
    for j in range(Sy,Iy-1,-1): 
        for i in range(Ix,Sx+1): 
            delta = majPotentielRapide(i,j) 
            if delta > maxdelta: 
                maxdelta = delta 
    return maxdelta 
 
def majPotentielsBitmapRapide(): 
    maxdelta = 0.0 
    # parcours de bas en haut et de gauche à droite 
    # N-1 à 0 
    for j in range(N-1,-1,-1): 
        # 0 à N-1 
        for i in range(N): 
            delta = majPotentielRapide(i,j) 
            if delta > maxdelta: 
                maxdelta = delta 
    return maxdelta 
 
def estValide(xy, bitmap): 
    # valide si qu'un seul voisin dessiné de xy dans bitmap 
    if bitmap[xy[0]+1][xy[1]] + bitmap[xy[0]-1][xy[1]] + bitmap[xy[0]][xy[1]+1] + bitmap[xy[0]][xy[1]-1] + bitmap[xy[0]+1][xy[1]+1] + bitmap[xy[0]-1][xy[1]+1] + bitmap[xy[0]+1][xy[1]-1] + bitmap[xy[0]-1][xy[1]-1] == 1: 
        return True 
    return False 
 
def sontAcotes(pt1,pt2): 
    if (abs(pt1[0] - pt2[0]) <= 1) and (abs(pt1[1] - pt2[1]) <= 1): 
        return True 
    return False 
 
def pasAcoteCroissance(pt, pixelsCroissance):
    for c in range(len(pixelsCroissance)): 
        if sontAcotes(pt, pixelsCroissance[c]): 
            return False 
    return True 
 
def eliminePixelsPres(pt, pixelsCroissance, potentielsCroissance): 
    for c in range(len(pixelsCroissance) - 1, -1, -1): 
        if sontAcotes(pt, pixelsCroissance[c]): 
            pixelsCroissance.pop(c) 
            potentielsCroissance.pop(c) 
    return None 
 
def estDansCroissance(pt, pixelsCroissance): 
    for c in range(len(pixelsCroissance)): 
        if pixelsCroissance[c] == pt: 
            return True 
    return False 
 
def croissanceRapide(nouv, pixelsBitmap, pixelsCroissance, potantielsCroissance): 
    # ajoute les pixels adjacents a nouv qui ne sont pas dans pixelsCroissance 
    candidats = [[nouv[0] + 1, nouv[1]], [nouv[0] - 1, nouv[1]], [nouv[0], nouv[1] + 1], [nouv[0], nouv[1] - 1], [nouv[0] + 1, nouv[1] + 1], [nouv[0] + 1, nouv[1] - 1], [nouv[0] - 1, nouv[1] + 1], [nouv[0] - 1, nouv[1] - 1], ] 
    for c in range(len(candidats)): 
        # si le candidat a qu'un seul voisin et n'est pas déjà un point dessiné et qu'il est pas en bordure supérieure 
        if estValide(candidats[c], pixelsBitmap) and (pixelsBitmap[candidats[c][0]][candidats[c][1]] == 0) and (candidats[c][1] > 0): 
 
            pixelsCroissance.append(candidats[c]) 
             
            potentielsCroissance.append(potentielsBitmap[candidats[c][0]][candidats[c][1]]) 
 
def choix(pixelsCroissance, potentielsCroissance): 
    choixPotentiel = random.uniform(0, 1) 
    PotentielTotalEta = 0 
    pTotal = [] 
    sommePTotal = 0 
    for i in range(len(potentielsCroissance)): 
        PotentielTotalEta += pow(potentielsCroissance[i], eta) 
    for i in range(len(pixelsCroissance)): 
        pi = pow(potentielsCroissance[i], eta) / PotentielTotalEta 
        sommePTotal += pi 
        pTotal.append(sommePTotal) 
    for i in range(len(pTotal)): 
        if pTotal[i] > choixPotentiel: 
            choixFinal = pixelsCroissance[i] 
            return([choixFinal, i]) 

def majPotentielsCroissance(pixelsCroissance, potentielsCroissance, nbPart): 
    # mise a jour des potentiels de la liste complête 
    for c in range(len(pixelsCroissance)): 
        potentielsCroissance[c] = potentielsBitmap[pixelsCroissance[c][0]][pixelsCroissance[c][1]] 
 
def main(pixelsBitmap, pixelsCroissance, potentielsCroissance, nbPart): 
    run = True 
    init() 
    # graine: début de décharge en haut au milieu 
    graine = [int(N / 2), 1] 
    nouv = graine 
    pixelsBitmap[nouv[0]][nouv[1]] = 1 
    dessinBitmap[nouv[1]][nouv[0]] = 1 
    condInitBitmap[nouv[0]][nouv[1]] = -1 
    potentielsBitmap[nouv[0]][nouv[1]] = 0 
    nbPart = 1 
    while run == True: 
        # elimine les pixelsCroissance qui sont proche de nouv 
        eliminePixelsPres(nouv, pixelsCroissance, potentielsCroissance) 
        # mise à jour de la carte des potentiels 
        maxdelta = 1 
        # condition d'arrêt à MAXDELTA du max des mises à jour des potentiels relatifs 
        cf = 0 
        if MAJPETITE: 
            while maxdelta > MAXDELTA: 
                maxdelta = majPotentielsSousBitmapRapide(nouv[0], nouv[1], S) 
                cf += 1 
        maxdelta = 1 
        cs = 0 
        while maxdelta > MAXDELTA and cs<200: 
            maxdelta = majPotentielsBitmapRapide() 
            #print(cs, " : ", maxdelta)
            cs += 1 
        # définition des nouveaux sites de croissance potentiels 
        croissanceRapide(nouv, pixelsBitmap, pixelsCroissance, potentielsCroissance) 
        # mise à jour des potentiels des candidats à la croissance 
        majPotentielsCroissance(pixelsCroissance, potentielsCroissance, nbPart) 
        res = choix(pixelsCroissance, potentielsCroissance) 
        nouv = res[0] 
        # le point choisi est elimine des croissances possibles 
        pixelsCroissance.pop(res[1]) 
        potentielsCroissance.pop(res[1]) 
            # le point choisi est dessine 
        pixelsBitmap[nouv[0]][nouv[1]] = 1 
        dessinBitmap[nouv[1]][nouv[0]] = 1 
        # le point choisi devient une contrainte à potentiel nul 
        condInitBitmap[nouv[0]][nouv[1]] = -1 
        potentielsBitmap[nouv[0]][nouv[1]] = 0 
        nbPart += 1 
        if nouv[0] == 0 or nouv[0] == N-1 or nouv[1] == N-2 or nbPart > partMax : 
            run = False 
 
    print("N=", N, "eta=", eta, "nbpart=", nbPart, "MAXDELTA=", MAXDELTA)
    return nbPart
 

# Partie rajoutée


def Save_txt(y, N, fichier):
    space=''                    # <--- Pour modifier les espaces
    f=open(fichier + ".txt","a")
    for i in range(N):
        for j in range(N):
            if y[i][j]:
                print('#', end=space, file=f)
            else:
                print(' ', end=space, file=f)
        print("", file=f)
    f.close()

def Print_plt(Mat, N, eta, nbPart, fichier, afficher=False):
    x = []
    y = []
    c="blue"                    # <--- Couleur des icones
    mk="o"                      # <--- Motifs des icones ("o", "x", "1")
    size=30                     # <--- Taille des icones
    for i in range(1, N-1):
        for j in range(1, N-1):
            if Mat[i][j]:
                x.append(j)
                y.append(N-i)
    plt.scatter(x, y, color=c,  s=size, marker=mk)
    # title="N="+str(N)+" eta="+str(eta)+" nbpart="+str(nbPart)+" MAXDELTA="+str(MAXDELTA)
    plt.title("N="+str(N)+" eta="+str(eta)+" nbpart="+str(nbPart)+" MAXDELTA="+str(MAXDELTA))
    # plt.legend(loc='upper left')
    plt.axis([0,N,0,N])
    plt.savefig(fichier+".png")
    if afficher:
        plt.show()
    plt.close()


eta = 6
# [64, 128, 256, 512]
for N in [64, 128, 256, 512]:
    # MAXDELTA = MAXDELTA/1000.0
    # [1, 0.1, 0.05, 0.017, 0.01, 0.005, 0.001, 0.0005, 0.0001]
    for MAXDELTA in [0.001, 0.0005, 0.0001]:

        for i in range(50):
            nbPart = 1
            dossier = "..\\Image\\"+"eta="+str(eta)+" N="+str(N)+" MAXDELTA="+str(MAXDELTA)+"\\"
            
            # la grille est de NxN mais en réalite la mesure d'une unité h est 1/N 
            pixelsBitmap = [[0 for j in range(N)] for i in range(N)] 
            # que pour le dessin pour éviter la transposition 
            dessinBitmap = [[0 for j in range(N)] for i in range(N)] 
            # conditions initiales -1 charge négative ou 1 charge positive ou 0 non defini sera mis à jour pendant le programme avec les nouvelles charges 
            condInitBitmap = [[0 for j in range(N)] for i in range(N)] 
            potentielsBitmap = [[0.0 for j in range(N)] for i in range(N)] 
            pixelsCroissance = [] 
            potentielsCroissance = [] 

            nbPart=main(pixelsBitmap, pixelsCroissance, potentielsCroissance, nbPart) 
            
            # fichier = "foudre-"+str(N)+"-"+str(eta)+"-"+str(MAXDELTA)+"-"+str(nbPart)+"-"+datetime.now().strftime("%Y%m%d%H%M%S")

            # eta=6 N=128 MAXDELTA=0,0001

            fichier = dossier+"foudre-"+str(N)+"-"+str(eta)+"-"+str(MAXDELTA)+"-"+str(nbPart)+"-"+datetime.now().strftime("%Y%m%d%H%M%S")
            np.save(fichier,np.array(dessinBitmap)) 
            Save_txt(np.array(dessinBitmap), N, fichier)
            Print_plt(np.array(dessinBitmap), N, eta, nbPart, fichier)
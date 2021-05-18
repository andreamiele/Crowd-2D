#%%
#           IMPORTATIONS


import numpy as np
import matplotlib.pyplot as plt
from math import *



##          EXEMPLE

mat=np.array([[(0,1) for i in range(200)]]+[[(0,1)]+[(0,2) for i in range(198)]+[(0,1)] for j in range(198)]+[[(0,1) for i in range(200)]]) 

#Remarque de compréhension générale :
    #   1:      Limite 
    #   2:      Non calculé 
    #   3:      Calculé 
    #   4:      Considéré (mais non encore accepté)
    
for i in range(150):
    for j in range(95,100):
        mat[(i,j)]=(0,1)
for i in range(95,100):
    for j in range(70):
        mat[(i,j)]=(0,1)
        
        
#%% 
#               VOISINNAGE
#                   (On conserve ceux qui sont non calculés ou considérés)

def voisinnage(M,c):
    a,b=c
    res=[]
    if M[(a-1,b)][1]!=1 and M[(a-1,b)][1]!=3:
        res.append((a-1,b))
    if M[(a+1,b)][1]!=1 and M[(a+1,b)][1]!=3:
        res.append((a+1,b))
    if M[(a,b-1)][1]!=1 and M[(a,b-1)][1]!=3:
        res.append((a,b-1))
    if M[(a,b+1)][1]!=1 and M[(a,b+1)][1]!=3:
        res.append((a,b+1))
    return(res)

#%% 
#               DISTANCE
    
    
def calcul_distance(M,c,pepins):
    a,b=c
    test=0
    if M[(a-1,b)][1]==3:        #Calculé en a-1,b
        if M[(a+1,b)][1]==3:    # + Calculé en a+1,b
            x=min(M[(a-1,b)][0],M[(a+1,b)][0])
        else:
            x=M[(a-1,b)][0]     #Non calculé en a+1,b
    elif M[(a+1,b)][1]==3:      #Non calculé en a-1,b mais a+1,b oui
        x=M[(a+1,b)][0]
    else:                       #Non calculé en a-1,b ni en a+1,b
        x=0
        test=2
    if M[(a,b-1)][1]==3:        #Calculé en a,b-1
        if M[(a,b+1)][1]==3:    # + Calculé en a,b-1
            y=min(M[(a,b-1)][0],M[(a,b+1)][0])
        else:
            y=M[(a,b-1)][0]     #Non calculé en a,b+1
    elif M[(a,b+1)][1]==3:      #Non calculé en a,b-1 mais a,b+1 oui
        y=M[(a,b+1)][0]
    else:                       #Non calculé en a,b-1 ni en a,b+1
        y=0
        test=1
    if test==0:                 #Si on en a au moins 2 de calculé
        if (x-y)*(x-y)>2:       #Problème sous la racine
            pepins+=1           #On a un soucis 
            if x<y:             #On regarde la distance la plus petite
                d=1+x
            else:
                d=1+y
        else:
            d=(x+y+sqrt(2-(x-y)*(x-y)))/2   #On peut calculer avec la formule souhaitée
    elif test==1:
        d=1+x
    else:
        d=1+y
    return(d,pepins)

#%%
##              FONCTIONS DE GESTION DU TAS


def remonter(t,i,pos):                          #Fonction remonter dans un tas
    if i//2!=0 and t[i//2][0]>t[i][0]:
        t[i//2],t[i]=t[i],t[i//2]
        pos[t[i][1]],pos[t[i//2][1]]=pos[t[i//2][1]],pos[t[i][1]]
        remonter(t,i//2,pos)

def inserer(tas,v,d,pos):                       #Fonction insertion dans un tas
    n=tas[0]
    pos[v]=n+1
    if n+1==len(tas):
        tas.append((d,v))
    else:
        tas[n+1]=(d,v)
    remonter(tas,n+1,pos)

def descendre(t,i,n,pos):                       #Fonction descendre dans un tas
    if 2*i+1<n:
        if t[i][0]>t[2*i][0]:
            if t[2*i][0]<t[2*i+1][0]:
                t[i],t[2*i]=t[2*i],t[i]
                pos[t[i][1]],pos[t[2*i][1]]=pos[t[2*i][1]],pos[t[i][1]]
                descendre(t,2*i,n,pos)
            else:
                t[i],t[2*i+1]=t[2*i+1],t[i]
                pos[t[i][1]],pos[t[2*i+1][1]]=pos[t[2*i+1][1]],pos[t[i][1]]
                descendre(t,2*i+1,n,pos)
        elif t[i][0]>t[2*i+1][0]:
            t[i],t[2*i+1]=t[2*i+1],t[i]
            pos[t[i][1]],pos[t[2*i+1][1]]=pos[t[2*i+1][1]],pos[t[i][1]]
            descendre(t,2*i+1,n,pos)
    elif 2*i==n:
        if t[i][0]>t[2*i][0]:
            t[i],t[2*i]=t[2*i],t[i]
            pos[t[i][1]],pos[t[2*i][1]]=pos[t[2*i][1]],pos[t[i][1]]

#%%
#               FONCTION PRINCIPALE : 
#                    Création de la carte des distances (sur une matrice)

def carte_distance(M,sortie):
    pepins=0
    d=42
    f,g,h=np.shape(M)
    position=np.zeros((f,g),dtype=int)
    for c in sortie:
        M[c]=(0,3)
    tas=[0]
    for c in sortie:
        for v in voisinnage(M,c):
            d,pepins=calcul_distance(M,v,pepins)
            if M[v][1]==2:
                inserer(tas,v,d,position)
                tas[0]+=1
                M[v]=(d,4)
            elif d<M[v][0]:
                i=position[v]
                a,b=tas[i]
                tas[i]=(d,b)
                remonter(tas,i,position)
                M[v][0]=d
    while tas[0]!=0:
        n=tas[0]
        d,c=tas[1]
        tas[1]=tas[n]
        position[tas[1][1]]=1
        tas[0]-=1
        descendre(tas,1,n-1,position)
        M[c]=(d,3)
        for v in voisinnage(M,c):
            d,pepins=calcul_distance(M,v,pepins)
            if M[v][1]==2:
                inserer(tas,v,d,position)
                tas[0]+=1
                M[v]=(d,4)
            elif d<M[v][0]:
                i=position[v]
                a,b=tas[i]
                tas[i]=(d,b)
                remonter(tas,i,position)
                M[v][0]=d
    print(pepins)
    return(M,d)
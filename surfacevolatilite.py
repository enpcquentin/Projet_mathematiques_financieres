# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 14:28:32 2017

@author: qduch
"""
from blackscholes import *
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


S0=100;
r=5/100;
ls_T=[0.1,.25 ,.5,.75,1.]
ls_K=[90 ,95 ,100 ,105 ,110]
ls_prix = [[] for i in range(len(ls_K))]


localvol = []

for i in range(len(ls_K)):
    for j in range(len(ls_T)):
        localvol.append(min([0.2+5*np.log(100./ls_K[i])**2+0.1*np.exp(-(ls_T[j])), 0.6]))
        ls_prix[i].append(BlackScholes("Call",S0,ls_K[i],r,localvol[i],ls_T[j]))

ls_prix = np.array(ls_prix)
        
liste_sigma = [[] for i in range(len(ls_K))]
for i in range(len(ls_K)):
    for j in range(len(ls_T)):
        liste_sigma[i].append(dicho("Call",S0, ls_K[i], r, ls_T[j], 0.5, 0, np.sqrt(0.25), 0.01, 0.6, ls_prix[i,j]))

liste_sigma = np.array(liste_sigma)
ls_T = np.array(ls_T)
ls_K = np.array(ls_K)

ax = Axes3D(plt.figure())


ls_T,ls_K = np.meshgrid(ls_T,ls_K)

Gx, Gy = np.gradient(liste_sigma) # gradients with respect to x and y
G = (Gx**2+Gy**2)**.5  # gradient magnitude
N = G/G.max()  # normalize 0..1
#ax.plot_wireframe(ls_T,ls_K,liste_sigma, rstride=1, cstride=1)

ax.plot_surface(ls_T,ls_K,liste_sigma, rstride=1, cstride=1, facecolors=cm.jet(N), linewidth=0, antialiased=False, shade=False)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.title("Surface de volatilité")


ax.view_init(17, 30)

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 17:10:41 2017

@author: qduch
"""

##### Modèles d'actifs avec "sauts gaussiens" (question 2 exercice 47 p 189)


from blackscholes import *


def saut_gaussien(type,x,K,r,sigma,tau,lamb,moy,ecarttype):
    prix = 0
    # calcul de l'espérance commune des variables aléatoires U_j
    espeU = np.exp(moy + (ecarttype**2) / 2.) - 1
    lambp = lamb*(1 + espeU )
    gamma = moy + (ecarttype**2 )/2.
    factn = 1
    for n in range(40):
        if n!=0:
            factn = factn * n
        rn = r-lamb * espeU + n*gamma/tau
        sigman = np.sqrt(sigma**2 + n*(ecarttype**2)/tau)
        BlackSn = BlackScholes(type,x,K,rn,sigman,tau)
        prix = prix + (np.exp(-lambp*tau)*( (lambp*tau)**n ) / factn) * BlackSn
    return (prix)
    

    # Code pour tracer le smile de volatilité
    
def dicho(type,x,K,r,tau,lamb,moy,ecarttype,sg,sd,prix):
    pg = saut_gaussien(type,x,K,r,sg,tau,lamb,moy,ecarttype)
    pd = saut_gaussien(type,x,K,r,sd,tau,lamb,moy,ecarttype)
    epsilon= 10**(-4)
    sm = sg
    while (pd-pg>epsilon):
        sm = (sg+sd)/2
        pm = saut_gaussien(type,x,K,r,sm,tau,lamb,moy,ecarttype)
        if pm>prix:
            sd = sm
            pd = pm
        else:
            sg = sm
            pg = pm
    return sm
    

        #### Etude du smile de volatilite implicite

        
def smile_gaussien():
#S0 = 100
#liste_K= [80, 90, 100 , 110, 120 ]
#liste_prix = [29,20,12,8.5,8]
#r=0.05
#T = 1
#Otype='Call'
#    S0 = 2872
#    liste_K= [2650, 2700, 2750 ,2800 ,2850, 2900, 2950, 3000 ]
#    liste_prix = [233 ,183, 135, 89 ,50 ,24, 9 ,3]
#    r=0.05
#    T = 1
#    Otype='Call'
    S0 = 100;
    r = 5/100;
    liste_K = [0.8*S0 + 0.4*S0*i/float(20) for i in range(20)]
    T = 0.25
    Otype='Call'
    
    
    liste_prix = []
    localvol = []
    for i in range(len(liste_K)):
        localvol.append(min([0.2+5*np.log(100./liste_K[i])**2+0.1*np.exp(-(T)), 0.6]))
        liste_prix.append(BlackScholes("Call",S0,liste_K[i],r,localvol[i],T))
    
    
    liste_sigma = []
    
     
    for i in range(len(liste_K)):
         liste_sigma.append(dicho(Otype,S0, liste_K[i], r, T, 0.5, 0, np.sqrt(0.25), 0.01, 0.6, liste_prix[i]))
             
    plt.plot(liste_K,liste_sigma)
    plt.title('Smile de volatilité pour un modèle de sauts gaussiens')
    plt.show()
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 17:13:22 2017

@author: qduch
"""

##### Modèles d'actifs avec "sauts bernouilli" (question 1 exercice 47 p 189)


from blackscholes import *
    
def saut_bernou(type,x,K,r,sigma,tau,lamb,p,a,b):
    prix = 0
    # calcul de l'espérance commune des variables aléatoires U_j
    factn = 1
    factk = 1
    alpha = np.log(1+a)
    beta = np.log(1+b)
    espU = p*a + (1-p)*b
    for n in range(40):
        if n!=0:
            factn = factn * n
        for k in range(40):
            if k!=0:
                k = factk * k
            xp = x * np.exp(-lamb*tau*espU + alpha*n + beta*k)
            BlackSn = BlackScholes(type,xp,K,r,sigma,tau)
            prix = prix + (np.exp(-lamb*tau)*( (lamb*tau*p)**n ) * ( (lamb*tau*(1-p))**k ) / (factn * factk)) * BlackSn
    return (prix)

    
        
def dicho_bernou(type,x,K,r,tau,lamb,p,a,b,sg,sd,prix):
    pg = saut_bernou(type,x,K,r,sg,tau,lamb,p,a,b)
    pd = saut_bernou(type,x,K,r,sd,tau,lamb,p,a,b)
    epsilon= 10**(-2)
    sm = sg
    while (pd-pg>epsilon):
        sm = (sg+sd)/2
        pm = saut_bernou(type,x,K,r,sm,tau,lamb,p,a,b)
        if pm>prix:
            sd = sm
            pd = pm
        else:
            sg = sm
            pg = pm
    return sm
    
    
    
        #### Etude du smile de volatilite implicite

def smile_bernou():    
#S0 = 100
#liste_K= [70, 80, 90, 100 , 110, 120 ]
#liste_prix = [4,8,15,20,25,30]
#r=0.05
#T = 0.5
#Otype='Call'

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
         liste_sigma.append(dicho_bernou(Otype,S0, liste_K[i], r, T, 0.5, 0.5, 1,2, 0.005, 0.6, liste_prix[i]))
             
    plt.plot(liste_K,liste_sigma)
    plt.title('Smile de volatilité pour des sauts de deux types')
    plt.show()
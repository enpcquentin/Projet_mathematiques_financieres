# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:11:05 2017

@author: quentin duchemin et pierre boyeau
"""


import numpy as np
import scipy.stats as ss
import time 
import matplotlib
import matplotlib.pyplot as plt

##### Black- Scholes

    # tau = T - t

def d1(x,K,r,sigma,tau):
    return (np.log(x/K) + (r + sigma**2 / 2.)*tau)/(sigma * np.sqrt(tau))
 
def d2(x, K, r, sigma, tau):
    return (np.log(x/K) + (r - sigma**2 / 2.)*tau)/(sigma * np.sqrt(tau))
 
def BlackScholes(type,x,K,r,sigma,tau):
    if type=="Call":
        return ( x * ss.norm.cdf(d1(x, K, r, sigma, tau)) - K*np.exp(-r*tau)*ss.norm.cdf(d2(x, K, r, sigma, tau))  )
    else:
        return (K * np.exp(-r*tau)*ss.norm.cdf(-d2(x, K, r, sigma, tau)) - x*ss.norm.cdf(-d1(x, K, r, sigma, tau)) )

def dicho_bs(type,x,K,r,tau,sg,sd,prix):
    pg =  BlackScholes(type,x,K,r,sg,tau)
    pd = BlackScholes(type,x,K,r,sd,tau)
    epsilon= 10**(-2)
    sm = sg
    while (pd-pg>epsilon):
        sm = (sg+sd)/2
        pm = BlackScholes(type,x,K,r,sm,tau)
        if pm>prix:
            sd = sm
            pd = pm
        else:
            sg = sm
            pg = pm
    return sm
    
      
    
    ##### BlackScholes('Call',65.24,65,0.01,0.3955,16)
def test_BS():
    S0 = 102
    K = 100
    r = 0.05
    sigma = 0.25
    T = 2
    Otype='Call'
    
    print ("S0\tstock price at time 0:", S0)
    print ("K\tstrike price:", K)
    print ("r\tcontinuously compounded risk-free rate:", r)
    print ("sigma\tvolatility of the stock price per year:", sigma)
    print ("T\ttime to maturity in trading years:", T)
    
    
    t=time.time()
    c_BS = BlackScholes(Otype,S0, K, r, sigma, T)
    elapsed=time.time()-t
    print ("c_BS\tBlack-Scholes price:", c_BS, elapsed)     



    ### Etude du smile de volatilite implicite

def smile_BS():
    S0 = 2872
    liste_K= [2650, 2700, 2750 ,2800 ,2850, 2900, 2950, 3000 ]
    liste_prix = [233 ,183, 135, 89 ,50 ,24, 9 ,3]
    r=0.05
    T = 0.04
    Otype='Call'
    
    liste_sigma = []
    
     
    for i in range(len(liste_K)):
         liste_sigma.append(dicho_bs(Otype,S0, liste_K[i], r, T, 0.005, 0.6, liste_prix[i]))
             
    plt.plot(liste_K,liste_sigma)
    plt.title('Smile de volatilité pour des sauts de deux types')
    plt.show()
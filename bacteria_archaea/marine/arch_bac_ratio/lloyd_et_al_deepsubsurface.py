# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 13:30:19 2017

@author: yinonbaron
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def fraction_calc(f):
    a = f/(1.-f)
    log_a = np.log10(a)
    mean_a = 10**log_a.mean()
    a_std = 10**(log_a.std()/np.sqrt(len(log_a))*1.96)
    dist_a = np.random.lognormal(mean=np.log(mean_a),sigma=np.log(a_std),size=1000)
    f_dist = 1./(1.+1./dist_a)
    print(np.percentile(f_dist,97.5)/gmean(f_dist))
    print(gmean(f_dist)/np.percentile(f_dist,2.5))
    print(gmean(f_dist))
    f_arc = 1./(1.+1./mean_a)
    return f_arc


data = pd.read_excel('deepsubsurface.xlsx')

card = data[data['Arc permeabilization'] == 'proteinase K']
card = card[card['Fish or cardFish'] == 'CARDFISH']

frac_archaea_CARD = card['Fraction Arc CARDFISH'].dropna()

bottom_CARD = card[card['Sediment Depth (m)']>0.01]
bottom_CARD = bottom_CARD[bottom_CARD['Fraction Arc CARDFISH']>0]
f_CARD = bottom_CARD['Fraction Arc CARDFISH']

print('Archaea CARD-FISH')
f_arc_CARD = fraction_calc(f_CARD)
#a_CARD = f_CARD/(1-f_CARD)
#log_a_CARD = np.log10(a_CARD)
#mean_a_CARD = 10**log_a_CARD.mean()
#a_CARD_std = 10**(log_a_CARD.std()/np.sqrt(len(log_a_CARD))*1.96)
#dist_a_CARD = np.random.lognormal(mean=np.log(mean_a_CARD),sigma=np.log(a_CARD_std),size=1000)
#f_dist_CARD = 1./(1.+1./dist_a_CARD)
#print(np.percentile(f_dist_CARD,97.5)/gmean(f_dist_CARD))
#print(gmean(f_dist_CARD)/np.percentile(f_dist_CARD,2.5))
#print(gmean(f_dist_CARD))
#f_arc_CARD = 1./(1.+1./mean_a_CARD)


qpcr = data[~np.isnan(data['Fraction Arc qPCR'])]
f1_qpcr = qpcr.drop(qpcr['TaqMan Arc'].dropna().index)
f2_qpcr = f1_qpcr[f1_qpcr['Arc reverse'].str.contains('516')==False]
f3_qpcr = f2_qpcr[f2_qpcr['Arc forward'].str.contains('519')==False]
f4_qpcr = f3_qpcr[f3_qpcr['Sediment Depth (m)']>0.01]
f4_qpcr = f3_qpcr[f3_qpcr['Sediment Depth (m)']>0.01]
f5_qpcr = f4_qpcr[f4_qpcr['Fraction Arc qPCR']>0]['Fraction Arc qPCR']

print('Archaea qPCR')
f_arc_qPCR = fraction_calc(f5_qpcr)
#a_qPCR = f5_qpcr/(1.-f5_qpcr)
#log_a_qPCR = np.log10(a_qPCR)
#inv_log_a_qPCR = -log_a_qPCR
#mean_a_qPCR = 10**log_a_qPCR.mean()
#a_qPCR_std = 10**(log_a_qPCR.std()/np.sqrt(len(log_a_qPCR))*1.96)
#dist_a_qPCR = np.random.lognormal(mean=np.log(mean_a_qPCR),sigma=np.log(a_qPCR_std),size=1000)
#f_dist_qPCR = 1./(1.+1./dist_a_qPCR)
#print(np.percentile(f_dist_qPCR,97.5)/gmean(f_dist_qPCR))
#print(gmean(f_dist_qPCR)/np.percentile(f_dist_qPCR,2.5))
#print(gmean(f_dist_qPCR))
#f_arc_qPCR = 1./(1.+1./mean_a_qPCR)

print('Archaea interstudy')
f_inter = pd.DataFrame([f_arc_CARD,f_arc_qPCR])
f_arc_inter = fraction_calc(f_inter)

print('Bacteria interstudy')
f_bac_inter = fraction_calc(1.-f_inter)
#a_inter = gmean([mean_a_CARD,mean_a_qPCR])
#inter_a_std = np.exp(np.std(np.log([mean_a_CARD,mean_a_qPCR]))/np.sqrt(2)*1.96)
#dist_a_inter = np.random.lognormal(mean=np.log(a_inter),sigma=np.log(inter_a_std),size=1000)
#f_dist_inter = 1./(1.+1./dist_a_inter)
#print(np.percentile(f_dist_inter,97.5)/gmean(f_dist_inter))
#print(gmean(f_dist_inter)/np.percentile(f_dist_inter,2.5))
#print(gmean(f_dist_inter))


r = np.random.normal(-0.8,0.1,1000)

y = lambda x,z: 1./(x+1)*(z**(x+1)-0.1**(x+1))
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 13:51:01 2017

@author: yinonbaron
"""

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd

fig1 = pd.read_excel('../../results.xlsx','Table1 & Fig1',index_col=[0,1])
ms_data = pd.read_excel('../../results.xlsx','Data mentioned in MS',index_col=0)

data = pd.DataFrame(index=['Wild mammals','Humans','Livestock'],columns=['100,000 BP','present'])
data.loc['Wild mammals','100,000 BP'] = ms_data.loc['Prehuman biomass of wild land mammals','Original Value'] + ms_data.loc['Prehuman biomass of marine mammals','Original Value']
data.loc['Wild mammals','present'] = fig1.loc[('Animals','Wild mammals'),'Biomass [Gt C]']
data.loc['Humans','present'] = fig1.loc[('Animals','Humans'),'Biomass [Gt C]']
data.loc['Livestock','present'] = fig1.loc[('Animals','Livestock'),'Biomass [Gt C]']


fig = plt.figure()
fig.set_figwidth(10)
fig.set_figheight(20)
ax = fig.gca()

p3 = plt.bar([0.1,1.1],data.loc['Livestock'],0.8,bottom=data.loc['Humans']+data.loc['Wild mammals'],color='#4250ff')
p2 = plt.bar([0.1,1.1],data.loc['Humans'],0.8,bottom=data.loc['Wild mammals'],color='#b04e2d')
p1 = plt.bar([0.1,1.1],data.loc['Wild mammals'],0.8,color='#ff282d')




plt.xticks([0.1,1.1], ('100,000 BP', 'present'))
plt.legend((p2[0], p3[0],p1[0]), ('Humans', 'Livestock','Wild mammals'),loc='upper left')
ax.set_ylabel('Biomass (Gt C)',fontsize=20)



ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

plt.title('Figure S5')
plt.savefig('../output/figS5.pdf')
plt.savefig('../output/figS5.svg')
plt.show()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 15:17:17 2018

@author: yinon
"""

import matplotlib.pyplot as plt
import pandas as pd
import os

# Get the path of the script
file_path = os.path.dirname(os.path.realpath(__file__))

biomass = pd.read_excel(file_path + '/../../results.xlsx','Table1 & Fig1', index_col= [0,1])
kingdom = pd.Series(index=['Bacteria','Archaea','Plants','Animals','Fungi','Protists','Viruses'])
for x in kingdom.index:
    kingdom.loc[x] = biomass.loc[x,'Biomass [Gt C]'].sum()

biomass4 = pd.Series(data =[74,8,450,2.5,13,4,0.2],index=['Bacteria','Archaea','Plants','Animals','Fungi','Protists','Viruses'])

fig, axes = plt.subplots(ncols=2, sharey=True)

fig.set_figwidth(10)
fig.set_figheight(5)
kingdom.plot(kind='pie',colors=['#ff8541','#9500ff','#5fd35f','#9d93ac','#ffdd55','#5f8dd3','#000000'],ax=axes[0])
animals = pd.Series(index=['Arthropods','Fish','Livestock','Humans','Wild mammals','Wild birds','Annelids','Molluscs','Cnidarians','Nematodes'])
for x in animals.index:
    if x == 'Arthropods':
        animals.loc[x] = biomass.loc[[('Animals','Terrestrial arthropods'),('Animals','Marine arthropods')],'Biomass [Gt C]'].sum()
    else:
        animals.loc[x] = biomass.loc[('Animals',x),'Biomass [Gt C]']


animals.plot(kind='pie',colors=['#ff525d','#6385e7','#e9afaf','#de8787','#ff5200','#fd3cea','#64c7d1','#fff6d3','#9e675f','934028'],ax=axes[1])


plt.show()


plt.savefig(file_path + '/../output/figS4AB.pdf')
plt.savefig(file_path + '/../output/figS4AB.svg')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 15:17:17 2018

@author: yinon
"""

import matplotlib.pyplot as plt
import pandas as pd

biomass4 = pd.Series(data =[74,8,450,2.5,13,4,0.2],index=['Bacteria','Archaea','Plants','Animals','Fungi','Protists','Viruses'])
plt.figure()
biomass4.plot(kind='pie')
animals = pd.Series(data =[1.1,0.7,0.1,0.05,0.007,0.002,0.2,0.2,0.1,0.02],index=['Arthropods','Fish','Livestock','Humans','Wild mammals','Wold birds','Annelids','Molluscs','Cnidarians','Nematodes'])
plt.figure()
animals.plot(kind='pie')
plt.pie(animals,labels=animals.index)

plt.show()
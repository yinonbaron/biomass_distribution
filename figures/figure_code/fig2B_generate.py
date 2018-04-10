# -*- coding: utf-8 -*-
"""
Created on Wed May 17 10:29:39 2017

@author: yinonbaron
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 16 13:51:01 2017

@author: yinonbaron
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# Get the path of the script
file_path = os.path.dirname(os.path.realpath(__file__))

data = pd.DataFrame(index = ['plants','fungi','protists','animals','bacteria','archaea'],columns=['terrestrial','marine','deep subsurface'])

fig1 = pd.read_excel(file_path + '/../../results.xlsx', 'Table1 & Fig1',index_col=(0,1))
fig2a = pd.read_excel(file_path + '/../../results.xlsx', 'Fig2A',index_col=(0,1))
fig2c = pd.read_excel(file_path + '/../../results.xlsx', 'Fig2C')

data.loc['plants'] = [fig1.loc[('Plants','Plants'),'Biomass [Gt C]'], fig2c.iloc[20:23,1].sum(),0]
data.loc['fungi'] = [fig1.loc[('Fungi','Terrestrial'),'Biomass [Gt C]'], fig1.loc[('Fungi','Marine'),'Biomass [Gt C]'],0]
data.loc['protists'] = [fig1.loc[('Protists','Terrestrial'),'Biomass [Gt C]'], fig1.loc[('Protists','Marine'),'Biomass [Gt C]'],0]
data.loc['animals'] = [fig1.loc[[('Animals','Terrestrial arthropods'),
                                 ('Animals','Humans'),
                                 ('Animals','Livestock'),
                                 ('Animals','Wild birds'),
                                 ('Animals','Annelids')],
                                 'Biomass [Gt C]'].sum(),
                       fig1.loc[[('Animals','Fish'),
                                ('Animals','Molluscs'),
                                ('Animals','Cnidarians'),
                                ('Animals','Marine arthropods')],
                                'Biomass [Gt C]'].sum(),0]
data.loc['bacteria'] = [fig1.loc[('Bacteria','Soil'),'Biomass [Gt C]'],fig1.loc[('Bacteria','Marine'),'Biomass [Gt C]'], fig1.loc[[('Bacteria','Marine deep subsurface'),('Bacteria','Terrestrial deep subsurface')],'Biomass [Gt C]'].sum()]
data.loc['archaea'] = [fig1.loc[('Archaea','Soil'),'Biomass [Gt C]'],fig1.loc[('Archaea','Marine'),'Biomass [Gt C]'], fig1.loc[[('Archaea','Marine deep subsurface'),('Archaea','Terrestrial deep subsurface')],'Biomass [Gt C]'].sum()]

norm_data = data.div(data.sum(axis=1), axis=0)

fig, ax = plt.subplots(nrows=1)
terr = plt.barh(np.arange(6.1,0.1,-1),norm_data['terrestrial'],color='#9f764d')
mar = plt.barh(np.arange(6.1,0.1,-1),norm_data['marine'],left=norm_data['terrestrial'], color='#2a66ff')
deep = plt.barh(np.arange(6.1,0.1,-1),norm_data['deep subsurface'],left=norm_data['terrestrial']+norm_data['marine'], color='#373737')
#
#
plt.yticks(np.arange(6,0,-1), ('plants', 'fungi', 'protists','animals', 'bacteria','archaea'),fontsize=20)
plt.legend((terr[0], mar[0],deep[0]), ('Terrestrial', 'Marine','Deep Subsurface'),loc='best')

plt.xlabel('fraction of biomass',fontsize=20)


ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

ax.tick_params(axis='both', which='both', length=0)
plt.savefig(file_path + '/../output/fig2B.pdf')
plt.show()

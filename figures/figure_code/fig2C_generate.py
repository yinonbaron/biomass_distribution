# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 17:20:55 2016

@author: yinonbaron
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
from openpyxl import load_workbook
import os

# Get the path of the script
file_path = os.path.dirname(os.path.realpath(__file__))

matplotlib.rc('xtick', labelsize=20) 
y_pos = [0,0.8]
colormap = np.array([(9,176,20),(205,23,7)])/255

fig1 = pd.read_excel(file_path + '/../../results.xlsx', 'Table1 & Fig1',index_col=(0,1))
fig2a = pd.read_excel(file_path + '/../../results.xlsx', 'Fig2A',index_col=(0,1))
fig2c = pd.read_excel(file_path + '/../../results.xlsx', 'Fig2C')

data = pd.DataFrame(data=[], index=['Marine','Terrestrial'],columns=['Producers','Consumers'])

data.loc['Terrestrial','Producers'] = fig1.loc[('Plants','Plants'),'Biomass [Gt C]']
data.loc['Terrestrial','Consumers'] = fig1.loc[[('Bacteria','Soil'),
                                               ('Archaea','Soil'),
                                               ('Fungi','Terrestrial'),
                                               ('Protists','Soil'),
                                               ('Animals','Terrestrial arthropods'),
                                               ('Animals','Humans'),
                                               ('Animals','Livestock'),
                                               ('Animals','Wild birds'),
                                               ('Animals','Annelids')],
                                               'Biomass [Gt C]'].sum()
data.loc['Terrestrial','Consumers'] += fig2a.loc[[('Terrestrial','Wild land mammals'),('Terrestrial','Nematodes')],'Biomass [Gt C]'].sum()

data.loc['Marine','Producers'] = fig2c.iloc[20:25,1].sum()
data.loc['Marine','Consumers'] = fig1.loc[[('Bacteria','Marine'),
                                            ('Archaea','Marine'),
                                            ('Animals','Fish'),
                                            ('Animals','Molluscs'),
                                            ('Animals','Cnidarians'),
                                            ('Animals','Marine arthropods'),
                                            ('Fungi','Marine')],
                                            'Biomass [Gt C]'].sum()
data.loc['Marine','Consumers'] += fig1.loc[('Protists','Marine'),'Biomass [Gt C]'] - fig2c.iloc[22:25,1].sum()
data.loc['Marine','Consumers'] += fig2a.loc[[('Marine','Wild marine mammals'),('Marine','Nematodes')],'Biomass [Gt C]'].sum()

fig, axes = plt.subplots(ncols=2, sharey=True)


fig.set_figwidth(10)
fig.set_figheight(1)


axes[0].barh(y_pos,data.loc['Marine'], left=0,color=colormap)
axes[0].set_title('marine',fontsize=20)
axes[0].text(data.loc['Marine','Producers']+0.3,-0.25,int(np.round(data.loc['Marine','Producers'])),fontsize=20)
axes[0].text(data.loc['Marine','Consumers']+0.3,0.57,int(np.floor(data.loc['Marine','Consumers'])),fontsize=20)

axes[1].barh(y_pos,data.loc['Terrestrial'], left=0,color=colormap)
axes[1].set_title('terrestrial',fontsize=20)
axes[1].text(data.loc['Terrestrial','Producers']+0.3,-0.25,int(np.round(data.loc['Terrestrial','Producers'])),fontsize=20)
axes[1].text(data.loc['Terrestrial','Consumers']+0.3,0.57,int(np.round(data.loc['Terrestrial','Consumers'])),fontsize=20)


for ax in axes:
    for key, value in ax.spines.items():
        value.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([0,1])
    ax.set_yticklabels(['producers','consumers'],fontsize=20)
    ax.tick_params(axis='both', which='both', length=0)




axes[0].set_xlim([0,8])
axes[1].set_xlim([0,480])
plt.title('Figure 2B')
plt.savefig(file_path + '/../output/fig2C.svg')
plt.savefig(file_path + '/../output/fig2C.pdf')
plt.show()


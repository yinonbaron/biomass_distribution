
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

# Get the path of the script
file_path = os.path.dirname(os.path.realpath(__file__))


font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 15}

matplotlib.rc('font', **font)

data = pd.read_excel(file_path + '/../../results.xlsx','FigS2-S3',index_col=0)
biomass = pd.read_excel(file_path + '/../../results.xlsx','Table1 & Fig1',index_col=[0,1])
ind_num = pd.read_excel(file_path + '/../../results.xlsx','Table S1',index_col=[0,1])
data.loc['Plants','Number of individuals'] = np.nan
data.loc['Chordates','Number of individuals'] = np.nan

data.loc['Bacteria',['Biomass [Gt C]','Uncertainty']] = [biomass.loc['Bacteria','Biomass [Gt C]'].sum(),biomass.loc[('Bacteria','Terrestrial deep subsurface'),'Total uncertainty']]
data.loc['Archaea',['Biomass [Gt C]','Uncertainty']] = [biomass.loc['Archaea','Biomass [Gt C]'].sum(),biomass.loc[('Archaea','Terrestrial deep subsurface'),'Total uncertainty']]
data.loc['Plants',['Biomass [Gt C]','Uncertainty']] = [biomass.loc[('Plants','Plants'),'Biomass [Gt C]'],biomass.loc[('Plants','Plants'),'Uncertainty']]
data.loc['Plants (trees)',['Biomass [Gt C]','Uncertainty']] = [biomass.loc[('Plants','Plants'),'Biomass [Gt C]'],biomass.loc[('Plants','Plants'),'Uncertainty']]
data.loc['Fungi',['Biomass [Gt C]','Uncertainty']] = [biomass.loc['Fungi','Biomass [Gt C]'].sum(),biomass.loc[('Fungi','Terrestrial'),'Total uncertainty']]
data.loc['Arthropods',['Biomass [Gt C]']] = biomass.loc[[('Animals','Terrestrial arthropods'),('Animals','Marine arthropods')],'Biomass [Gt C]'].sum()
data.loc['Annelids','Biomass [Gt C]'] = biomass.loc[('Animals','Annelids'),'Biomass [Gt C]']
data.loc['Molluscs','Biomass [Gt C]'] = biomass.loc[('Animals','Molluscs'),'Biomass [Gt C]']
data.loc['Fish',['Biomass [Gt C]','Uncertainty']] = [biomass.loc[('Animals','Fish'),'Biomass [Gt C]'],biomass.loc[('Animals','Fish'),'Uncertainty']]
data.loc['Nematodes','Biomass [Gt C]'] = biomass.loc[('Animals','Nematodes'),'Biomass [Gt C]']
data.loc['Humans','Biomass [Gt C]'] = biomass.loc[('Animals','Humans'),'Biomass [Gt C]']
data.loc['Livestock','Biomass [Gt C]'] = biomass.loc[('Animals','Livestock'),'Biomass [Gt C]']
data.loc['Cnidarians','Biomass [Gt C]'] = biomass.loc[('Animals','Cnidarians'),'Biomass [Gt C]']
data.loc['Protists',['Biomass [Gt C]','Uncertainty']] = [biomass.loc['Fungi','Biomass [Gt C]'].sum(),biomass.loc[('Protists','Marine'),'Total uncertainty']]
data.loc['Wild birds','Biomass [Gt C]'] = biomass.loc[('Animals','Wild birds'),'Biomass [Gt C]']
data.loc['Chordates','Biomass [Gt C]'] = biomass.loc[('Animals',['Fish','Livestock','Humans','Wild mammals','Wild birds']),'Biomass [Gt C]'].sum()

data.loc['Bacteria','Number of individuals'] = ind_num.loc['Bacteria','Number of individuals'].sum()
data.loc['Archaea','Number of individuals'] = ind_num.loc['Archaea','Number of individuals'].sum()
data.loc['Plants (trees)','Number of individuals'] = ind_num.loc['Plants','Number of individuals'].sum()
data.loc['Fungi','Number of individuals'] = ind_num.loc['Fungi','Number of individuals'].sum()
data.loc['Arthropods','Number of individuals'] = ind_num.loc[[('Animals','Terrestrial arthropods'),('Animals','Marine arthropods')],'Number of individuals'].sum()
data.loc['Annelids','Number of individuals'] = ind_num.loc[('Animals','Annelids'),'Number of individuals']
data.loc['Molluscs','Number of individuals'] = ind_num.loc[('Animals','Molluscs'),'Number of individuals']
data.loc['Cnidarians','Number of individuals'] = ind_num.loc[('Animals','Cnidarians'),'Number of individuals']
data.loc['Fish','Number of individuals'] = ind_num.loc[('Animals','Fish'),'Number of individuals']
data.loc['Nematodes','Number of individuals'] = ind_num.loc[('Animals','Nematodes'),'Number of individuals']
data.loc['Humans','Number of individuals'] = ind_num.loc[('Animals','Humans'),'Number of individuals']
data.loc['Livestock','Number of individuals'] = ind_num.loc[('Animals','Livestock'),'Number of individuals']
data.loc['Wild birds','Number of individuals'] = ind_num.loc[('Animals','Wild birds'),'Number of individuals']
data.loc['Protists','Number of individuals'] = ind_num.loc['Protists','Number of individuals'].sum()


lower_error = data['Biomass [Gt C]'] - data['Biomass [Gt C]']/data['Uncertainty']
upper_error = data['Biomass [Gt C]']*data['Uncertainty'] - data['Biomass [Gt C]']

# Fig S3
figs2 = data[~pd.isnull(data['Number of species'])]
figs3 = data[~pd.isnull(data['Number of individuals'])]


plt.figure()
ax= plt.gca() 

plt.errorbar(figs2['Number of species'],
             figs2['Biomass [Gt C]'],
             yerr=[lower_error.loc[figs2.index],upper_error.loc[figs2.index]],
             axes=ax,
             marker='.',
             capthick=1.5,
             elinewidth=1.5,
             ecolor='#bfbfbf',
             ms=20,
             fmt='',
             ls='None',
             color='k')

ax.set_xscale("log", nonposx='clip')
ax.set_yscale("log", nonposy='clip')
for txt in (data[data['Number of species'] != np.nan].index):
    ax.annotate(txt,(data.loc[txt,'Number of species']*1.1,data.loc[txt,'Biomass [Gt C]']*1.11))
plt.ylabel('Biomass [Gt C]', fontsize=15)
plt.xlabel('Number of species', fontsize=15)
plt.xlim([1e3,1e7])

plt.title('Figure S3')
plt.savefig(file_path + '/../output/figS3.pdf')
plt.savefig(file_path + '/../output/figS3.svg')


# Fig S2

plt.figure()
ax= plt.gca()

plt.errorbar(figs3['Number of individuals'],
             figs3['Biomass [Gt C]'],
             yerr=[lower_error.loc[figs3.index],upper_error.loc[figs3.index]],
             axes=ax,
             marker='.',
             capthick=1.5,
             elinewidth=1.5,
             ecolor='#bfbfbf',
             ms=20,
             fmt='',
             ls='None',
             color='k')


ax.set_xscale("log", nonposx='clip')
ax.set_yscale("log", nonposy='clip')
for txt in (data[data['Number of individuals'] != np.nan].index):
    ax.annotate(txt,(data.loc[txt,'Number of individuals']*1.1,data.loc[txt,'Biomass [Gt C]']*1.1))
plt.ylabel('Biomass [Gt C]', fontsize=15)
plt.xlabel('Number of individuals', fontsize=15)
plt.xticks([1e10,1e15,1e20,1e25,1e30])
plt.title('Figure S2')
plt.savefig(file_path + '/../output/figS2.pdf')
plt.savefig(file_path + '/../output/figS2.svg')

plt.show()


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


plt.figure()
ax= plt.gca() 
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 15}

matplotlib.rc('font', **font)

data = pd.read_excel('BiomassEarth_Results_20180108.xlsx','FigS2-S3',index_col=0)
data.loc['Plants','Number of individuals'] = np.nan
data.loc['Chordates','Number of individuals'] = np.nan



lower_error = data['Biomass [g]'] - data['Biomass [g]']/data['Uncertainty']
upper_error = data['Biomass [g]']*data['Uncertainty'] - data['Biomass [g]']




plt.errorbar(data['Number of species'],
             data['Biomass [g]']/1e15,
             yerr=[lower_error/1e15,upper_error/1e15],
             axes=ax,
             marker='.',
             capthick=1.5,
             elinewidth=1.5,
             ecolor='#bfbfbf',
             ms=20,
             fmt='',
             ls='None',
             color='k')
plt.loglog(data.loc['Plants','Number of species'],
             data.loc['Plants','Biomass [g]']/1e15,
             axes=ax,
             marker='.',
             ms=20,
             ls='None',
             color='k')

ax.set_xscale("log", nonposx='clip')
ax.set_yscale("log", nonposy='clip')
for txt in (data[data['Number of species'] != np.nan].index):
    ax.annotate(txt,(data.loc[txt,'Number of species'],data.loc[txt,'Biomass [g]']/1e15))
plt.ylabel('Biomass (Gt C)')
plt.xlabel('Number of species')
plt.xlim([1e3,1e7])

plt.savefig('figS3_20180111.svg')


# In[67]:

plt.figure()
ax= plt.gca()

plt.errorbar(data['Number of individuals'],
             data['Biomass [g]']/1e15,
             yerr=[lower_error/1e15,upper_error/1e15],
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
    ax.annotate(txt,(data.loc[txt,'Number of individuals'],data.loc[txt,'Biomass [g]']/1e15))
plt.ylabel('Biomass (Gt C)')
plt.xlabel('Number of individuals')
plt.xticks([1e10,1e15,1e20,1e25,1e30])
plt.savefig('figS2_20180111.svg')

plt.show()
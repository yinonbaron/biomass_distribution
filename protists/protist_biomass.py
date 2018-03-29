
# coding: utf-8

# In[1]:


# Load dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean
import sys
sys.path.insert(0,'../statistics_helper/')
from fraction_helper import *
from CI_helper import *
from excel_utils import *
pd.options.display.float_format = '{:,.1e}'.format


# # Estimating the total biomass of protists
# To estimate the total biomass of protists, we combine our estimates for the total biomass of marine and terrestrial protists, which we have generated in the dedicated sections for each group. Our estimates for the biomass of the marine and terrestrial protists are presented below:

# In[2]:


data = pd.read_excel('protists_biomass_estimate.xlsx')
data


# To estimate the total biomass of protists, we sum up the contributions from terrestrial and marine protists. 

# In[3]:


best_estimate = data.loc[[0,1],'Value'].sum()
mul_CI = CI_sum_prop(estimates=data.loc[[0,1],'Value'], mul_CIs=data.loc[[0,1],'Uncertainty'])


# # Estimating the total number of protists
# To estimate the total number of individual protists, we estimate the total number of nano-pico eukaryotes, as they are the smallest eukaryotes and still have significant biomass. The diameter range of pico-nanoplankton is 0.8-5 µm. We use the geometric mean of the radius range, which is ≈1 µm. This means that the mean cell volume is ≈4 $µm^3$. We use a conversion equation from biovolume to carbon content reported in [Pernice et al.](https://dx.doi.org/10.1038%2Fismej.2014.168) of: $$carbon\ content\ [pg\ C\ cell^-1] = 0.216×V^{0.939} $$

# In[4]:


# Conversion equation from Pernice et al.
conversion_eq = lambda x: 0.216*x**0.939

# We estimate a biovolume of ≈4 µm^3 per pico-nano eukaryote
pico_nano_vol = 4

# Convert biovolume to carbon content
pico_nano_cc = conversion_eq(pico_nano_vol)

print('We estimate a pico-nanoprotists has a carbon content of ≈%.0f pg C' %pico_nano_cc)


# We divide our estimate of the total biomass of pico-nanoprotists by our estimate of the carbon content of a single pico-nano protist. This give us an estimate for the total number of individual protists.

# In[5]:


# Load our estimate of the total biomass of pico-nanoprotists
pico_nano_biomass = data.loc[2,'Value']

# Calculate the total number of individual protists
protist_num = pico_nano_biomass*1e15/(pico_nano_cc/1e12)
print('Our estimate of the total number of individual protists is ≈%.0e ' %protist_num)


# In[6]:


# Feed total marine protists results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Protists','Marine'), 
               col=['Biomass [Gt C]','Uncertainty','Total uncertainty'],
               values=[data.loc[1,'Value'],data.loc[1,'Uncertainty'],mul_CI],
               path='../results.xlsx')

# Feed total terrestrial protists results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Protists','Terrestrial'), 
               col=['Biomass [Gt C]','Uncertainty'],
               values=[data.loc[0,'Value'],data.loc[0,'Uncertainty']],
               path='../results.xlsx')

# Feed total protist results to Table S1
update_results(sheet='Table S1', 
               row=('Protists','Protists'), 
               col=['Number of individuals'],
               values=protist_num,
               path='../results.xlsx')



# coding: utf-8

# In[1]:


# Load dependencies
import numpy as np
import pandas as pd
import sys
sys.path.insert(0,'../../../statistics_helper/')
from excel_utils import *


# # Estimating the total biomass of humans
# To estimate the total biomass of humans, we rely on estimates of the total human population from the [UN World Population Prospects of 2017](https://esa.un.org/unpd/wpp/Download/Standard/Population/) (File - 'Total Population - Both Sexes'). We use the estimate for the total human population in 2015

# In[2]:


#Load data from the UN
data = pd.read_excel('humans_data.xlsx',index_col=0,skiprows=16)

# Use data from 2015, multiply by 1000 because data is given in thousands
tot_human_pop = data.loc[1,'2015']*1e3

print('The UN estimate for the total human population is ≈%.1e' %tot_human_pop)


# We use an estimate for the average body mass of humans of ≈50 kg from [Hern](http://link.springer.com/article/10.1023/A:1022153110536). We convert the average body weight to carbon mass assuming 70% water content and 50% carbon out of the dry weight:

# In[3]:


wet_to_c = 0.15
human_cc = 5e4*wet_to_c


# We estimate the total biomass of humans by multiplying the total number of humans by the average carbon content of a single human:

# In[4]:


best_estimate = tot_human_pop*human_cc

print('Our best estimate for the total biomass of humans is ≈%.2f Gt C' %(best_estimate/1e15))


# In[5]:


# Feed results to the chordate biomass data
old_results = pd.read_excel('../../animal_biomass_estimate.xlsx',index_col=0)
result = old_results.copy()
result.loc['Humans',(['Biomass [Gt C]','Uncertainty'])] = (best_estimate/1e15,None)
result.to_excel('../../animal_biomass_estimate.xlsx')

# Feed results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Animals','Humans'), 
               col='Biomass [Gt C]',
               values=best_estimate/1e15,
               path='../../../results.xlsx')

# Feed results to Table S1
update_results(sheet='Table S1', 
               row=('Animals','Humans'), 
               col='Number of individuals',
               values=tot_human_pop,
               path='../../../results.xlsx')



# coding: utf-8

# In[1]:


# Load dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.display.float_format = '{:,.1e}'.format
import sys
pd.options.display.float_format = '{:,.1e}'.format
sys.path.insert(0,'../../../statistics_helper/')
from excel_utils import *


# # Estimating the biomass of livestock
# To estimate the biomass of livestock, we rely on data on global stocks of cattle, sheep goats, and pigs froms the Food and Agriculture Organization database FAOStat. We downloaded data from the domain Production/Live animals.
# We combined data on the total stocks of each animal with estimates of the mean mass of each type of animal species (in kg) from [Dong et al.](http://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_10_Ch10_Livestock.pdf), Annex 10A.2, Tables 10A-4 to 10A-9.
# 
# Here are samples of the data:

# In[2]:


# Load global stocks data
stocks = pd.read_csv('FAOSTAT_stock_data_mammals.csv')
stocks.head()


# In[3]:


# Load species body mass data
body_mass = pd.read_excel('livestock_body_mass.xlsx',skiprows=1,index_col=0) 
body_mass.head()


# We pivot the stocks DataFrame to have a view of each kind of animal at each region:

# In[4]:


# Replace NaN with zeros
stocks.fillna(value=0,inplace=True)
stock_pivot = pd.pivot(stocks.Area,stocks.Item, stocks.Value).astype(float)

# Replace NaN with zeros
stock_pivot.fillna(value=0,inplace=True)

stock_pivot


# There is a difference between the body mass of a dairy producing cow to a non-dairy producing cow. We thus count seperately the dairy producing cattle from the non-dairy producing cattle. Data about the amount of dairy cattle comes from the FAOStat domain Production - Livestock Primary.
# There is also a difference in body mass between breeding and non-breeding pigs. We assume 90% of the population is breeding based on IPCC, 2006, Vol.4, Ch.10,Table.10.19.

# In[5]:


# Load data on the number of dairy producing cattle
dairy = pd.read_csv('FAOSTAT_cattle_dairy_data.csv')

# Set the index of the DataFrame to be the region so we can compare with the stocks data
dairy.set_index('Area',inplace=True)

# Add a category of dairy producing cattle
stock_pivot['Cattle - dairy'] = dairy.Value

# Set the amount of non-dairy producing cattle to be the total number minus the dairy producing cattle
stock_pivot['Cattle'] = stock_pivot['Cattle']-stock_pivot['Cattle - dairy']

# Rename the Cattle column name to Cattle - non-dairy
stock_pivot.rename(columns={'Cattle': 'Cattle - non-dairy'}, inplace=True)

# Set the amount of non-breeding (market) pigs (swine) to 10% of the total amount of pigs
stock_pivot['Swine - market'] = 0.1*stock_pivot['Pigs']

# Set the amount of breeding pigs (swine) to 90% of the total amount of pigs
stock_pivot['Pigs'] *= 0.9

# Rename the Pigs column name to Swine - breeding
stock_pivot.rename(columns={'Pigs': 'Swine - breeding'}, inplace=True)

stock_pivot


# Data on the mass of animals is divided into different regions than the FAOStat data so we need preprocess the stocks DataFrame and merge it with the body mass data:

# In[6]:


# Preprocessing the stocks DataFrame

# Calculate the total number of animals in Latin America by subtracting values for Northern America from the total
# values for the Americas
stock_pivot.loc['Americas'] -= stock_pivot.loc['Northern America']

# Change name of Americas to Latin America
stock_pivot.rename(index={'Americas': 'Latin America'},inplace=True)

# Calculate the total number of animals in Asia without the Indian Subcontinent by subtracting values for the Southern Asia 
# from the total values for the Asia
stock_pivot.loc['Asia'] -= stock_pivot.loc['Southern Asia']

# Change name of Southern Asia to Indian Subcontinent
stock_pivot.rename(index={'Southern Asia': 'Indian Subcontinent'},inplace=True)


stock_pivot


# We now multiply the stocks of each animal type and for each region by the characteristic body weight of each animal:

# In[7]:


wet_biomass =(body_mass*stock_pivot)
wet_biomass


# We sum over all regions and convert units from kg wet weight to Gt C carbon by assuming carbon is ≈15% of the wet weight (30% dry weight of wet weight and carbon is 50% of dry weight).

# In[8]:


pd.options.display.float_format = '{:,.3f}'.format

# conversion factor from kg wet weight to Gt C
kg_to_gt_c = 1000*0.15/1e15
total_biomass = wet_biomass.sum()*kg_to_gt_c
total_biomass


# We sum over all animal categories to generate our best estimate for the total biomass of livestock

# In[9]:


best_estimate = total_biomass.sum()
print('Our best estimate for the biomass of mammal livestock is %.1f Gt C' % best_estimate)


# In[10]:


# Feed results to the chordate biomass data
old_results = pd.read_excel('../../animal_biomass_estimate.xlsx',index_col=0)
result = old_results.copy()
result.loc['Livestock',(['Biomass [Gt C]','Uncertainty'])] = (best_estimate,None)
result.to_excel('../../animal_biomass_estimate.xlsx')

# Feed results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Animals','Livestock'), 
               col='Biomass [Gt C]',
               values=best_estimate,
               path='../../../results.xlsx')

# Feed results to Table S1
update_results(sheet='Table S1', 
               row=('Animals','Livestock'), 
               col='Number of individuals',
               values=stock_pivot.sum().sum(),
               path='../../../results.xlsx')


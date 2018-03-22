
# coding: utf-8

# In[1]:


# Load dependencies
import pandas as pd
import numpy as np
pd.options.display.float_format = '{:,.1e}'.format
import sys
sys.path.insert(0,'../../../../statistics_helper/')
from excel_utils import *


# # Estimating the biomass of poultry
# To estimate the biomass of poultry, we rely on data on global stocks of chickens, ducks, and turkeys from the Food and Agriculture Organization database FAOStat. We downloaded data from the domain Production/Live animals.
# We combined data on the total stocks of each animal with estimates of the mean mass of each type of animal species (in kg) from [Dong et al.](http://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_10_Ch10_Livestock.pdf), Annex 10A.2, Tables 10A-4 to 10A-9.
# 
# Here are samples of the data:

# In[2]:


# Load bird data
bird = pd.read_csv('FAOSTAT_data_bird.csv')
bird.head()


# In[3]:


# Load body mass data
body_mass = pd.read_csv('ipcc_animal_weight.csv')
body_mass.set_index('IPCC Area',inplace=True)
body_mass.head()


# We pivot the stocks DataFrame to have a view of each kind of animal at each region:

# In[4]:



# Replace NaN with zeros
bird.fillna(value=0,inplace=True)

bird_pivot = pd.pivot(bird.Area,bird.Item, bird.Value).astype(float)

# Replace NaN with zeros
bird_pivot.fillna(value=0,inplace=True)


bird_pivot


# There is a difference between the body mass of a egg laying chicken to a non-egg laying chicken. We thus count seperately the egg laying chicken from the non-egg laying chicken. Data about the amount of egg laying chicken comes from the FAOStat domain Production - Livestock Primary.

# In[5]:


# Load data about egg laying chicken
egg = pd.read_csv('FAOSTAT_data_eggs.csv')

# Set the index of the DataFrame to be the region so we can compare with the stocks data
egg.set_index('Area',inplace=True)

# Add a category of egg laying chicken
bird_pivot['Chicken - Layers'] = egg.Value

# Set the amount of non-egg laying chicken to be the total number minus the egg laying chicken
bird_pivot['Chickens'] -= egg.Value

# Rename the Chicken column name to Chicken - Broileers
bird_pivot.rename(columns={'Chickens': 'Chicken - Broilers'},inplace=True)

# Use only data for chicken, ducks and turkeys
birds = ['Chicken - Broilers','Chicken - Layers','Ducks','Turkeys']
bird_pivot_filt = bird_pivot[birds]
body_mass_filt = body_mass[birds]

bird_pivot_filt


# Data on the mass of animals is divided into different regions than the FAOStat data so we need preprocess the stocks DataFrame and merge it with the body mass data:

# In[6]:


# Convert units
bird_pivot_filt *= 1e3

# Calculate the total number of animals in Latin America by subtracting values for Northern America from the total
# values for the Americas
bird_pivot_filt.loc['Americas'] -= bird_pivot_filt.loc['Northern America']

# Change name of Americas to Latin America
bird_pivot_filt.rename(index={'Americas': 'Latin America'},inplace=True)

# Calculate the total number of animals in Asia without the Indian Subcontinent by subtracting values for the Southern Asia 
# from the total values for the Asia
bird_pivot_filt.loc['Asia'] -= bird_pivot_filt.loc['Southern Asia']

# Change name of Southern Asia to Indian Subcontinent
bird_pivot_filt.rename(index={'Southern Asia': 'Indian Subcontinent'},inplace=True)

bird_pivot_filt


# We now multiply the stocks of each animal type and for each region by the characteristic body weight of each animal:

# In[7]:


wet_bird_biomass = (body_mass_filt*bird_pivot_filt)
wet_bird_biomass


# We sum over all regions and convert units from kg wet weight to Gt C carbon by assuming carbon is ≈15% of the wet weight (30% dry weight of wet weight and carbon is 50% of dry weight).

# In[8]:


pd.options.display.float_format = '{:,.3f}'.format

# conversion factor from kg wet weight to Gt C
kg_to_gt_c = 1000*0.15/1e15
total_biomass = wet_bird_biomass.sum()*kg_to_gt_c
total_biomass


# In[9]:


best_estimate = total_biomass.sum()
print('Our estimate for the total biomass of poultry is ≈%.3f Gt C' % best_estimate)


# In[10]:


update_MS_data(row='Biomass of poultry',values= best_estimate,path='../../../../results.xlsx')



# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np

bird = pd.read_csv('FAOSTAT_data_bird.csv')
egg = pd.read_csv('FAOSTAT_data_eggs.csv')
body_mass = pd.read_csv('ipcc_animal_weight.csv')
body_mass.set_index('IPCC Area',inplace=True)
egg.set_index('Area',inplace=True)
bird_pivot = pd.pivot(bird.Area,bird.Item, bird.Value).astype(float)

bird_pivot['Chicken - Layers'] = egg.Value
bird_pivot['Chickens'] -= egg.Value
bird_pivot.rename(columns={'Chickens': 'Chicken - Broilers'},inplace=True)
birds = ['Chicken - Broilers','Chicken - Layers','Ducks','Turkeys']
bird_pivot_filt = bird_pivot[birds]
body_mass_filt = body_mass[birds]

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

bird_biomass = ((body_mass_filt*bird_pivot_filt)*1e3*0.15).sum()/1e15
bird_biomass


# In[2]:

print('Our estimate for the total biomass of poultry is ≈%.3f Gt C' % bird_biomass.sum())


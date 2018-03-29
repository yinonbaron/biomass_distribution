
# coding: utf-8

# In[1]:


# Load dependencies
import numpy as np
import pandas as pd
pd.options.display.float_format = '{:,.1e}'.format
import sys
sys.path.insert(0, '../../statistics_helper')
from CI_helper import *
from excel_utils import *


# # Estimating the total biomass of terrestrial deep subsurface archaea and bacteria
# 
# We use our best estimates for the total biomass of terrestrial deep subsurface prokaryotes and the fraction of archaea and bacteria out of the total population of terrestrial deep subsurface prokaryotes to estimate the total biomass of terrestrial deep subsurface bacteria and archaea.

# In[2]:


results = pd.read_excel('terrestrial_deep_subsurface_prok_biomass_estimate.xlsx')
results


# We multiply all the relevant parameters to arrive at our best estimate for the biomass of terrestrial deep subsurface archaea and bacteria, and propagate the uncertainties associated with each parameter to calculate the uncertainty associated with the estimate for the total biomass.

# In[3]:


# Calculate the total biomass of marine archaea and bacteria
total_arch_biomass = results['Value'][0]*results['Value'][1]
total_bac_biomass = results['Value'][0]*results['Value'][2]

print('Our best estimate for the total biomass of terrestrial deep subsurface archaea is %.0f Gt C' %(total_arch_biomass/1e15))
print('Our best estimate for the total biomass of terrestrial deep subsurface bacteria is %.0f Gt C' %(total_bac_biomass/1e15))

# Propagate the uncertainty associated with each parameter to the final estimate

arch_biomass_uncertainty = CI_prod_prop(results['Uncertainty'][:2])
bac_biomass_uncertainty = CI_prod_prop(results.iloc[[0,2]]['Uncertainty'])

print('The uncertainty associated with the estimate for the biomass of archaea is %.1f-fold' %arch_biomass_uncertainty)
print('The uncertainty associated with the estimate for the biomass of bacteria is %.1f-fold' %bac_biomass_uncertainty)


# In[4]:


# Feed bacteria results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Bacteria','Terrestrial deep subsurface'), 
               col=['Biomass [Gt C]', 'Uncertainty'],
               values=[total_bac_biomass/1e15,bac_biomass_uncertainty],
               path='../../results.xlsx')

# Feed archaea results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Archaea','Terrestrial deep subsurface'), 
               col=['Biomass [Gt C]', 'Uncertainty'],
               values=[total_arch_biomass/1e15,arch_biomass_uncertainty],
               path='../../results.xlsx')

# Feed bacteria results to Table S1
update_results(sheet='Table S1', 
               row=('Bacteria','Terrestrial deep subsurface'), 
               col=['Number of individuals'],
               values= results['Value'][0]*results['Value'][2]/results['Value'][3],
               path='../../results.xlsx')

# Feed archaea results to Table S1
update_results(sheet='Table S1', 
               row=('Archaea','Terrestrial deep subsurface'), 
               col=['Number of individuals'],
               values= results['Value'][0]*results['Value'][1]/results['Value'][3],
               path='../../results.xlsx')


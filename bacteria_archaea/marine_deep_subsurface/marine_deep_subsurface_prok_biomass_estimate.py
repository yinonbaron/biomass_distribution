
# coding: utf-8

# # Estimating the total biomass of marine deep subsurface archaea and bacteria
# 
# We use our best estimates for the total number of marine deep subsurface prokaryotes, the carbon content of marine deep subsurface prokaryotes and the fraction of archaea and bacteria out of the total population of marine deep subsurface prokaryotes to estimate the total biomass of marine deep subsurface bacteria and archaea.

# In[1]:


import numpy as np
import pandas as pd
pd.options.display.float_format = '{:,.1e}'.format
import sys
sys.path.insert(0, '../../statistics_helper')
from CI_helper import *
results = pd.read_excel('marine_deep_subsurface_prok_biomass_estimate.xlsx')
results


# We multiply all the relevant parameters to arrive at our best estimate for the biomass of marine deep subsurface archaea and bacteria, and propagate the uncertainties associated with each parameter to calculate the uncertainty associated with the estimate for the total biomass.

# In[2]:


# Calculate the total biomass of marine archaea and bacteria
total_arch_biomass = results['Value'][0]*results['Value'][1]*1e-15*results['Value'][2]
total_bac_biomass = results['Value'][0]*results['Value'][1]*1e-15*results['Value'][3]

print('Our best estimate for the total biomass of marine deep subsurface archaea is %.0f Gt C' %(total_arch_biomass/1e15))
print('Our best estimate for the total biomass of marine deep subsurface bacteria is %.0f Gt C' %(total_bac_biomass/1e15))

# Propagate the uncertainty associated with each parameter to the final estimate

arch_biomass_uncertainty = CI_prod_prop(results['Uncertainty'][:3])
bac_biomass_uncertainty = CI_prod_prop(results.iloc[[0,1,3]]['Uncertainty'])

print('The uncertainty associated with the estimate for the biomass of archaea is %.1f-fold' %arch_biomass_uncertainty)
print('The uncertainty associated with the estimate for the biomass of bacteria is %.1f-fold' %bac_biomass_uncertainty)

CI_sum_prop(np.array([58,1.3,8,7]),np.array([10.2,1.8,2.02,7.6]))


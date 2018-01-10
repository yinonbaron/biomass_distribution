
# coding: utf-8

# # Estimating the total biomass of marine archaea and bacteria
# 
# We use our best estimates for the total number of marine prokaryotes, the carbon content of marine prokaryotes and the fraction of marine archaea and bacteria out of the total population of marine prokaryotes to estimate the total biomass of marine bacteria and archaea

# In[1]:

import numpy as np
import pandas as pd
pd.options.display.float_format = '{:,.1e}'.format
import sys
sys.path.insert(0, '../../statistics_helper')
from CI_helper import *
results = pd.read_excel('marine_prok_biomass_estimate.xlsx')


# These are our best estimates for the different parameters required for the estimate, along with the associated uncertainties

# In[2]:

results.head()


# We multiply all the relevant parameters to arrive at our best estimate for the biomass of marine archaea and bacteria, and propagate the uncertainties associated with each parameter to calculate the uncertainty associated with the estimate for the total biomass

# In[3]:

# Calculate the total biomass of marine archaea and bacteria
total_arch_biomass = results['Value'][0]*results['Value'][1]*(1+results['Value'][4])*1e-15*results['Value'][2]
total_bac_biomass = results['Value'][0]*results['Value'][1]*(1+results['Value'][4])*1e-15*results['Value'][3]

print('Our best estimate for the total biomass of marine archaea is %.1f Gt C' %(total_arch_biomass/1e15))
print('Our best estimate for the total biomass of marine bacteria is %.1f Gt C' %(total_bac_biomass/1e15))

# Propagate the uncertainty in the total biomass of bacteria and archaea
prok_biomass_CI = CI_sum_prop(estimates=np.array([results['Value'][0]*results['Value'][1], results['Value'][0]*results['Value'][1]*results['Value'][4]]), mul_CIs=np.array([CI_prod_prop(results['Uncertainty'][:2]),results['Uncertainty'][4]]))

# Propagate the uncertainty associated with each parameter to the final estimate
arch_biomass_uncertainty = CI_prod_prop(np.array([prok_biomass_CI,results['Uncertainty'][2]]))
bac_biomass_uncertainty = CI_prod_prop(np.array([prok_biomass_CI,results['Uncertainty'][3]]))

print('The uncertainty associated with the estimate for the biomass of archaea is %.1f-fold' %arch_biomass_uncertainty)
print('The uncertainty associated with the estimate for the biomass of bacteria is %.1f-fold' %bac_biomass_uncertainty)


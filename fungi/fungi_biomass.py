
# coding: utf-8

# # Estimating the total biomass of fungi
# We use our best estimates for the total biomass of soil microbes and the fraction of fungi out of the total biomass of soil microbes to estimate the total biomass of fungi.

# In[1]:

import numpy as np
import pandas as pd
import sys
sys.path.insert(0, '../statistics_helper')
from CI_helper import *

pd.options.display.float_format = '{:,.1e}'.format

results = pd.read_excel('fungi_biomass_estimate.xlsx')


# These are our best estimates for the different parameters required for the estimate, along with the associated uncertainties

# In[2]:

results


# In[3]:

# Calculate the total biomass of fungi
soil_fungi_biomass = np.prod(results['Value'])
print('Our best estimate for the total biomass of soil fungi is %.f Gt C' %(soil_fungi_biomass/1e15))

# Propagate the uncertainty associated with each parameter to the final estimate

soil_fungi_biomass_CI = CI_prod_prop(results['Uncertainty'])

print('The uncertainty associated with the estimate for the biomass of soil fungi is %.1f-fold' %soil_fungi_biomass_CI)


# We multiply all the relevant parameters to arrive at our best estimate for the biomass of fungi, and propagate the uncertainties associated with each parameter to calculate the uncertainty associated with the estimate for the total biomass. 

# We add to the our estimate of the biomass of soil fungi our estimates for the contribution of marine and deep subsurface fungi. For marine fungi, we project an uncertainty of 10-fold (similar to our uncertainties for other marine taxa.

# In[4]:

marine_fungi = 0.6e15
marine_fungi_CI = 10


# For deep subsurface fungi, we estimate they constitute 1% of the total biomass of terresrial deep subsurface bacterial and archaeal biomass. We assume ≈10-fold uncertainty in the fraction of fungi out of the total biomass of the terrestrial deep subsurface bacteria and archaea, and combine this uncertainty with our projection for the uncertainty associated with our estimate of the total biomass of terrestrial deep subsurface bacteria and archaea, which is ≈20-fold.

# In[5]:

deep_fungi = 0.6e15
deep_fungi_CI = CI_prod_prop(np.array([10,20]))


# We combine all the biomass contributions of fungi from the different environments, and combine their uncertainties:

# In[6]:

total_fungi_biomass = soil_fungi_biomass + marine_fungi + deep_fungi

print('Our best estimate for the total biomass of fungi is %.f Gt C' %(total_fungi_biomass/1e15))

# Propagate the uncertainty associated with each parameter to the final estimate

mul_CI = CI_sum_prop(np.array([soil_fungi_biomass, marine_fungi, deep_fungi]), np.array([ soil_fungi_biomass_CI, marine_fungi_CI, deep_fungi_CI]))

print('The uncertainty associated with the estimate for the biomass of fungi is %.1f-fold' %mul_CI)


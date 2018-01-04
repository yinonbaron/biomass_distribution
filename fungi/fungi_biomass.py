
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


# We multiply all the relevant parameters to arrive at our best estimate for the biomass of fungi, and propagate the uncertainties associated with each parameter to calculate the uncertainty associated with the estimate for the total biomass

# In[3]:


# Calculate the total biomass of fungi
total_fungi_biomass = np.prod(results['Value'])
print('Our best estimate for the total biomass of fungi is %.f Gt C' %(total_fungi_biomass/1e15))

# Propagate the uncertainty associated with each parameter to the final estimate

fungi_biomass_uncertainty = CI_prod_prop(results['Uncertainty'])

print('The uncertainty associated with the estimate for the biomass of fungi is %.1f-fold' %fungi_biomass_uncertainty)



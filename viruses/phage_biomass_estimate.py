
# coding: utf-8

# # Estimating the biomass of phages
# Our estimate of the total biomass of phages relies upon the estimates for the total number of phages and the carbon content of a single phage which we derived in the relevant sections
# 
# These are our best estimates for the different parameters required for the estimate, along with the associated uncertainties:

# In[1]:

import pandas as pd
import sys
sys.path.insert(0,'../statistics_helper/')
from CI_helper import *
pd.options.display.float_format = '{:,.0e}'.format

# Load estimates for the total number of phages and for the carbon cont
estimate = pd.read_excel('phage_biomass_estimate.xlsx')
estimate


# In order to estimate the total biomass of phages, we multiply our estimate of the total number of phages by our estimate of the carbon content of a single phage.

# In[2]:

best_estimate = estimate['Value'].prod()

print('Our best estimate for the total biomass of phages is %.1f Gt C' %(best_estimate/1e15))


# We propagate the uncertainties associated with each of the parameters to project the uncertainty of our estimate of the total biomass of phages:

# In[3]:

mul_CI = CI_prod_prop(estimate['Uncertainty'])

print('Our best projection for the uncertainty associated with our estiamte of the biomass of phages is %.1f-fold' %mul_CI)


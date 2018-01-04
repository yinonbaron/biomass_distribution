
# coding: utf-8

# # Estimating the total number of phages
# In order to estimate the total number of phages world-wide, we sum our estimates for the total biomass of phages in all of the environments we cover: the marine environment, soils, the marine deep subsurface, and the terrestrial deep subsurface.
# Here is a summary of our estimates for the total number of phages in each of the environments:

# In[1]:


import pandas as pd
import sys
import sys
sys.path.insert(0, '../../statistics_helper/')
from CI_helper import *

pd.options.display.float_format = '{:,.1e}'.format
estimate = pd.read_excel('phage_num_estimate.xlsx')
estimate


# Our best estimate of the total number of phages is the sum of our estimates for the number of phages in all the environments we cover:

# In[2]:


# Calculate the total number of phages
best_estimate = estimate.sum()['Value']

print('Our best estimate for the total number of phages is %.1e' %best_estimate)


# # Uncertainty analysis
# We could only produce projections for the number of phages in soils and in the terrestrial deep subsurface. For the number of phages in the marine environment and in the marine deep subsurface, we did not have a methodology which we believe represents well the uncertainty associated with our estimate. We therefore chose to use an uncertainty of about one and a half orders of magnitude for both the number of phages in the marine environments and in the marine deep subsurface. We hope further studies could come up with a better methodology for assessing the uncertainty of the estimate of the total number of phages in those environments.
# 
# We combine the uncertainties for the number of phages in each of the environments to produce our projection for the uncertainty associated with our estimate of the total number of phages:

# In[3]:


# Set the uncertainty associated with our estimate of the total number of phages
# in the marine environment and in the marine deep subsurface as one and a half
# orders of magnitude
estimate.loc[0,'Uncertainty'] = 10**1.5
estimate.loc[1,'Uncertainty'] = 10**1.5

# Combine the uncertainties for all environments to produce our best projection
mul_CI = CI_sum_prop(estimates=estimate['Value'],mul_CIs=estimate['Uncertainty'])

print('Our best projection for the uncertainty associated with our estimate of the total number of phages is %.1f-fold' %mul_CI)


# Our final parameters are:

# In[4]:


print('Our best estimate for the total number of phages : %.0e' % best_estimate)
print('Uncertainty associated with the estiamte of the total number of phages: %.0f-fold' % mul_CI)

old_results = pd.read_excel('../phage_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[0] = pd.Series({
                'Parameter': 'Total number of phages',
                'Value': best_estimate,
                'Units': 'Number of individuals',
                'Uncertainty': mul_CI
                })

result.to_excel('../phage_biomass_estimate.xlsx',index=False)


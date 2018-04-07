
# coding: utf-8

# In[1]:

# Load dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean
import sys
sys.path.insert(0, '../statistics_helper/')
from CI_helper import *
from excel_utils import *


# # Estimating the total biomass of bacteria & archaea
# To estimate the total biomass of bacteria & archaea, we conbine our estimates for the biomass of each environment, which we calculated in each subdirectory. Our estimates for the biomass of each animal taxon are:

# In[2]:

data = pd.read_excel('../results.xlsx','Table1 & Fig1',index_col=[0,1])
data.loc[['Bacteria','Archaea']]


# We sum all these different contributions to produce our best estimate for the biomass of animals:

# In[3]:

best_estimate_bac = data.loc['Bacteria','Biomass [Gt C]'].sum()
best_estimate_arch = data.loc['Archaea','Biomass [Gt C]'].sum()

print('Our best estimate for the biomass of bacteria is ≈%.1f Gt C' %best_estimate_bac)
print('Our best estimate for the biomass of archaea is ≈%.1f Gt C' %best_estimate_arch)


# # Uncertainty analysis
# To project the uncertainty associated with our estimate of the total biomass of animals, we combine the uncertainties of the estimates for which is have uncertainty projections, namely arthropods (marine and terrestrial), fish and wild mammals.

# In[4]:

mul_CI_bac = CI_sum_prop(estimates=data.loc['Bacteria','Biomass [Gt C]'].values, mul_CIs = data.loc['Bacteria','Uncertainty'].values)
mul_CI_arch = CI_sum_prop(estimates=data.loc['Archaea','Biomass [Gt C]'].values, mul_CIs = data.loc['Archaea','Uncertainty'].values)

print('Our projection for the uncertainty of our estimate of the total biomass of bacteria is ≈%.0f-fold' %mul_CI_bac)
print('Our projection for the uncertainty of our estimate of the total biomass of archaea is ≈%.0f-fold' %mul_CI_arch)


# In[5]:

# Feed bacteria results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Bacteria','Terrestrial deep subsurface'), 
               col=['Total biomass [Gt C]', 'Total uncertainty'],
               values=[best_estimate_bac,mul_CI_bac],
               path='../results.xlsx')

# Feed archaea results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Archaea','Terrestrial deep subsurface'), 
               col=['Total biomass [Gt C]', 'Total uncertainty'],
               values=[best_estimate_arch,mul_CI_arch],
               path='../results.xlsx')


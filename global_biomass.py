
# coding: utf-8

# In[1]:


# Load dependencies
# Load dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean
import sys
sys.path.insert(0, 'statistics_helper/')
from CI_helper import *
from excel_utils import *


# # Estimating the total biomass on Earth
# To estimate the total biomass on Earth, we sum all of the contributions from each of the taxa. Here are our estimate of the total biomass of each taxon:

# In[2]:


results = pd.read_excel('results.xlsx','Table1 & Fig1', index_col=[0,1])
results


# In[3]:


best_estimate = results['Biomass [Gt C]'].sum()
print('Our best estimate for the global biomass on Earth is ≈%.d Gt C' %round(best_estimate,-1))


# # Uncertainty analysis
# To project the uncertainty associated with our estimate of the total biomass on Earth, we sum the biomass of the different kingdoms of life and take into account the uncertainty in our estimates of their biomass:

# In[4]:


kingdoms = results.groupby(level=0).apply(sum).drop('Total biomass')

mul_CI = CI_sum_prop(estimates=kingdoms['Biomass [Gt C]'], mul_CIs=kingdoms['Total uncertainty'])
print('Our best projection for the uncertainty associated with our estimate of the total biomass on Earth is ≈%.1f-fold' %mul_CI)


# In[5]:


update_results(path='results.xlsx', sheet='Table1 & Fig1',row = ('Total biomass','Total biomass'), col='Total uncertainty', values=mul_CI)


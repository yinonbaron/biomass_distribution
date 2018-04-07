
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


# # Estimating the total biomass of animals
# To estimate the total biomass of animals, we conbine our estimates for the biomass of each animal taxon, which we calculated in each subdirectory. Our estimates for the biomass of each animal taxon are:

# In[2]:

data = pd.read_excel('animal_biomass_estimate.xlsx')
data


# We sum all these different contributions to produce our best estimate for the biomass of animals:

# In[3]:

best_estimate = data['Biomass [Gt C]'].sum()

print('Our best estimate for the biomass of animals is ≈%.1f Gt C' %best_estimate)


# # Uncertainty analysis
# To project the uncertainty associated with our estimate of the total biomass of animals, we combine the uncertainties of the estimates for which is have uncertainty projections, namely arthropods (marine and terrestrial), fish and wild mammals.

# In[4]:

mul_CI = CI_sum_prop(estimates=data.loc[~np.isnan(data['Uncertainty']),'Biomass [Gt C]'].values, mul_CIs = data.loc[~np.isnan(data['Uncertainty']),'Uncertainty'].values)

print('Our projection for the uncertainty of our estimate of the total biomass of animals is ≈%.0f-fold' %mul_CI)


# In[5]:

# Feed results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Animals','Annelids'), 
               col=['Total biomass [Gt C]', 'Total uncertainty'],
               values=[best_estimate,mul_CI],
               path='../results.xlsx')


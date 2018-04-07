
# coding: utf-8

# In[1]:

# Load dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean
import sys
sys.path.insert(0, '../../statistics_helper/')
from CI_helper import *
from excel_utils import *


# # Estimating the total biomass of chordates
# To estimate the total biomass of animals, we conbine our estimates for the biomass of marine and terrestrial arthropods. Our estimates for the biomass of terrestrial and marine arthropods are:

# In[2]:

data = pd.read_excel('../animal_biomass_estimate.xlsx',index_col=0)
chord_biomass = data.loc[['Fish','Livestock','Wild birds', 'Wild mammals', 'Humans']]
chord_biomass


# We sum all these different contributions to produce our best estimate for the biomass of animals:

# In[3]:

best_estimate = chord_biomass['Biomass [Gt C]'].sum()

print('Our best estimate for the biomass of arthropods is ≈%.0f Gt C' %best_estimate)


# # Uncertainty analysis
# To project the uncertainty associated with our estimate of the total biomass of animals, we combine the uncertainties of the estimates for which is have uncertainty projections, namely arthropods (marine and terrestrial), fish and wild mammals.

# In[4]:

mul_CI = CI_sum_prop(estimates=chord_biomass.loc[~np.isnan(chord_biomass['Uncertainty']),'Biomass [Gt C]'].values, mul_CIs = chord_biomass.loc[~np.isnan(chord_biomass['Uncertainty']),'Uncertainty'].values)

print('Our projection for the uncertainty of our estimate of the total biomass of animals is ≈%.0f-fold' %mul_CI)


# In[5]:

# Feed results to Fig. S2-S3
update_figs2s3(row='Chordates', 
               col='Uncertainty',
               values=mul_CI,
               path='../../results.xlsx')


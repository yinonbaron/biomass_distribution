
# coding: utf-8

# In[1]:

# Load dependencies
import pandas as pd
import sys
sys.path.insert(0,'../statistics_helper/')
from CI_helper import *
pd.options.display.float_format = '{:,.0e}'.format
from excel_utils import *


# # Estimating the biomass of phages
# Our estimate of the total biomass of phages relies upon the estimates for the total number of phages and the carbon content of a single phage which we derived in the relevant sections
# 
# These are our best estimates for the different parameters required for the estimate, along with the associated uncertainties:

# In[2]:

# Load estimates for the total number of phages and for the carbon cont
estimate = pd.read_excel('phage_biomass_estimate.xlsx')
estimate


# In order to estimate the total biomass of phages, we multiply our estimate of the total number of phages by our estimate of the carbon content of a single phage.

# In[3]:

best_estimate = estimate['Value'].prod()

print('Our best estimate for the total biomass of phages is %.1f Gt C' %(best_estimate/1e15))


# We propagate the uncertainties associated with each of the parameters to project the uncertainty of our estimate of the total biomass of phages:

# In[4]:

mul_CI = CI_prod_prop(estimate['Uncertainty'])

print('Our best projection for the uncertainty associated with our estiamte of the biomass of phages is %.1f-fold' %mul_CI)


# Due to the scarcity of data on the different parameters used to estimate the total biomass of phages, we use a higher uncertainty projection of ≈20-fold.

# In[5]:

mul_CI = 20

# Feed results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Viruses','Viruses'), 
               col=['Biomass [Gt C]', 'Uncertainty','Total uncertainty'],
               values=[best_estimate/1e15,mul_CI,mul_CI],
               path='../results.xlsx')


# Feed results to Table S1
update_results(sheet='Table S1', 
               row=('Viruses','Viruses'), 
               col=['Number of individuals'],
               values=estimate.loc[1,'Value'],
               path='../results.xlsx')

# Calculate non-deep subsurface virus biomass
phage_num = pd.read_excel('phage_num/phage_num_estimate.xlsx')
non_deep_phage = phage_num.loc[[0,2],'Value'].sum()*estimate.loc[0,'Value']

# Feed results to Fig S1
update_results(sheet='FigS1', 
               row=('Viruses','Viruses'), 
               col=['Biomass [Gt C]'],
               values=non_deep_phage/1e15,
               path='../results.xlsx')


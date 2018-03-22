
# coding: utf-8

# In[1]:


# Load dependencies
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, '../statistics_helper')
from CI_helper import *
from excel_utils import *
pd.options.display.float_format = '{:,.1e}'.format


# # Estimating the total biomass of fungi
# We use our best estimates for the total biomass of soil microbes and the fraction of fungi out of the total biomass of soil microbes to estimate the total biomass of fungi.

# In[2]:


results = pd.read_excel('fungi_biomass_estimate.xlsx')


# These are our best estimates for the different parameters required for the estimate, along with the associated uncertainties

# In[3]:


results


# In[4]:


# Calculate the total biomass of fungi
soil_fungi_biomass = results.loc[[0,1],'Value'].prod()
print('Our best estimate for the total biomass of soil fungi is %.f Gt C' %(soil_fungi_biomass/1e15))

# Propagate the uncertainty associated with each parameter to the final estimate

soil_fungi_biomass_CI = CI_prod_prop(results.loc[[0,1],'Uncertainty'])

print('The uncertainty associated with the estimate for the biomass of soil fungi is %.1f-fold' %soil_fungi_biomass_CI)


# We multiply all the relevant parameters to arrive at our best estimate for the biomass of fungi, and propagate the uncertainties associated with each parameter to calculate the uncertainty associated with the estimate for the total biomass. 

# We add to the our estimate of the biomass of soil fungi our estimates for the contribution of marine and deep subsurface fungi. For marine fungi, we project an uncertainty of 10-fold (similar to our uncertainties for other marine taxa.

# In[5]:


marine_fungi = results.loc[2,'Value']
marine_fungi_CI = results.loc[2,'Uncertainty']


# We combine all the biomass contributions of fungi from the different environments, and combine their uncertainties:

# In[6]:


total_fungi_biomass = soil_fungi_biomass + marine_fungi

print('Our best estimate for the total biomass of fungi is %.f Gt C' %(total_fungi_biomass/1e15))

# Propagate the uncertainty associated with each parameter to the final estimate

mul_CI = CI_sum_prop(np.array([soil_fungi_biomass, marine_fungi]), np.array([ soil_fungi_biomass_CI, marine_fungi_CI]))

print('The uncertainty associated with the estimate for the biomass of fungi is %.1f-fold' %mul_CI)


# # Estimating the total number of fungal cells
# To estimate the total number of fungal cells we divide our biomass estimate by an average carbon
# content per fungal cell. We very roughly estimate the volume of fungal cells to be ≈100 μm$^3$
# based on [Veses et al.](https://doi.org/10.1111/j.1365-2958.2008.06545.x), and thus we estimate a carbon content of a cell to be ≈15 pg C cell$^{-1}$.
# 

# In[7]:


# Carbon content of a single fungal cell based on Veses et al.
carbon_content = 15e-12

# Calculate the total number of fungal cells
soil_fungi_num = soil_fungi_biomass/carbon_content
marine_fungi_num = marine_fungi/carbon_content
print('Our best estimate for the total number of fungal cells is ≈%.0e.' %(soil_fungi_num+marine_fungi_num))


# In[8]:


# Feed soil fungi results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Fungi','Terrestrial'), 
               col=['Biomass [Gt C]', 'Uncertainty','Total uncertainty'],
               values=[soil_fungi_biomass/1e15,soil_fungi_biomass_CI, mul_CI],
               path='../results.xlsx')

# Feed marine fungi results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Fungi','Marine'), 
               col=['Biomass [Gt C]', 'Uncertainty'],
               values=[marine_fungi/1e15,marine_fungi_CI],
               path='../results.xlsx')

# Feed soil fungi results to Table S1
update_results(sheet='Table S1', 
               row=('Fungi','Terrestrial'), 
               col=['Number of individuals'],
               values=soil_fungi_num,
               path='../results.xlsx')

# Feed marine fungi results to Table S1
update_results(sheet='Table S1', 
               row=('Fungi','Marine'), 
               col=['Number of individuals'],
               values=marine_fungi_num,
               path='../results.xlsx')



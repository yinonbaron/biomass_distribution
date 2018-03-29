
# coding: utf-8

# In[1]:


# Load dependencies
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '../../statistics_helper')
from fraction_helper import *
pd.options.display.float_format = '{:,.3f}'.format


# # Estimating the fraction of fungi out of the biomass of soil microbes
# Our estimate for the fraction of fungi out of the biomass of soil microbes is based on a study by [Joergensen & Wichern ](http://dx.doi.org/10.1016/j.soilbio.2008.08.017). Joergensen & Wichern survey the fraction of fungi out of the total microbial biomass using several independent methods. The data in Joergensen & Wichern contains measurements of the fraction of fungi out of the total biomass of soil microbes in four differennt soil types - arable soil, forest soil, grassland soil and litter. We rely on measurement collected in these four soil types using two independent methods - microscopy and measurement of cell wall components.
# 
# Here is a sample of the data from Joergensen & Wichern:

# In[2]:



data = pd.read_excel('fungi_fraction_data.xlsx')
data.head()


# Our general methodology for calculating the fraction of fungi out of the biomass of soil microbes is the following. We calculate the geometric mean of all values reported from the same soil type using the same method. This gives us estimates for characteric fraction of fungi in each soil type for each method. 

# In[3]:


def groupby_geo_frac_mean(input):
    return frac_mean(input['Fraction'],weights=input['N'])

type_method_mean = data.groupby(['Method','Type']).apply(groupby_geo_frac_mean).unstack(level=0)
type_method_mean


# We then calculate the geometric mean of the characteristic fractions from different soil types using the same method. This gives us a characteristic fraction of fungi for each of the two methods.

# In[4]:


method_mean = type_method_mean.apply(frac_mean)
method_mean


# In the last stage, we calculate the geometric mean of the characteristic values from the two methods. We use the geometric mean as our best estimate for the fraction of fungi out of the total biomass of soil microbes.

# In[5]:


best_estimate = frac_mean(method_mean)
print('Our best estimate for the fraction of fungi out of the total biomass of fungi is ≈' + '{:,.0f}%'.format(best_estimate*100))


# # Uncertainty analysis
# 
# To calculate the uncertainty associated with the estimate for the fraction of fungi out of the total biomass of number of of bacteria and archaea, we first collect all available uncertainties and then take the largest value as our best projection for the uncertainty.
# 
# **Variability of studies using the same method and done in the same soil type** <br>
# We calculate the 95% confidence confidence interval of the values reported by studies performed in the same soil type and using the same method.
# 

# In[6]:


def groupby_frac_CI(input):
    return frac_CI(input['Fraction'])

type_method_CI = data.groupby(['Method','Type']).apply(groupby_frac_CI).unstack(level=0)
type_method_CI


# **Variability of fractions from different soil types measured using the same method** <br>
# We calculate the 95% confidence interval of the characteristic values from each soil type measured in the same method.

# In[7]:


intra_method_CI = type_method_mean.apply(frac_CI)
intra_method_CI


# **Variability of fraction measured using different methods** <br>
# We calculate the 95% confidence interval of the characteristic values from each method.

# In[8]:


inter_method_CI = frac_CI(method_mean)
print('The 95' + '%'+' confidence interval of the characteristic values from each method is ≈%.1f-fold' % inter_method_CI)


# We choose the highest uncertainty among the uncertianties we collected which is ≈3-fold, as our projection for the uncertainty of the fraction of fungi out of the total biomass of soil microbes.
# Our final parameters are:

# In[9]:


mul_CI = np.max([type_method_CI.values.flatten().max(),intra_method_CI.max(),inter_method_CI])
print('Fraction of fungi out of the total biomass of microbes:' +'{:.1f}%'.format(best_estimate*100))
print('Uncertainty associated with the estimate of the total biomass of soil microbes ≈%.1f-fold' % mul_CI)

old_results = pd.read_excel('../fungi_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[1] = pd.Series({
                'Parameter': 'Fraction of fungi ou out the total biomass of soil microbes',
                'Value': '{0:.1f}'.format(best_estimate),
                'Units': 'Unitless',
                'Uncertainty': "{0:.1f}".format(mul_CI)
                })

result.to_excel('../fungi_biomass_estimate.xlsx',index=False)


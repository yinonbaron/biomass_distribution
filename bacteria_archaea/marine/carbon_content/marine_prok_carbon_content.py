
# coding: utf-8

# In[1]:

# Load dependencies
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '../../../statistics_helper')
from CI_helper import *
pd.options.display.float_format = '{:,.1f}'.format


# # Estimating the carbon content of marine bacteria and archaea

# In order to estimate the characteristic carbon content of marine bacteria and archaea, we collected data on the carbon content of marine prokaryotes from 5 studies. Here is a summary of the data collected

# In[2]:

summary = pd.read_excel('marine_prok_carbon_content_data.xlsx','Summary')
summary.head()


# We use the geometric mean of the carbon content from each study as our best estimate for the carbon content of marine bacteria and archaea.

# In[3]:

best_estimate = 10**(np.log10(summary['fg C cell-1']).mean())
print('Our best estimate for the carbon content of marine bacteria and arcaea is %0.1f fg C cell^-1' % best_estimate)


# # Uncertainty analysis
# 
# In order to assess the uncertainty associated with our estimate of the carbon content of marine bacteria and archaea, we survey all availabe measures of uncertainty.
# 
# ## Intra-study uncertainty
# We collected the uncertainties reported in each of the studies. Below is a list of the uncertainties reported in each of the studies. The highest uncertainty reported is lower than 1.5-fold.

# In[4]:

print(summary[['Reference','Intra-study uncertainty']])


# ## Interstudy uncertainty
# We estimate the 95% multiplicative confidence interval around the geometric mean of the values from the different studies. 

# In[5]:

mul_CI = geo_CI_calc(summary['fg C cell-1'])
print('The interstudy uncertainty is ≈%.1f-fold' % mul_CI)


# We thus take the highest uncertainty from our collection of intra-study and interstudy uncertainties which is ≈1.4-fold.
# Our final parameters are:

# In[6]:

print('Carbon content of marine bacteria and archaea: %.1f fg C cell^-1' % best_estimate)
print('Uncertainty associated with the carbon content of marine bacteria and archaea: %.1f-fold' % mul_CI)

old_results = pd.read_excel('../marine_prok_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[1] = pd.Series({
                'Parameter': 'Carbon content',
                'Value': "{0:.1f}".format(best_estimate),
                'Units': 'fg C cell^-1',
                'Uncertainty': "{0:.1f}".format(mul_CI)
                })

result.to_excel('../marine_prok_biomass_estimate.xlsx',index=False)


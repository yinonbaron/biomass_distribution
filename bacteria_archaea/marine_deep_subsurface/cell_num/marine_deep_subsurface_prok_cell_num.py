
# coding: utf-8

# In[1]:


# Load dependencies
import pandas as pd
import numpy as np
import sys
from scipy.stats import gmean
sys.path.insert(0, '../../../statistics_helper')
from CI_helper import *


# # Estimating the total number of bacteria and archaea in the marine deep subsurface
# In order to estimate the total number of cells of bacteria and archaea in the marine deep subsurface, we rely of estimates from two studies - [Parkes et al.](http://www.sciencedirect.com/science/article/pii/S0025322714000425), and [Kallmeyer et al.](http://dx.doi.org/10.1073/pnas.1203849109). Our best esimate for the total number of cells of bacteria and archaea in the marine deep subsurface is the geometric mean of the estimates by Parkes et al. and Kallmeyer et al.

# In[2]:


#Kallmeyer et al. estimate ≈2.9×10^29 cells in the marine deep subsurface
kallmeyer = 2.9e29
#Parkes et al. estimate ≈5.4×10^29 cells in the marine deep subsurface
parkes = 5.4e29

best_estimate = gmean([kallmeyer,parkes])
print('Our best estimate for the total number of cells of bacteria and archaea the marine deep subsurface is %.1e.' % best_estimate)


# # Uncertainty analysis
# 
# To calculate the uncertainty associated with the estimate for the total number of of bacteria and archaea in the marine deep subsurface, we first collect all available uncertainties and then take the largest value as our best projection for the uncertainty. 
# 
# ## Intra-study uncertainty
# We survey the uncertainties reported in Parkes et al. and Kallmeyer et al. for their estimates of the total number of cells in the marine deep subsurface.
# Parkes et al. reports a 95% confidence interval of $1.95×10^{29}-4.35×10^{30}$ with a mean of $8.65×10^{29}$ excluding contribution from Ocean Gyre sites, and a mean of $5.39×10^{29}$. As we do not know the 95% confidence interval of the estimate including Ocean Gyre sites, we use the 95% confidence interval from the estimate excluding Ocean Gyre sites as a measure of the intra-study uncertainty of the estimate of the total number of bacteria and archaea in the marine deep subsurface. We report uncertainty as a multiplicative factor, so we calculate the fold change of the minimal and maximal values in the 95% confidence interval relative to the mean estiamte and use this value as the intra-study uncertainty of Parkes et al.

# In[3]:


parkes_low = 1.95e29
parkes_high = 4.34e30
parkes_mean_ex_ocean_gyre = 8.65e29

# We calculate the fold change in the minimum and maximum of the 95% confidence interval relative to the mean estimate
parkes_high_mul_CI = parkes_high/parkes_mean_ex_ocean_gyre
parkes_low_mul_CI = parkes_mean_ex_ocean_gyre/parkes_low

# We use the average of the fold changes as our estimate for the intra-study uncertainty of the estimate by Parkes et al.
parkes_mul_CI = np.mean([parkes_high_mul_CI,parkes_low_mul_CI])

print('The intra-study uncertainty of the estimate by Parkes et al. is %.1f-fold' % parkes_mul_CI)


# Kallmeyer et al., report an estimate of ≈$2.9×10^{29}$ cells of bacteria and archaea in the marine deep subsurface. Kallmeyer et al. bootstrap the parameters of the model for estimating the total number of cells, which results in a distribution of estimates for the total number of cells. Kallmeyer et al. report a range of one standard deviation from the mean estimate of ≈$1.2×10^{29}-≈8×10^{29}$. We use this range as a measure of the intra-study uncertainty of the estimate by Kallmeyer et al. As Kallmeyer et al. only reports a standard deviation range, we convert this range to 95% multiplicative confidence interval by calculating the fold change of the minimum and maximum of the range relative to the average estimate by Kallmeyer et al., and taking this fold change to the power of 1.96 to move from one standard deviation to 95% confidence interval.

# In[4]:


kallmeyer_low = 1.2e29
kallmeyer_high = 8e29

# We calculate the fold change in the minimum and maximum of the standard deviation range relative to the mean estimate
kallmeyer_high_mul_std = (kallmeyer_high/kallmeyer)
kallmeyer_low_mul_std = (kallmeyer/kallmeyer_low)

# We use the average of the fold changes as our estimate for the intra-study uncertainty of the estimate by Parkes et al.
kallmeyer_mul_CI = np.mean([kallmeyer_high_mul_std,kallmeyer_low_mul_std])**1.96
print('The intra-study uncertainty of the estimate by Kallmeyer et al. is %.1f-fold' % kallmeyer_mul_CI)


# ## Interstudy uncetainty
# We calculate the 95% confidence interval of the geometric mean of the estimates by Parkes et al. and Kallmeyer et al. as a measure of the interstudy uncertainty.

# In[5]:


inter_mul_CI = geo_CI_calc(np.array([parkes,kallmeyer]))

print('The interstudy uncertainty of the geometric mean of the estimates by Parkes et al. and Kallmeyer et al. is %.1f-fold' % inter_mul_CI)


# We use the highest uncertainty among the intra-study and interstudy uncertainties as our projection of the uncertainty associated with the estimate of the total number of cells of bacteria and archaea in the marine deep subsurface. Are final parameters are:

# In[6]:


# Take the maximal uncetainty as our best projection of uncertainty
mul_CI = np.max([parkes_mul_CI,kallmeyer_mul_CI,inter_mul_CI])

print('Total number of bacteria and archaea in the marine deep subsurface: %.1e' % best_estimate)
print('Uncertainty associated with the total number of bacteria and archaea in the marine deep subsurface: %.1f-fold' % mul_CI)

old_results = pd.read_excel('../marine_deep_subsurface_prok_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[0] = pd.Series({
                'Parameter': 'Total number of bacteria and archaea in the marine deep subsurface',
                'Value': best_estimate,
                'Units': 'Cells',
                'Uncertainty': "{0:.1f}".format(mul_CI)
                })

result.to_excel('../marine_deep_subsurface_prok_biomass_estimate.xlsx',index=False)


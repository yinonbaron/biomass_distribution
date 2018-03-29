
# coding: utf-8

# In[1]:


# Load dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean
import sys
sys.path.insert(0, '../../../statistics_helper')
from CI_helper import *
pd.options.display.float_format = '{:,.2f}'.format


# # Estimating the carbon content of marine bacteria and archaea
# 
# In order to estimate the characteristic carbon content of marine bacteria and archaea, we rely on two main methodologies - volume based estimates and amino acid based estimates.
# 
# ## Volume-based estimates
# We collected measurements of the characeteristic volume of bacteria and archaea in the marine deep subsurface from 4 different studies. For 3 of those studies, we collected reported average cell volumes. Here are the average values we collected from those three studies:

# In[2]:


volumes = pd.read_excel('marine_deep_subsurface_prok_carbon_content_data.xlsx','Volume based')
volumes


# In addition we used data from [Braun et al.](http://dx.doi.org/10.3389/fmicb.2016.01375) which measured cell volumes for three cell morphologies (coccoid, elongated and filamentous), along with the relative fraction of each morphology in each site sampled. Here is the data extracted from Braun et al.:

# In[3]:


braun_volumes = pd.read_excel('marine_deep_subsurface_prok_carbon_content_data.xlsx','Braun', skiprows=1)
braun_volumes


# We first calculate the characteristic volume of a single cell from the data in Braun et al. to be able to compare it with the other resources:

# In[4]:


# Group by depth

braun_depth_binned = braun_volumes.groupby(['Depth (m)'])

# Define the function which will to the weighted average of volume based on the fraction of the
# population of each cell type

def groupby_weighted_average(input):
    return np.average(input['Mean volume (µm^3)'],weights=input['Fraction FM'])

# Calculate the weighted average volume for each depth sample
braun_weighted_average = braun_depth_binned.apply(groupby_weighted_average)

# Calculate the geometric mean of the volumes from different depths
braun_characteristic_volume = gmean(braun_weighted_average)
print(r'The characteristic volume of bacterial and archaeal cells in the marine deep subsurface based on Braun et al. is ≈%.2fµm^3' %braun_characteristic_volume)
volumes.append(pd.DataFrame.from_dict([{'Study': 'Braun et al.', 'Mean cell volume (µm^3)':braun_characteristic_volume}]))


# In order to covert the five different estimates for the characteristic volume of bacterial and archaeal cell in the marine deep subsurface into estimates of carbon content, we use two independent models that have been used in the literature: [Fry et al.](http://dx.doi.org/10.1016/S0580-9517(08)70239-3) which estimates ≈300 fg C per $µm^3$, and [Simon & Azam](http://dx.doi.org/10.3354/meps051201), which developed an allometric model of the carbon content of cells with different volumes. The allometric model they developed is:
# $$C = 88.1 \times V^{0.59}$$
# Where C is the carbon content of a single cell [fg C cell$^{-1}$], and V is cell volume [$µm^3$]. We apply these two independent conversion equations to the volumes we gathered from the literature to produce 10 estimates for the characteristic carbon content of bacterial and archaeal cells in the marine deep subsurface.

# In[5]:


# Apply the conversion equations to the volumes reported in the literature
volumes['Fry et al.'] = volumes['Mean cell volume (µm^3)']*310
volumes['Simon and Azam'] = 88.1*volumes['Mean cell volume (µm^3)']**0.59

volumes


# We calculate the geometric mean of the values from different studies using the same conversion equation to generate a characteristic carbon content for each conversion method.

# In[6]:


fry_volume_mean = gmean(volumes['Fry et al.'])
sa_volume_mean = gmean(volumes['Simon and Azam'])

print('The characteristic carbon content of a single bacterial or archaeal cell in the marine deep subsurface based on cell volume converted using the conversion equation from Fry et al. is ≈%.0f fg C cell^-1\n' %fry_volume_mean)
print('The characteristic carbon content of a single bacterial or archaeal cell in the marine deep subsurface based on cell volume converted using the conversion equation from Simon & Azam is ≈%.0f fg C cell^-1' %sa_volume_mean)


# We compute the geometric mean of the characteristic values from the two volume to carbon content conversion methods and use it as our best estimate for the carbon content of bacterial and archaeal cells in the marine deep subsurface, based on volume measurements.

# In[7]:


vol_best_carbon_content = gmean([fry_volume_mean,sa_volume_mean])
print('Our best volume-based estimate for the carbon content of bacterial and archaeal cells in the marine deep subsurface is %.0f fg C cell^-1' %vol_best_carbon_content)


# ## Amino acid-based estimate
# We rely on the study by Braun et al., which measured carobon content of bacterial and archaeal cells in the marine deep subsurface based on amino acid carbon mass, and assuming ≈55% of the carbon mass of single cells is stored in amino acids. Here are the values reported by Braun et al.:

# In[8]:


aa_based = pd.read_excel('marine_deep_subsurface_prok_carbon_content_data.xlsx', 'Amino acid based', skiprows=1)
aa_based


# We use the geometric mean of the values reported by Braun et al. as our best estimate for the amino acid-based estimate of the carbon content of bacterial and archaeal cells in the marine deep subsurface.

# In[9]:


aa_best_carbon_content = gmean(aa_based['Carbon content (fg C cell-1)'])

print('Our best amino acid-based estimate for the carbon content of bacterial and archaeal cells in the marine deep subsurface is %.0f fg C cell^-1' %aa_best_carbon_content)


# As our best estimate for the carbon content of bacterial and archaeal cells in the marine deep subsurface, we use the geometric mean of the volume-based and amino acid-based estimates.

# In[10]:


best_estimate = gmean([vol_best_carbon_content,aa_best_carbon_content])
print('Our best estimate for the carbon content of bacterial and archaeal cells in the marine deep subsurface is %.0f fg C cell^-1' %best_estimate)


# # Uncertainty analysis
# To calculate the uncertainty associated with the estimate for the total number of of bacteria and archaea in the marine deep subsurface, we first collect all available uncertainties and then take the largest value as our best projection for the uncertainty. 
# 
# ## Volume-based
# 
# ### intra-study uncertainty
# For the volume based approaches, we had data on intra-study uncertainty only for the Braun et al. study. We calculate the intra study uncertainty of the volumes reported in Braun et al. by calculating the 95% confidence interval of the values reported in Braun et al.

# In[11]:


vol_braun_intra_CI = geo_CI_calc(braun_weighted_average)
print('The intra-study uncertainty for Braun et al. is ≈%.1f-fold' %vol_braun_intra_CI)


# ### Interstudy uncertainty
# As a measure of the interstudy uncertainty, we compare the 95% confidence interval for the geometric mean of the carbon content from different studies, using the same conversion method.
# We also use the 95% confidence interval for the geometric mean of the carbon content estimates from the two different conversion methods (Fry et al. and Simon & Azam) as a measure of interstudy uncertainty.

# In[12]:


carbon_content_fry_CI = geo_CI_calc(volumes['Fry et al.'])
carbon_content_sa_CI = geo_CI_calc(volumes['Simon and Azam'])
print('The interstudy uncertainty of the geometric mean of carbon content using the conversion method of Fry et al. is ≈%.1f-fold' %carbon_content_fry_CI)
print('The interstudy uncertainty of the geometric mean of carbon content using the conversion method of Simon & Azam is ≈%.1f-fold' %carbon_content_sa_CI)

carbon_content_vol_CI = geo_CI_calc([fry_volume_mean,sa_volume_mean])
print('The interstudy uncertainty of the geometric mean of carbon content between conversion methods is ≈%.1f-fold' %carbon_content_vol_CI)


# ## Amino acid-based
# 
# ### Intra-study uncertainty
# We calculate the 95% confidence interval of the geometric mean of values for the carbon content from Braun et al. as a measure of the intra-study uncertainty.

# In[13]:


aa_intra_CI = geo_CI_calc(aa_based['Carbon content (fg C cell-1)'])
print('The intra-study uncertainty of amino acid-based carbon content estimates from Braun et al. is ≈%.1f-fold' %aa_intra_CI)


# ## Inter-method uncertainty
# As another measure of uncertainty we calculate the 95% confidence interval of the geometric mean of the estimates for carbon content calculated using either the volume-based method or the amino acid-based method.

# In[14]:


inter_method_CI = geo_CI_calc([vol_best_carbon_content,aa_best_carbon_content])
print('The intra-method uncertainty for the caron content of bacretial and archaeal cells in the marine deep subsurface is  ≈%.1f-fold' %inter_method_CI)


# We use the highest uncertainty among this collection, which is ≈2.2-fold, as our best projection of the uncertainty associated with our estimate of the carbon content of bacterial and archaeal cells in the marine deep subsurface.
# 
# Our final parameters are:

# In[15]:


# Take the maximal uncetainty as our best projection of uncertainty
mul_CI = np.max([inter_method_CI,aa_intra_CI,carbon_content_vol_CI,carbon_content_fry_CI,carbon_content_sa_CI,vol_braun_intra_CI])

print('Carbon content of bacterial and archaeal cells in the marine deep subsurface: %.0f fg C' % best_estimate)
print('Uncertainty associated with the carbon content of bacterial and archaeal cells in the marine deep subsurface: %.1f-fold' % mul_CI)

old_results = pd.read_excel('../marine_deep_subsurface_prok_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[1] = pd.Series({
                'Parameter': 'Carbon content of bacterial and archaeal cells in the marine deep subsurface',
                'Value': int(best_estimate),
                'Units': 'fg C cell^-1',
                'Uncertainty': "{0:.1f}".format(mul_CI)
                })

result.to_excel('../marine_deep_subsurface_prok_biomass_estimate.xlsx',index=False)


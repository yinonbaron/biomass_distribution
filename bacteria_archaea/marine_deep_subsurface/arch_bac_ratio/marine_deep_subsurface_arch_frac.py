
# coding: utf-8

# In[1]:

# Load dependencies
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '../../../statistics_helper')
from fraction_helper import *
pd.options.display.float_format = '{:,.1e}'.format

# Genaral parameters used in the estimate
ocean_area = 3.6e14
liters_in_m3 = 1e3
ml_in_m3 = 1e6


# # Estimating the fraction of archaea out of the total marine deep subsurface prokaryote population
# 
# In order to estimate the fraction of archaea out of the total population of marine deep subsurface bacteria and archaea, we rely of two independent methods:  catalyzed reporter deposition fluorescent in-situ hybridization (CARD-FISH) and quantitative PCR (qPCR). Both methods have been found reliable for reporting the fraction of archaea out of the population of marine deep subsurface bacteria and archaea
# 
# ### CARD-FISH based estimate
# For our CARD-FISH based estimate we rely on data from [Lloyd et al.](http://dx.doi.org/10.1128/AEM.02090-13). Here is a sample of the data:

# In[2]:

# Load the dataset
lloyd = pd.read_excel('marine_deep_subsurface_arch_frac_data.xlsx','Lloyd',skiprows=1)
lloyd.head()


# We use values reported in Lloyd et al. for sediments deeper than 10 cm and using CARD-FISH with proteinase K permeabilization (this mathod generates reliable results). We calculate the geometric mean fraction of archaea out of the population of archaea and bacteria in this dataset.

# In[3]:

# Filter the data in Lloyd et al. to contain only samples which have been measured in sediments deeper than
# 10 cm and with CARD-FISH with proteinase K permeabilization
# Also remove NaN values and zeros
lloyd_fish = lloyd[(lloyd['Arc permeabilization'] == 'proteinase K') & 
                   (lloyd['Fish or cardFish'] == 'CARDFISH') & 
                   (lloyd['Fraction Arc CARDFISH']>0) &
                   (lloyd['Sediment Depth (m)'] >0.01)]

# Calculate the geometric mean of the fraction of archaea out of the total population of bacteria and archaea
# Remove zeros and NaNs
fish_frac = frac_mean(lloyd_fish['Fraction Arc CARDFISH'])
print('The geometric mean of the fraction of archaea out of the population of bacteria and archaea measured using CARD-FISH is ' + '{:,.0f}%'.format(fish_frac*100))


# ## qPCR-based estimate
# For the qPCR-based estimate of the fraction of archaea out of the total population of marine deep subsurface bacteria and archaea, we also rely on data from Lloyd et al. We also consider only samples deeper than 10 cm. We exclude measurements using the ARCH516 as an archaeal primer or TaqMan probe, as measurements based on these primers of probes were shown to be unreliable.

# In[4]:

# Filter the data in Lloyd et al. to contain only samples which have been measured in sediments deeper than
# 10 cm and not with the ARCH516 as an archaeal primer or TaqMan probe.
# Also remove NaN values and zeros
lloyd_qpcr = lloyd[(~np.isnan(lloyd['Fraction Arc qPCR'])) & 
                   (lloyd['Sediment Depth (m)'] >0.01) &
                   (lloyd['Fraction Arc qPCR']>0) &
                  (lloyd['Arc reverse'].str.contains('516')==False) &
                  (lloyd['Arc forward'].str.contains('519')==False)]
lloyd_qpcr = lloyd_qpcr.drop(lloyd_qpcr['TaqMan Arc'].dropna().index)


# Calculate the geometric mean of the fraction of archaea out of the total population of bacteria and archaea
qpcr_frac = frac_mean(lloyd_qpcr['Fraction Arc qPCR'])
print('The geometric mean of the fraction of archaea out of the population of bacteria and archaea measured using qPCR is ' + '{:,.0f}%'.format(qpcr_frac*100))


# Our best estimate for the fraction of archaea out of the total population of marine deep subsurface bacteria and archaea is the geometric mean of the estimates based on CARD-FISH and qPCR.

# In[5]:


best_estimate = frac_mean(np.array([fish_frac,qpcr_frac]))
print('Our best estimate for the fraction of archaea out of the population marine deep subsurface bacteria and archaea is ' + '{:,.0f}%'.format(best_estimate*100))


# # Uncertainty analysis
# 
# In order to assess the uncertainty associated with our estimate for the fraction of marine archaea out of the total population of bacteria and archaea in the marine deep subsurface, we gather all possible indices of uncertainty. We compare the uncertainty of values within each one of the methods and the uncertainty stemming from the variability of the values provided by the two methods. 
# 
# ## Intra-method uncertainty 
# ### CARD-FISH-based method
# We calculate the 95% confidence inteval for the geometric mean of the values for the fraction of archaea out of the total population of bacteria and archaea measured using CARD-FISH.

# In[6]:

fish_arc_CI = frac_CI(lloyd_fish['Fraction Arc CARDFISH'])
fish_bac_CI = frac_CI(1-lloyd_fish['Fraction Arc CARDFISH'])
print('The uncertainty of the CARD-FISH-based estimate of the fraction of archaea out of the population of bacteria nad archaea is ≈%.1f-fold' %fish_arc_CI)
print('The uncertainty of the CARD-FISH-based estimate of the fraction of bacteria out of the population of bacteria nad archaea is ≈%.1f-fold' %fish_bac_CI)


# ### qPCR-based method
# We calculate the 95% confidence inteval for the geometric mean of the values for the fraction of archaea out of the total population of bacteria and archaea measured using qPCR.

# In[7]:

qpcr_arc_CI = frac_CI(lloyd_qpcr['Fraction Arc qPCR'])
qpcr_bac_CI = frac_CI(1-lloyd_qpcr['Fraction Arc qPCR'])
print('The uncertainty of the qPCR-based estimate of the fraction of archaea out of the population of bacteria nad archaea is ≈%.1f-fold' %qpcr_arc_CI)
print('The uncertainty of the qPCR-based estimate of the fraction of bacteria out of the population of bacteria nad archaea is ≈%.1f-fold' %qpcr_bac_CI)


# ## Inter-method uncertainty 
# We calculate the 95% confidence inteval for the geometric mean of the estiamtes based on CARD-FISH and qPCR for the fraction of archaea out of the total population of bacteria and archaea. This serves as a measure of the inter-method uncertainty of our estimate.

# In[8]:

inter_arc_CI = frac_CI(np.array([fish_frac,qpcr_frac]))
inter_bac_CI = frac_CI(np.array([1-fish_frac,1-qpcr_frac]))
print('The inter-method uncertainty of the estimate of the fraction of archaea out of the population of bacteria nad archaea is ≈%.1f-fold' %inter_arc_CI)
print('The inter-method uncertainty of the estimate of the fraction of bacteria out of the population of bacteria nad archaea is ≈%.1f-fold' %inter_bac_CI)


# As our best estimates for the uncertainty associated with the fraction of archaea and bacteria out of the total population of marine deep subsurface bacteria and archaea, we use the highest uncertainty out of the available set pf uncertainties we collected.
# 
# The highest inter-method uncertainty for the fraction of archaea is ≈1.6-fold, which is higher than the highest intra-method uncertainty of ≈1.2-fold, so we use ≈1.8-fold as our best projection of the uncertainty associated with the fraction of archaea out of the total population of marine deep subsurface bacteria and archaea. 
# Similarly, the highest inter-method uncertainty for the fraction of bacteria is ≈1.3-fold, which is higher than the highest intra-method uncertainty of ≈1.1-fold, so we use ≈1.3-fold as our best projection of the uncertainty associated with the fraction of bacteria out of the total population of marine deep subsurface bacteria and archaea. 
# 
# Our final parameters are:

# In[9]:

# Take the maximum uncertainty as our best projection of uncertainty
arc_mul_CI = np.max([fish_arc_CI,qpcr_arc_CI,inter_arc_CI])
bac_mul_CI = np.max([fish_bac_CI,qpcr_bac_CI,inter_bac_CI])

print('Fraction of archaea out of the total population of marine deep subsurface bacteria and archaea: %.0f percent' %(best_estimate*100))
print('Fraction of bacteria out of the total population of marine deep subsurface bacteria and archaea: %.0f percent' %(100.-best_estimate*100))
print('Uncertainty associated with the fraction of marine archaea: %.1f-fold' % arc_mul_CI)
print('Uncertainty associated with the fraction of marine bacteria: %.1f-fold' % bac_mul_CI)

old_results = pd.read_excel('../marine_deep_subsurface_prok_biomass_estimate.xlsx')
result = old_results.copy()

if (result.shape[0]==0):
    result = pd.DataFrame(index= range(2), columns=['Parameter','Value','Units','Uncertainty'])

result.loc[2] = pd.Series({
                'Parameter': 'Fraction of archaea',
                'Value': "{0:.1f}".format(best_estimate),
                'Units': 'Unitless',
                'Uncertainty': "{0:.1f}".format(arc_mul_CI)
                })

result.loc[3] = pd.Series({
                'Parameter': 'Fraction of bacteria',
                'Value': "{0:.1f}".format(1.0 - best_estimate),
                'Units': 'Unitless',
                'Uncertainty': "{0:.1f}".format(bac_mul_CI)
                })


result.to_excel('../marine_deep_subsurface_prok_biomass_estimate.xlsx',index=False)


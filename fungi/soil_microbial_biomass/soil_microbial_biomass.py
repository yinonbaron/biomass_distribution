
# coding: utf-8

# In[1]:


# Load dependencies
from scipy.stats import gmean
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '../../statistics_helper')
from CI_helper import *
from fraction_helper import *
pd.options.display.float_format = '{:,.1f}'.format


# # Estimating the biomass of soil microbes
# 
# In order to estimate the total biomass of soil microbes, we rely on two recent studies - [Xu et al.](http://dx.doi.org/10.1111/geb.12029) and [Serna-Chavez et al.](http://dx.doi.org/10.1111/geb.12070)
# 
# We use the final estimates in each of the studies as two independent estimates of the biomass of soil microbes. Xu et al. estimate a biomass of ≈23 Gt C of soil microbes, whereas Serna-Chavez et al. estimate ≈15 Gt C.

# In[2]:


# Define the values for the estimates of the biomass of soil microbes from Xu et al. and Serna-Chavez et al.
xu = 23.2e15
serna_chavez = 14.6e15


# As our best estimate for the biomass of soil microbes, we use the geometric mean of the values from Xu et al. and Serna-Chavez et al.

# In[3]:


# Our best estimate is the geometric mean of values from Xu et al. and Serna-Chavez et al.
best_estimate = gmean([xu,serna_chavez])
print('Our best estimate for the biomass of soil microbes is ≈%.0f Gt C' % (best_estimate/1e15))


# ## Cells in deeper layers
# The estimates reported in Xu et al. and Serna-Chavez et al. are for microbial biomass in the top 1 meter of soil. To take into account microbial biomass in depths lower than 1 meter, we try to estimate the fraction of microbial biomass in the top 1 meter out of the total biomass of soil microbes.
# 
# Xu et al. extrapolate the microbial biomass across the soil profile based on empirical equations for the distribution of root biomass along soil depth from [Jackson et al.](http://dx.doi.org/10.1007/BF00333714). The empirical equations are biome-specific, and follow the general form: $$Y = 1-\beta^d$$ Where Y is the cumulative fraction of roots, d is depth in centimeters, and $\beta$ is a coefficient fitted for each biome. This means the $\beta^d$ represents the fraction of roots present in layers lower deeper than d centimeters.
# 
# We use the fitted $\beta$ coefficients from Jackson et al., along with estimates for the total microbial biomass in the top meter fo soils in each biome from Xu et al. to estimate the amount of biomass present in soil layers deeper than 1 meter.

# In[4]:


# Load data on the microbial biomass from each biome and the coefficients for the depth distribution of roots
# in each biome
data = pd.read_excel('soil_microbial_biomass_data.xlsx',skiprows=1)

# Calculate the fraction of biomass deeper than 100 centimeters for each biome
biome_deeper_frac = (data['beta']**100)

# Calculate the relative fraction of total microbial biomass that is present in layers deeper than 1 meter
total_deeper_relative_fraction = (data['Total microbial biomass 100 cm (g C)']*biome_deeper_frac).sum()/xu
print('The fraction of microbial biomass in layers deeper than 1 meter based on Xu et al. is ' + '{:,.0f}%'.format(total_deeper_relative_fraction*100))


# As an additional source for estimating the fraction of biomass of microbes in soil layers deeper than 1 meter, we use the concentration of bacterial cells present in layers deeper than 1 meter reported in [Whitman et al.](https://www.ncbi.nlm.nih.gov/pubmed/9618454). Whitman et al. estimate that in forests there are ≈$4×10^7$ cells per gram in the top 1 meter and ≈$10^6$ cells per gram in depths of 1-8 meters. For other soils, Whitman et al. estimate ≈$2×10^9$ cells per gram in the top 1 meterand ≈$10^8$ cells per gram in depth of 1-8 meters. Assuming cells in deeper layers are similar in size to cells in the top 1 meter, this is equivalent to: 

# In[5]:


# Concentration of cells in top 1 meter of forest soils
forest_upper = 4e7
# Top 1 meter is 1 meter in depth
forest_upper_depth = 1
# Concentration of cells in depths of 1-7 meters of forest soils
forest_lower = 1e6
# The deeper layer of soils is 1-8 meters - 7 meters in depth
forest_lower_depth = 7
# Concentration of cells in top 1 meter of other soils
other_upper = 2e9
# Top 1 meter is 1 meter in depth
other_upper_depth = 1
# Concentration of cells in depths of 1-7 meters of other soils
other_lower = 1e8
# The deeper layer of soils is 1-8 meters - 7 meters in depth
other_lower_depth = 7

#Calculate the fraction of cells present in deeper layers of soil in forests and other soils
forest_lower_frac = forest_lower*forest_lower_depth/(forest_lower*forest_lower_depth + forest_upper*forest_upper_depth)
other_lower_frac = other_lower*other_lower_depth/(other_lower*other_lower_depth + other_upper*other_upper_depth)
whitman_mean_frac = frac_mean(np.array([forest_lower_frac,other_lower_frac]))
print('The fraction of cells found in soil layers deeper than 1 meter is ' + '{:,.0f}%'.format(forest_lower_frac*100) + ' in forests and ' '{:,.0f}%'.format(other_lower_frac*100) + ' in other soils.')
print('The average fraction of cells found in deeper layers is ' + '{:,.0f}%'.format(100*whitman_mean_frac))


# As our estimate for the fraction of biomass present in layers deeper than 1 meter, we take the geometric mean of the fractions estimated by Xu et al. and by Whitman et al.

# In[6]:


# Calculate the geometric mean of the estimates by Xu et al. and Whitman et al.
mean_deep_frac = frac_mean(np.array([total_deeper_relative_fraction,whitman_mean_frac]))
print('Our best estimate for the fraction of biomass present in layers deeper than 1 meter is ' + '{:,.0f}%'.format(100*mean_deep_frac))

# Correct out best estimate to account for the biomass of microbes in soil layers deeper than 1 meter
best_estimate_corrected = best_estimate*(1+mean_deep_frac)
print('Our best estimate for the biomass of soil microbes, including contributions from microbes present in layers deeper than 1 meter is %.0f Gt C' % (best_estimate_corrected/1e15))


# # Uncertainty analysis
# To calculate the uncertainty associated with the estimate for the total number of of bacteria and archaea, we first collect all available uncertainties and then take the largest value as our best projection for the uncertainty.
# 
# ## Total biomass of microbes in the top 1 meter
# 
# ### Intra-study uncertainty
# As noted above, our estimate is based on two studies which report the total biomass of soil microbes - [Xu et al.](http://dx.doi.org/10.1111/geb.12029) and [Serna-Chavez et al.](http://dx.doi.org/10.1111/geb.12070). Xu et al. does not report uncertainties associated with the total estimate of microbial biomass. However, Xu et al. report 95% confidence intervals for the average microbial biomass densities in each biome. We use these ranges as a measure of the intra-study uncertainty in Xu et al. The highest uncertainty across biomes is ≈1.5-fold.

# In[7]:


# We calculate the upper and lower multiplicative 95% confidence interval of the average microbial 
# biomass density for each biome
xu_upper_CI = data['upper 95% confidence interval of Cmic']/data['Cmic (0-30 cm) [mmol C kg^-1]']
xu_lower_CI = data['Cmic (0-30 cm) [mmol C kg^-1]']/data['lower 95% confidence interval of Cmic']

# Our estimate for the final uncertainty is the average of the upper and lower confidence intervals.
data['95% confidence interval'] = (pd.concat([xu_upper_CI,xu_lower_CI],axis=1).mean(axis=1))
data[['Biome','95% confidence interval']]


# In[8]:


print('The maximal intra-study uncertainty in Xu et al. across biomes is %.1f-fold' % data['95% confidence interval'].max())


# Serna-Chavez et al. report 95% confidence internal of the final estimate for the total biomass of soil microbes. It is not clear from the paper what does this uncertainty represents, but it most probably represents 95% range of values from bootstrapping the parameters of the model used to estimate the local biomass density of soil microbes at each location. The reported 95% confidence interval is ≈0.007 Gt C, which represents an uncertainty of ≈1.0005-fold.
# 
# ### Interstudy uncertainty
# We estimate the 95% multiplicative error of the geometric mean of the estimates from Xu et al. and Serna-Chavez et al. 

# In[9]:


mul_CI_top = geo_CI_calc([xu,serna_chavez])
print('The interstudy uncertainty is ≈%.1f-fold' % mul_CI_top)


# We use the maximal uncertainty out of the collection of intra-study and interstudy uncertainties as our projection for the uncertainty associated with the biomass of soil microbes. The maximal uncertainty is the interstudy uncertainty of ≈1.6-fold. 
# 
# ## Fraction of biomass in soil layers deeper than 1 meter
# ### Intra-study uncertainty
# We estimate the intra-study uncetainty in the fraction of microbial biomass located in soil layers deeper than 1 meter in Xu et al. and in Whitman et al. For Xu et al. we calculating the 95% confidence interval of the $\beta^d$ measure across biomes. For Whitman et al. we calculate the 95% confidence interval of the estimates for the fraction of bacterial cells in depth of 1-8 meters out of the total number of cells in forests and other soil types.

# In[10]:


xu_deep_frac_CI = frac_CI(data['beta']**100)
whitman_deep_frac_CI = frac_CI(np.array([forest_lower_frac,other_lower_frac]))
print('The intra-study uncertainty of the fraction of microbial biomass present in soil layers deeper than 1 meter is ≈%.1f-fold for Xu et al. and ≈%.1f-fold for Whitman et al.' %(xu_deep_frac_CI,whitman_deep_frac_CI))


# 
# ### Interstudy uncertainty
# We calculate the 95% confidence interval from the average estimates of Xu et al. and Whitman et al. and use them as a measure of the interstudy uncertainty.

# In[11]:


inter_deep_frac_CI = frac_CI(np.array([total_deeper_relative_fraction,whitman_mean_frac]))
print('The interstudy uncertainty of the fraction of microbial biomass present in soil layers deeper than 1 meter is ≈%.1f-fold.' %(inter_deep_frac_CI))


# We take the highest uncertainty of the intra-study and interstudy uncertainty of ≈7.5-fold. This uncertainty relates to the fraction of biomass present in soil layers deeper than 1 meter. In order to propagate this uncertainty to the estimate of the total biomass of soil microbes, we sample 1000 times from a lognormal distribution with a mean and std of the fraction biomass from layers deeper than 1 meter, and add 1 to each sample to estimate the coefficient by which the total biomass of soil microbes should be corrected.
# The 97.5% and 2.5% percentiles of the resulting distribution of coefficients will be used as an estimate for the uncertainty of the total biomass of soil microbes contributed by the uncertainty in the estimate of the fraction of the biomass of microbes in soil layers deeper than 1 meter.

# In[12]:


# Calculate the maximal uncertainty between the intra-study and interstudy uncertainty
best_deep_frac_CI = np.max([xu_deep_frac_CI,whitman_deep_frac_CI,inter_deep_frac_CI])
# Sample the fraction of biomass in soil layers deeper than 1 meter from a lognormal distribution 
deep_frac_dist = np.random.lognormal(np.log(mean_deep_frac),np.log(best_deep_frac_CI**(1./1.96)),1000)
# Calculate the distribution of coefficients by which the total biomass of soil microbes should be corrected
cor_coeff_dist = 1 + deep_frac_dist

# Calculate the 97.5% and 2.5% percentiles of the correction coefficient distribution, relative to the mean
cor_coeff_upper_CI = np.percentile(cor_coeff_dist,97.5)/(1+mean_deep_frac)
cor_coeff_lower_CI = (1+mean_deep_frac)/np.percentile(cor_coeff_dist,2.5)
# our estimate for the 95% confidence interval is the average between the 97.5% and 2.5% fold changes
cor_coeff_CI = np.mean([cor_coeff_upper_CI,cor_coeff_lower_CI])
print('Our estimate for the uncertainty of the total biomass of soil microbes contributed by the uncertainty in the esti,ate of the fraction of the biomass of microbes in soil layers deeper than 1 meter is %.1f-fold' % cor_coeff_CI)


# ## Total uncertainty
# To estimate the total uncertainty of the biomass of soil microbes, we combine the ucnertainty assoicated with the estiamte of biomass of soil microbes in the top 1 meter of soil, and the uncertainty of the correction coefficient to include biomass contribution from soil layer deeper than 1 meter.

# In[13]:


mul_CI = CI_prod_prop(np.array([mul_CI_top,cor_coeff_CI]))
print('The total uncertainty for the biomass of soil microbes is %.1f-fold' % mul_CI)


# We also take into account additional sources of uncertainty which are difficult to quantify, as detailed in the section about soil fungi in the Supplementary Information. We thus project an uncertainty of ≈2-fold for the biomass of soil microbes. Our final parameters are:

# In[14]:


print('Total biomass of soil microbes: %.0f Gt C' % (best_estimate/1e15))
print('Uncertainty associated with the estimate of the total biomass of soil microbes ≈2-fold' % mul_CI)

old_results = pd.read_excel('../fungi_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[0] = pd.Series({
                'Parameter': 'Total biomass of soil microbes',
                'Value': int(best_estimate_corrected),
                'Units': 'g C',
                'Uncertainty': "{0:.1f}".format(2)
                })

result.to_excel('../fungi_biomass_estimate.xlsx',index=False)



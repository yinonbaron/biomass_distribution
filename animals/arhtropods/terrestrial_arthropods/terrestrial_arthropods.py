
# coding: utf-8

# # Estimating the biomass of terrestrial arthropods
# To estimate the biomass of terrestrial arthropods, we rely on two parallel methods - a method based on average biomass densities of arthropods extrapolated to the global ice-free land surface, and a method based on estimates of the average carbon content of a characteristic arthropod and the total number of terrestrial arthropods.
# 
# ## Average biomass densities method
# We collected values from the literature on the biomass densities of arthropods per unit area. We assume, based on [Stork et al.](http://dx.doi.org/10.1007/978-94-009-1685-2_1), most of the biomass is located in the soil, litter or in the canopy of trees. We thus estimate a mean biomass density of arhtropods in soil, litter and in canopies, sum those biomass densities and apply them across the entire ice-free land surface.
# 
# ### Litter arthropod biomass
# We complied a list of values from several different habitats. Most of the measurements are from forests and savannas. For some of the older studies, we did not have access to the original data, but to a summary of the data made by two main studies: [Gist & Crossley](http://dx.doi.org/10.2307/2424109) and [Brockie & Moeed](http://dx.doi.org/10.1007/BF00377108). Here is a sample of the data from Gist & Grossley:

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gmean
import sys
sys.path.insert(0, '../../../statistics_helper/')
from CI_helper import *
pd.options.display.float_format = '{:,.1f}'.format
# Load global stocks data
gc_data = pd.read_excel('terrestrial_arthropods_data.xlsx','Gist & Crossley',skiprows=1)
gc_data.head()


# Here is a sample from Brockie & Moeed:

# In[2]:

bm_data = pd.read_excel('terrestrial_arthropods_data.xlsx','Brockie & Moeed',skiprows=1)
bm_data.head()


# We calculate the sum of biomass of all the groups of arthropods in each study to provide an estimate for the total biomass density of arthropods in litter:

# In[3]:

gc_study = gc_data.groupby('Study').sum()
bm_study = bm_data.groupby('Study').sum()

print('The estimate from Brockie & Moeed:')
bm_study


# In[4]:

print('The estimate from Gist & Crossley:')
gc_study


# In cases where data is coflicting between the two studies, we calculate the mean. We merge the data from the papers to generate a list of estimates on the total biomass density of arhtropods

# In[5]:

# Concat the data from the two studies
conc = pd.concat([gc_study,bm_study])
conc_mean = conc.groupby(conc.index).mean()
conc_mean


# We calculate from the dry weight and wet weight estimates the biomass density in g C $m^{-2}$ by assuming 70% water content and 50% carbon in dry mass:

# In[6]:

# Fill places with no dry weight estimate with 30% of the wet weight estimate 
conc_mean['Dry weight [g m^-2]'].fillna(conc_mean['Wet weight [g m^-2]']*0.3,inplace=True)

# Calculate carbon biomass as 50% of dry weight
conc_mean['Biomass density [g C m^-2]'] = conc_mean['Dry weight [g m^-2]']/2
conc_mean['Biomass density [g C m^-2]']


# We calculate the geometric mean of the estimates from the different studies as our best estimate of the biomass density of litter arthropods.

# In[7]:

litter_biomass_density = gmean(conc_mean.iloc[0:5,3])
print('Our best estimate for the biomass density of arthropods in litter is ≈%.0f g C m^-2' %litter_biomass_density)


# ### Soil arthropod biomass
# As our source for estimating the biomass of soil arthropods, we use these data collected from the literature, which are detailed below:

# In[8]:

# Load additional data
soil_data = pd.read_excel('terrestrial_arthropods_data.xlsx','Soil',index_col='Reference')
soil_data


# We calculate the geometric mean of the estimate for the biomass density of arthropods in soils:

# In[9]:

# Calculate the geometric mean of the estimates of the biomass density of soil arthropods
soil_biomass_density = gmean(soil_data['Biomass density [g C m^-2]'])

print('Our best estimate for the biomass density of arthropods in soils is ≈%.0f g C m^-2' %soil_biomass_density)


# If we sum the biomass density of soil and litter arthropods, we arrive at an estimate of ≈2 g C m^-2, which is inline with the data from Kitazawa et al. of 1-2 g C m^-2.

# ### Canopy arthropod biomass
# Data on the biomass density of canopy arthropods is much less abundant. We extracted from the literature the following values:

# In[10]:

# Load the data on the biomass density of canopy arthropods
canopy_data = pd.read_excel('terrestrial_arthropods_data.xlsx', 'Canopy',index_col='Reference')
canopy_data


# We calculate the geometric mean of the estimates for the biomass density of arthropods in canopies:

# In[11]:

# Calculate the geometric mean of the estimates of biomass densitiy of canopy arthropods
canopy_biomass_density = gmean(canopy_data['Biomass density [g C m^-2]'])
print('Our best estimate for the biomass density of arthropods in canopies is ≈%.1f g C m^-2' %canopy_biomass_density)


# To generate our best estimate for the biomass of arthropods using estimates of biomass densities, we sum the estimates for the biomass density of arthropods in soils and in canopies, and apply this density over the entire ice-free land surface of $1.3×10^{14} \: m^2$:

# In[12]:

# Sum the biomass densities of arthropods in soils and in canopies
total_denisty = litter_biomass_density+soil_biomass_density+canopy_biomass_density

# Apply the average biomass density across the entire ice-free land surface
method1_estimate = total_denisty*1.3e14

print('Our best estimate for the biomass of terrestrial arthropods using average biomass densities is ≈%.1f Gt C' %(method1_estimate/1e15))


# ## Average carbon content method
# In this method, in order to estimate the total biomass of arthropods, we calculate the carbon content of a characteristic arthropod, and multiply this carbon content by an estimate for the total number of arthropods.
# We rely both on data from Gist & Crossley which detail the total number of arthropods per unit area as well as the total biomass of arthropods per unit area for serveal studies. Form this data we can calculate the characteristic carbon content of a single arthropod assuming 50% carbon in dry mass:

# In[13]:

pd.options.display.float_format = '{:,.1e}'.format

# Calculate the carbon content of a single arthropod by dividing the dry weight by 2 (assuming 50% carbon in
# dry weight) and dividing the result by the total number of individuals
gc_study['Carbon content [g C per individual]'] = gc_study['Dry weight [g m^-2]']/2/gc_study['Density of individuals [N m^-2]']

gc_study


# We combine the data from these studies with data from additional sources detailed below:

# In[14]:

# Load additional data sources
other_carbon_content_data = pd.read_excel('terrestrial_arthropods_data.xlsx', 'Carbon content',index_col='Reference')

other_carbon_content_data


# We calculate the geometric mean of the estimates from the difference studies and use it as our best estimate for the carbon content of a characteristic arthropod:

# In[15]:

# Calculate the geometric mean of the estimates from the different studies on the average carbon content of a single arthropod.
average_carbon_content = gmean(pd.concat([other_carbon_content_data,gc_study])['Carbon content [g C per individual]'])
print('Our best estimate for the carbon content of a characteristic arthropod is %.1e g C' % average_carbon_content)


# To estimate the total biomass of arthropods using the characteristic carbon content method, we multiply our best estiamte of the carbon content of a single arthropod by an estimate of the total number of arthropods made by [Williams](http://dx.doi.org/10.1086/282115). Williams estiamted a total of $~10^{18}$ individual insects in soils. We assume this estimate of the total number of insects is close to the total number of arthropods (noting that in this estimate Williams also included collembola which back in 1960 were considered insects, and are usually very numerous because of their small size). To estimate the total biomass of arthropods, we multiply the carbon content of a single arthropod by the the estimate for the total number of arthropods:

# In[16]:

# Total number of insects estimated by Williams
tot_num_arthropods = 1e18

# Calculate the total biomass of arthropods
method2_estimate = average_carbon_content*tot_num_arthropods
print('Our best estimate for the biomass of terrestrial arthropods using average biomass densities is ≈%.1f Gt C' %(method2_estimate/1e15))


# Our best estimate for the biomass of arthropods is the geometric mean of the estimates from the two methods:

# In[17]:

# Calculate the geometric mean of the estimates using the two methods
best_estimate = gmean([method1_estimate,method2_estimate])
print('Our best estimate for the biomass of terrestrial arthropods is ≈%.1f Gt C' %(best_estimate/1e15))             


# # Uncertainty analysis
# To assess the uncertainty associated with the estimate of the biomass of terrestrial arthropods, we compile a collection of the different sources of uncertainty, and combine them to project the total uncertainty. We survey the interstudy uncertainty for estimates within each method, the total uncertainty of each method and the uncertainty of the geometric mean of the values from the two methods.
# 
# ## Average biomass densities method
# We calculate the 95% confidence interval for the geometric mean of the biomass densities reported for soil and canopy arthropods:

# In[18]:

litter_CI = geo_CI_calc(conc_mean['Biomass density [g C m^-2]'])
soil_CI = geo_CI_calc(soil_data['Biomass density [g C m^-2]'])
canopy_CI = geo_CI_calc(canopy_data['Biomass density [g C m^-2]'])
print('The 95 percent confidence interval for the average biomass density of soil arthropods is ≈%.1f-fold' %litter_CI)
print('The 95 percent confidence interval for the average biomass density of soil arthropods is ≈%.1f-fold' %soil_CI)
print('The 95 percent confidence interval for the average biomass density of canopy arthropods is ≈%.1f-fold' %canopy_CI)


# To estimate the uncertainty of the global biomass estimate using the average biomass density method, we propagate the uncertainties of the soil and canopy biomass density:

# In[19]:

method1_CI = CI_sum_prop(estimates=np.array([litter_biomass_density,soil_biomass_density,canopy_biomass_density]),mul_CIs=np.array([litter_CI,soil_CI,canopy_CI]))
print('The 95 percent confidence interval biomass of arthropods using the biomass densities method is ≈%.1f-fold' %method1_CI)


# ## Average carbon content method
# As a measure of the uncertainty of the estimate of the total biomass of arthropods using the average carbon content method, we calculate the 95% confidence interval of the geometric mean of the estimates from different studies of the carbon content of a single arthropod:

# In[20]:

carbon_content_CI = geo_CI_calc(pd.concat([other_carbon_content_data,gc_study])['Carbon content [g C per individual]'])
print('The 95 percent confidence interval of the carbon content of a single arthropod is ≈%.1f-fold' %carbon_content_CI)


# We combine this uncertainty of the average carbon content of a single arthropod with the uncertainty reported in Williams on the total number of insects of about one order of magnitude. This provides us with a measure of the uncertainty of the estimate of the biomass of arthropods using the average carbon content method.

# In[21]:

# The uncertainty of the total number of insects from Williams
tot_num_arthropods_CI = 10

# Combine the uncertainties of the average carbon content of a single arthropod and the uncertainty of 
# the total number of arthropods
method2_CI = CI_prod_prop(np.array([carbon_content_CI,tot_num_arthropods_CI]))
print('The 95 percent confidence interval biomass of arthropods using the average carbon content method is ≈%.1f-fold' %method2_CI)


# ## Inter-method uncertainty
# We calculate the 95% conficence interval of the geometric mean of the estimates of the biomass of arthropods using the average biomass density or the average carbon content:

# In[22]:

inter_CI = geo_CI_calc(np.array([method1_estimate,method2_estimate]))
print('The inter-method uncertainty of the geometric mean of the estimates of the biomass of arthropods is ≈%.1f' % inter_CI)


# As our best projection for the uncertainty associated with the estimate of the biomass of terrestrial arthropods, we take the highest uncertainty among the collection of uncertainties we generate, which is the ≈15-fold uncertainty of the average carbon content method. 

# In[23]:

mul_CI = np.max([inter_CI,method1_CI,method2_CI])
print('Our best projection for the uncertainty associated with the estimate of the biomass of terrestrial arthropods is ≈%.1f-fold' %mul_CI)


# ## The biomass of termites
# As we state in the Supplementary Information, there are some groups of terrestrial arthropods for which better estimates are available. An example is the biomass of termites. We use the data in [Sanderson](http://dx.doi.org/10.1029/96GB01893) to estimate the global biomass of termites:

# In[24]:

# Load termite data
termite_data = pd.read_excel('terrestrial_arthropods_data.xlsx', 'Sanderson', skiprows=1, index_col=0)

# Multiply biomass density by biome area and sum over biomes
termite_biomass = (termite_data['Area [m^2]']* termite_data['Biomass density [g wet weight m^-2]']).sum()

# Calculate carbon mass assuming carbon is 15% of wet weight
termite_biomass *= 0.15

print('The estimate of the total biomass of termites based on Sanderson is ≈%.2f Gt C' %(termite_biomass/1e15))



# coding: utf-8

# # Estimating the biomass of Annelids
# To estimate the total biomass of annelids, we rely on data collected in a recent study by [Fierer et al.](http://dx.doi.org/10.1111/j.1461-0248.2009.01360.x). Fierer et al. collected data on the biomass density of two major groups on annelids (Enchytraeids & Earthworms) in different biomes. Here is a sample from the data:

# In[1]:


import pandas as pd
import numpy as np
from scipy.stats import gmean

# Load the data taken from Fierer et al.
data = pd.read_excel('annelid_biomass_data.xlsx','Fierer',skiprows=1)
data


# For each biome, Fierer et al. provides an estimate of the average biomass density and the median biomass density. We generate two estimates for the total biomass of annelids, one based on average biomass densities and one based on median biomass densities. The estimate based on the average biomass density is more susceptible to sampling bias, as even a single measurement which is not characteristic of the global population (such as samples which are in non-natural conditions, or samples which have some technical biases associated with them) might shift the average biomass density significantly. On the other hand, the estimate based on median biomass densities might underestimate global biomass as it will reduce the effect of biologically relevant high biomass concentrations. As a compromise between these two caveats, we chose to use as our best estimate the geometric mean of the estimates from the two methodologies.
# 
# For each biome, we multiply the sum of the biomass density of Enchytraeids and Earthworms by the total area of that biome taken from the book [Biogeochemistry: An analysis of Global Change](https://www.sciencedirect.com/science/book/9780123858740) by Schlesinger & Bernhardt.:

# In[2]:


# Load biome area data
area = pd.read_excel('annelid_biomass_data.xlsx','Biome area', skiprows=1, index_col='Biome')

# For each biome sum the total biomass density of annelids
total_biomass_density = data.groupby('Biome').sum()

# Calculate the total biomass of annelids based on average or median biomass densities
total_biomass_mean = (total_biomass_density['Average biomass density [g C m^-2]']*area['Area [m^2]']).sum()
total_biomass_median = (total_biomass_density['Median biomass density [g C m^-2]']*area['Area [m^2]']).sum()

print('The total biomass of annelids based on Fierer et al. based on average biomass densities is %.1f Gt C' %(total_biomass_mean/1e15))
print('The total biomass of annelids based on Fierer et al. based on median biomass densities is %.2f Gt C' %(total_biomass_median/1e15))


# The data in Fierer et al. does not account two biomes - croplands and tropical savannas. To estimate the biomass contribution of annelids from those biomes, we collected data from the literature on the biomass density of annelids (mostly earthworms) from these biomes. The data we collected is provided below:

# In[3]:


supp_biome_data = pd.read_excel('annelid_biomass_data.xlsx','Supplementary biomes')
supp_biome_data


# For each biome, we calculate the average and median annelid biomass density, and multiply by the total area of the biome:

# In[4]:


# Calculate average and median biomass densities for each additional biome
mean_supp_biome_biomass_density = supp_biome_data.groupby('Biome').mean()['Biomass density [g C m^-2]']
median_supp_biome_biomass_density = supp_biome_data.groupby('Biome').median()['Biomass density [g C m^-2]']

# Add the additional biomass to the estimate of the total biomass
total_biomass_mean += (mean_supp_biome_biomass_density*area['Area [m^2]']).sum()
total_biomass_median += (median_supp_biome_biomass_density*area['Area [m^2]']).sum()

print('Our estimate for the biomass of annelids based on average biomass densities is %.1f Gt C' %(total_biomass_mean/1e15))
print('Our estimate for the biomass of annelids based on median biomass densities is %.1f Gt C' %(total_biomass_median/1e15))


# As noted above, for our best estimate we use the geometric mean of the estimates based on the average and median biomass densities at each biome:

# In[5]:


# Calculate the geometric mean of the average-based and median-based estimates
best_estimate = gmean([total_biomass_mean,total_biomass_median])

print('Our best estimate for the biomass of annelids is %.1f Gt C' %(best_estimate/1e15))


# This estimate does not take into account marine annelids, which we estimate do not contribute a major biomass component to the total biomass of annelids, as discussed in the annelids section in the Supplementary Information.

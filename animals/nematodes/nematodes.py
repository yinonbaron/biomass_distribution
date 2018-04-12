
# coding: utf-8

# In[1]:


# Load dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean
import sys
sys.path.insert(0,'../../statistics_helper/')
from excel_utils import *


# # Estimating the biomass of nematodes
# To estimate the total biomass of nematodes, we calculate the total biomas of terrestrial and marine nematodes.
# 
# ## Terrestrial nematodes
# We based our estimate of the biomass of terrestrial nematodes on data collected in a recent study by [Fierer et al.](http://dx.doi.org/10.1111/j.1461-0248.2009.01360.x). Fierer et al. collected data on the biomass density of two major groups on annelids (Enchytraeids & Earthworms) in different biomes. Here is a sample from the data:

# In[2]:


# Load the data taken from Fierer et al.
data = pd.read_excel('nematode_biomass_data.xlsx','Fierer',skiprows=1,index_col='Biome')
data


# The data in Fierer et al. does not include biomass density of nematodes in savanna, pastures and cropland. We use the geometric mean of values from other biomes as our best estimate for the biomass density of nematodes in these biomes:

# In[3]:


# Calculate the geometric mean of the biomass density across biomes
average_biomass_density = gmean(data['Average biomass density [g C m^-2]'].dropna())
median_biomass_density = gmean(data['Median biomass density [g C m^-2]'].dropna())

# Set the biomass density in the missing biomes as the geometric mean of the biomass density of the
# available biomes
data.loc['Native tropical savanna','Average biomass density [g C m^-2]'] = average_biomass_density
data.loc['Tropical pastures','Average biomass density [g C m^-2]'] = average_biomass_density
data.loc['Crops','Average biomass density [g C m^-2]'] = average_biomass_density
data.loc['Native tropical savanna','Median biomass density [g C m^-2]'] = median_biomass_density
data.loc['Tropical pastures','Median biomass density [g C m^-2]'] = median_biomass_density
data.loc['Crops','Median biomass density [g C m^-2]'] = median_biomass_density


# For each biome, Fierer et al. provides an estimate of the average biomass density and the median biomass density. We generate two estimates for the total biomass of annelids, one based on average biomass densities and one based on median biomass densities. The estimate based on the average biomass density is more susceptible to sampling bias, as even a single measurement which is not characteristic of the global population (such as samples which are in non-natural conditions, or samples which have some technical biases associated with them) might shift the average biomass density significantly. On the other hand, the estimate based on median biomass densities might underestimate global biomass as it will reduce the effect of biologically relevant high biomass concentrations. As a compromise between these two caveats, we chose to use as our best estimate the geometric mean of the estimates from the two methodologies.
# 
# For each biome, we multiply the sum of the biomass density of nematodes by the total area of that biome taken from the book [Biogeochemistry: An analysis of Global Change](https://www.sciencedirect.com/science/book/9780123858740) by Schlesinger & Bernhardt.:

# In[4]:


# Load biome area data
area = pd.read_excel('nematode_biomass_data.xlsx','Biome area', skiprows=1, index_col='Biome')

# Calculate the total biomass of annelids based on average or median biomass densities
total_biomass_mean = (data['Average biomass density [g C m^-2]']*area['Area [m^2]']).sum()
total_biomass_median = (data['Median biomass density [g C m^-2]']*area['Area [m^2]']).sum()

print('The total biomass of terrestrial nematodes based on Fierer et al. based on average biomass densities is %.3f Gt C' %(total_biomass_mean/1e15))
print('The total biomass of terrestrial nematodes based on Fierer et al. based on median biomass densities is %.3f Gt C' %(total_biomass_median/1e15))

# Use the geometric mean of the estimate based on the average biomass density and the
# estimate based on the median biomass density as our best estimate for the biomass of
# nematodes
best_terrestrial_biomass = gmean([total_biomass_mean,total_biomass_median])
print('Our best estimate of total biomass of terrestrial nematodes based on Fierer et al. is %.3f Gt C' %(best_terrestrial_biomass/1e15))


# ## Marine nematodes
# Our estimate of the total biomass of marine nematodes is based on data for seafloor biomass from [Wei et al.](http://dx.doi.org/10.1371/journal.pone.0015323). Wei et al. estimate ≈0.1 Gt C of benthic biomass, with ≈13% of that biomass contributed by meiofauna (defined as organisms which are 45µm-1mm in diameter). We assume meiofauna to be dominated by nematodes, (see nematodes section in the Supplementary Information for details regarding this assumption). Thus, we estimate the total biomass of marine nematodes at ≈0.01 Gt C.
# 
# This estimate does not include biomass contribution from nematodes in benthic environments which are "hot spots" (such as marine canyons and seamounts). For more details regarding such contribution, see the other phyla section in the Supplementary Information.
# 
# Our best estimate for the total biomass of nematodes is the sum of our estimates for the biomass of terrestrial nematodes and marine nematodes:

# In[5]:


# As noted above, our best estimate for the biomass of marine nematodes is ≈0.01 Gt C
best_marine_biomass = 0.014e15

# Calculate our best estimate for the biomass of nematodes
best_estimate = best_terrestrial_biomass+best_marine_biomass

print('Our best estimate of total biomass of nematodes is %.2f Gt C' %(best_estimate/1e15))


# # Estimating the total number of nematodes
# We calculate the total number of nematodes by dividing our estimate of the total biomass of nematodes by the carbon content of nematodes, which is ≈0.05 µg C (Fierer et al.):

# In[6]:


# Carbon content of a single nematode based on Fierer et al.
carbon_content = 0.05e-6

# Calculate the total number of nematodes
tot_nematode_num = best_estimate/carbon_content

print('Our best estimate for the total number of nematodes is ≈%.1e' %tot_nematode_num)


# In[7]:


# Feed results to the animal biomass data
old_results = pd.read_excel('../animal_biomass_estimate.xlsx',index_col=0)
result = old_results.copy()
result.loc['Nematodes',(['Biomass [Gt C]','Uncertainty'])] = (best_estimate/1e15,np.nan)
result.to_excel('../animal_biomass_estimate.xlsx')

# Feed results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Animals','Nematodes'), 
               col=['Biomass [Gt C]', 'Uncertainty'],
               values=[best_estimate/1e15,None],
               path='../../results.xlsx')


# Feed results to Table S1
update_results(sheet='Table S1', 
               row=('Animals','Nematodes'), 
               col=['Number of individuals'],
               values=tot_nematode_num,
               path='../../results.xlsx')

# Feed results to Fig. 2A
update_results(sheet='Fig2A', 
               row=('Terrestrial','Nematodes'), 
               col=['Biomass [Gt C]'],
               values=best_terrestrial_biomass/1e15,
               path='../../results.xlsx')

# Feed results to Fig. 2A
update_results(sheet='Fig2A', 
               row=('Marine','Nematodes'), 
               col=['Biomass [Gt C]'],
               values=best_marine_biomass/1e15,
               path='../../results.xlsx')


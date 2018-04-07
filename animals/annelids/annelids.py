
# coding: utf-8

# In[1]:

# Load dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean
import sys
sys.path.insert(0, '../../statistics_helper/')
from excel_utils import *


# # Estimating the biomass of Annelids
# To estimate the total biomass of annelids, we rely on data collected in a recent study by [Fierer et al.](http://dx.doi.org/10.1111/j.1461-0248.2009.01360.x). Fierer et al. collected data on the biomass density of two major groups on annelids (Enchytraeids & Earthworms) in different biomes. Here is a sample from the data:

# In[2]:

# Load the data taken from Fierer et al.
data = pd.read_excel('annelid_biomass_data.xlsx','Fierer',skiprows=1)
data


# For each biome, Fierer et al. provides an estimate of the average biomass density and the median biomass density. We generate two estimates for the total biomass of annelids, one based on average biomass densities and one based on median biomass densities. The estimate based on the average biomass density is more susceptible to sampling bias, as even a single measurement which is not characteristic of the global population (such as samples which are in non-natural conditions, or samples which have some technical biases associated with them) might shift the average biomass density significantly. On the other hand, the estimate based on median biomass densities might underestimate global biomass as it will reduce the effect of biologically relevant high biomass concentrations. As a compromise between these two caveats, we chose to use as our best estimate the geometric mean of the estimates from the two methodologies.
# 
# For each biome, we multiply the sum of the biomass density of Enchytraeids and Earthworms by the total area of that biome taken from the book [Biogeochemistry: An analysis of Global Change](https://www.sciencedirect.com/science/book/9780123858740) by Schlesinger & Bernhardt.:

# In[3]:

# Load biome area data
area = pd.read_excel('annelid_biomass_data.xlsx','Biome area', skiprows=1, index_col='Biome')

# For each biome sum the total biomass density of annelids
total_biomass_density = data.groupby('Biome').sum()

# Calculate the total biomass of annelids based on average or median biomass densities
total_biomass_mean = (total_biomass_density['Average biomass density [g C m^-2]']*area['Area [m^2]']).sum()
total_biomass_median = (total_biomass_density['Median biomass density [g C m^-2]']*area['Area [m^2]']).sum()

print('The total biomass of annelids based on Fierer et al. based on average biomass densities is %.1f Gt C' %(total_biomass_mean/1e15))
print('The total biomass of annelids based on Fierer et al. based on median biomass densities is %.2f Gt C' %(total_biomass_median/1e15))
total_biomass_density


# The data in Fierer et al. does not account two biomes - croplands and tropical savannas. To estimate the biomass contribution of annelids from those biomes, we collected data from the literature on the biomass density of annelids (mostly earthworms) from these biomes. The data we collected is provided below:

# In[4]:

supp_biome_data = pd.read_excel('annelid_biomass_data.xlsx','Supplementary biomes')
supp_biome_data


# For each biome, we calculate the average and median annelid biomass density, and multiply by the total area of the biome:

# In[5]:

# Calculate average and median biomass densities for each additional biome
mean_supp_biome_biomass_density = supp_biome_data.groupby('Biome').mean()['Biomass density [g C m^-2]']
median_supp_biome_biomass_density = supp_biome_data.groupby('Biome').median()['Biomass density [g C m^-2]']


# We do no know the specifc division in terms of area between pastures and savanna. We thus make two estimates - one assumes the entire area of tropical savannas is filled with savanna, and the second assumes the entire area is pastures. We generate four estimates - median and mean-based estimates with considering only savanna or pastures. As our best estimate for the total biomass of soil annelids, we use the geometric mean of those four estimates:

# In[6]:

# Consider only savanna
all_savanna_area = area.copy()
all_savanna_area.loc['Native tropical savanna', 'Area [m^2]'] *=2
all_savanna_area.loc['Tropical pastures', 'Area [m^2]'] =0
all_savanna_mean =  total_biomass_mean + (mean_supp_biome_biomass_density*all_savanna_area['Area [m^2]']).sum()
all_savanna_median =  total_biomass_median + (median_supp_biome_biomass_density*all_savanna_area['Area [m^2]']).sum()

# Consider only pastures
all_pastures_area = area.copy()
all_pastures_area.loc['Native tropical savanna', 'Area [m^2]'] =0
all_pastures_area.loc['Tropical pastures', 'Area [m^2]'] *=2
all_pastures_mean =  total_biomass_mean + (mean_supp_biome_biomass_density*all_pastures_area['Area [m^2]']).sum()
all_pastures_median =  total_biomass_median + (median_supp_biome_biomass_density*all_pastures_area['Area [m^2]']).sum()

# Calculate the geometric mean of the average-based and median-based estimates
best_estimate = gmean([all_pastures_median,all_pastures_mean,all_savanna_mean,all_savanna_median])


print('Our best estimate for the biomass of annelids is %.1f Gt C' %(best_estimate/1e15))


# # Estimating the total number of annelids
# We consider only the Enchytraeids as they are ≈200-fold smaller than earthworms (Fierer et al.). We calculate the total biomass of Enchytraeids and divide it by the carbon content of Enchytraeids, which is ≈25 µg C (Fierer et al.):

# In[7]:

num_data = data.set_index('Biome')
# Calculate the total biomasss of Enchytraeids based on mean and median biomass densities
mean_ench_biomass = (num_data[num_data['Taxon'] == 'Enchytraeids']['Average biomass density [g C m^-2]']*area['Area [m^2]']).sum()
median_ench_biomass = (num_data[num_data['Taxon'] == 'Enchytraeids']['Median biomass density [g C m^-2]']*area['Area [m^2]']).sum()

# Calculate the geometric mean of both biomass estimates
ench_biomass = gmean([mean_ench_biomass, median_ench_biomass])

# The carbon content of Enchytraeids from Fierer et al.
ench_carbon_content = 25e-6

# Calculate the total number of Enchytraeids
tot_ench_num = ench_biomass/ench_carbon_content

print('Our best estimate for the total number of Enchytraeids is ≈%.0e' % tot_ench_num)


# In[8]:

# Feed results to the animal biomass data
old_results = pd.read_excel('../animal_biomass_estimate.xlsx',index_col=0)
result = old_results.copy()
result.loc['Annelids',(['Biomass [Gt C]','Uncertainty'])] = (best_estimate/1e15,np.nan)
result.to_excel('../animal_biomass_estimate.xlsx')

# Feed results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Animals','Annelids'), 
               col=['Biomass [Gt C]', 'Uncertainty'],
               values=[best_estimate/1e15,None],
               path='../../results.xlsx')


# Feed results to Table S1
update_results(sheet='Table S1', 
               row=('Animals','Annelids'), 
               col=['Number of individuals'],
               values=tot_ench_num,
               path='../../results.xlsx')


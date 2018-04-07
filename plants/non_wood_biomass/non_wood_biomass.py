
# coding: utf-8

# In[1]:

# Load dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean
import sys
sys.path.insert(0,'../../statistics_helper/')
from fraction_helper import *
from excel_utils import *


# # Estimating the fraction of plant biomass which is not woody
# To estimate the total non-woody plant biomass, we rely on two methods. The first is to estimate the global average leaf and root mass fractions, and the second is by estimating the total biomass of roots and leaves.
# 
# ## Method1 - fraction of leaves and roots
# To estimate the global average leaf and root mass fractions, we rely on a recent meta-analysis which collected data on the lead, shoot and root mass fractions in several different biomes ([Poorter et al.](http://dx.doi.org/10.1111/j.1469-8137.2011.03952.x)). Here are the mean leaf, shoot, and root mass fractions in each biome:

# In[2]:

# Load data from Poorter et al.
fractions = pd.read_excel('non_wood_biomass_data.xlsx','Poorter',skiprows=1,index_col=0)
fractions


# We calculate weighted mean of leaf and root mass fractions. We use the fraction of total plant biomass in each biome as our weights from [Erb et al.](http://dx.doi.org/10.1038/ngeo2782) for the weighted mean. Here is the data from Erb et al.:

# In[3]:

# Load data on the total plant biomass in each biome from Erb et al.
biomes = pd.read_excel('non_wood_biomass_data.xlsx','Erb',skiprows=1)
biomes


# The specific biomes in Erb et al. are not fully matching the biomes in Poorter et al., and thus we traslate between the biomes in the two studies:

# In[4]:

# Calculate the sum of the mass fractions of leaves and roots
non_wood_frac = (fractions['LMF']+fractions['RMF'])/fractions.sum(axis=1)

# Calculate the total biomass of each biome by the biomes reported in Poorter et al.
tot_biomass = biomes.groupby('Categories included in Poorter').sum()

# For the temperate steppe, desert and mountain, we use the mean values from grassland and shrubland in Poorter et al.
non_wood_frac.loc['Grassland, shrubland'] = frac_mean(np.array([non_wood_frac.loc['Grassland'],non_wood_frac.loc['Shrubland']]))


# Set the non-woody fraction as a column in the biome data
tot_biomass['Non wood fraction'] = non_wood_frac

# Calculate the weighed average of the non-woody biomass fraction
mean_non_wood_frac = np.average(tot_biomass['Non wood fraction'], weights= tot_biomass['Total biomass [Gt C]'])
print('Our global average for non-woody mass fraction is ≈%.0f percent' %(mean_non_wood_frac*100))


# Our estimate of the total non-woody plant biomass is the product of our best estimate of the total plant biomass and our estimate of the global average non-woody mass fraction:

# In[5]:


# Our best estimate for the total biomass
tot_plant_biomass = 450e15

# Multiply our estimate for the non-woody mass fraction by our estimate
# of the total plant biomass
method1_non_wood_biomass = mean_non_wood_frac*tot_plant_biomass

print('Our best estimate for the total non-wood plant biomass based on the fraction of roots and leaves is ≈%.0f Gt C' %(method1_non_wood_biomass/1e15))


# ## Method2 - total biomass of leaves and roots
# Our second method for estimating the total non-woody plant biomass is based on estimating the total biomass of roots and leaves. For roots, we rely on the estimate made by [Jackson et al.](http://dx.doi.org/10.1007/BF00333714):

# In[6]:

roots_jackson = 146e15


# To estimate the total biomass of leaves, we rely on biome averages on the leaf area index (LAI) from [Asner et al.](http://dx.doi.org/10.1046/j.1466-822X.2003.00026.x). Here is the data from Asner et al.:

# In[7]:

biome_LAI = pd.read_excel('non_wood_biomass_data.xlsx','Asner',skiprows=1,index_col=0)
biome_LAI


# We use data on the area on each biome from the book "Biogeochemistry", and multiply the LAI in each biome by the total area of each biome to estimate the global leaf area:

# In[8]:

# Load biome area data
biome_area = pd.read_excel('non_wood_biomass_data.xlsx','Biome area',skiprows=1,index_col=0)

# Calculate the mean LAI for boreal forests
biome_LAI.loc['Boreal forest'] = gmean(biome_LAI.loc[['Boreal DBL','Boreal ENL']])

# Calculate the mean LAI for temperate forests
biome_LAI.loc['Temperate forest'] = gmean(biome_LAI.loc[['Temperate DBL','Temperate EBL','Temperate ENL']])

# Calculate the mean LAI for tropical forests
biome_LAI.loc['Tropical forest'] = gmean(biome_LAI.loc[['Tropical DBL','Tropical EBL']])

# Calculate the mean LAI for temperate grasslands
biome_LAI.loc['Temperate grassland'] = biome_LAI.loc['Grassland']

# Calculate the mean LAI for tropical savanna
biome_LAI.loc['Tropical savanna'] = gmean(biome_LAI.loc[['Grassland','Shrubland']])

# Multiply the mean LAI in each biome by the total area of each biome
tot_leaf_area = (biome_LAI['LAI [m^2 m^-2]']*biome_area['Area [m^2]']).sum()
print('Our estimate for the total leaf area is ≈%.1e m^2' % tot_leaf_area)


# To convert the total leaf area into total biomass of leaves, we use an estimate for the average leaf mass per area (LMA) from the Glopnet database [Wright et al.](http://dx.doi.org/10.1038/nature02403):

# In[9]:

# Load the glopnet data
glopnet_data = pd.read_excel('non_wood_biomass_data.xlsx','glopnet_data',skiprows=1)

# Calculate the geometric mean of the LMA
geomean_LMA = 10**glopnet_data.loc[glopnet_data['GF']=='T',['log LMA']].mean()

# Convert the global leaf area to global leaf biomass
tot_leaf_biomass = tot_leaf_area*geomean_LMA/2

print('Our estimate for the global leaf biomass is ≈%.1f Gt C' %(tot_leaf_biomass/1e15))


# We sum our estimates for the total biomass of roots and leaves to produce our estimate of the total non-woody plant biomass:

# In[10]:

method2_non_wood_biomass = tot_leaf_biomass + roots_jackson
print('Our best estimate for the total non-wood plant biomass based on estimates of the total biomass of roots and leaves is ≈%.0f Gt C' %(method2_non_wood_biomass/1e15))


# We use the geometric mean of our estimates from the two methods as our best estimate for the total non-woody plant biomass:

# In[11]:

best_non_wood_biomass = gmean([method1_non_wood_biomass,method2_non_wood_biomass])
print('Our best estimate for the total non-wood plant biomass is ≈%.0f Gt C' %(best_non_wood_biomass/1e15))


# # Estimating the total belowground plant biomass
# To estimate the total belowground plant biomass, we use the same procedure as for estimating the total non-woody plant biomass. We rely on two methods - the first is based on calculating the mean root mass fraction.
# ## Method1 - fraction of roots
# To estimate the global average root mass fractions, we rely on a recent meta-analysis which collected data on the lead, shoot and root mass fractions in several different biomes ([Poorter et al.](http://dx.doi.org/10.1111/j.1469-8137.2011.03952.x)). We calculate the global average root mass fraction by taking into account the relative plant biomass present in each biome, based on data from [Erb et al.](http://dx.doi.org/10.1038/ngeo2782).

# In[12]:

# Calculate the root mass fraction in each biome based on data from Poorter et al.
root_frac = (fractions['RMF'])/fractions.sum(axis=1)

# For the temperate steppe, desert and mountain, we use the mean values from grassland and shrubland in Poorter et al.
root_frac.loc['Grassland, shrubland'] = frac_mean(np.array([root_frac.loc['Grassland'],root_frac.loc['Shrubland']]))


# Set the root fraction as a column in the biome data
tot_biomass['Root fraction'] = root_frac

# Calculate the weighted average root mass fraction
mean_root_frac = np.average(tot_biomass['Root fraction'], weights= tot_biomass['Total biomass [Gt C]'])

print('Our estimate for the global average root mass fraction is ≈%.1f percent' %(mean_root_frac*100))


# To estimate the total biomass of roots, we multiply the global average root mass fraction by our best estimate for the total plant biomass:

# In[13]:

method1_root_biomass = mean_root_frac*tot_plant_biomass

print('Our estimate of the total root biomass based on the global average root mass fraction is ≈%0.1f Gt C' %(method1_root_biomass/1e15))


# As a second source for estimating the global biomass of roots, we rely on the estimate in [Jackson et al.](http://dx.doi.org/10.1007/BF00333714). We use the geometric mean of the estimate from the two methods as our best estimate of the total biomass of roots, which we use as our best estimate for the total belowground plant biomass:

# In[14]:

best_root_biomass = gmean([method1_root_biomass,roots_jackson])

print('Our best estimate for the total belowground plant biomass is ≈%0.1f Gt C' %(best_root_biomass/1e15))


# In[15]:

# Feed results to Fig S1
update_results(sheet='FigS1', 
               row=('Plants','Plants'), 
               col=['Biomass [Gt C]'],
               values=best_non_wood_biomass/1e15,
               path='../../results.xlsx')

# Feed results to Data mentioned in MS
update_MS_data(row='Biomass of roots',
               values=best_root_biomass/1e15,
               path='../../results.xlsx')



# coding: utf-8

# In[1]:


# Load dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean
pd.options.display.float_format = '{:,.1e}'.format
import sys
sys.path.insert(0, '../../../statistics_helper')
from CI_helper import *

# Genaral parameters used in the estimate
ocean_area = 3.6e14
liters_in_m3 = 1e3
ml_in_m3 = 1e6


# # Estimating the total number of marine bacteria and archaea

# This notebook details the procedure for estimating the total number of marine bacteria and archaea.
# The estimate is based on three data sources:
# [Aristegui et al.](http://dx.doi.org/10.4319/lo.2009.54.5.1501),
# [Buitenhuis et al.](http://dx.doi.org/10.5194/essd-4-101-2012), and
# [Lloyd et al.](http://dx.doi.org/10.1128/AEM.02090-13)
# 

# In[2]:


# Load the datasets
buitenhuis = pd.read_excel('marine_prok_cell_num_data.xlsx','Buitenhuis',skiprows=1)
aristegui = pd.read_excel('marine_prok_cell_num_data.xlsx','Aristegui',skiprows=1)
aristegui[['Cell abundance (cells m-2)','SE']] = aristegui[['Cell abundance (cells m-2)','SE']].astype(float)
lloyd = pd.read_excel('marine_prok_cell_num_data.xlsx','Lloyd',skiprows=1)


# Here are samples from the data in Aristegui et al.:

# In[3]:


aristegui.head()


# From the data in Buitenhuis et al.:

# In[4]:


buitenhuis.head()


# And from Llyod et al.:

# In[5]:


lloyd.head()


# For Aristegui et al. we estimate the total number of cells by multiplying each layer by the surface area of the ocean

# In[6]:


aristegui_total = (aristegui['Cell abundance (cells m-2)']*ocean_area).sum()
print('Total number of cells based on Aristegui et al.: %.1e' % aristegui_total)


# For Buitenhuis et al. we bin the data along 100 meter depth bins, and estimate the average cell abundance in each bin. We then multiply the total number of cells per liter by the volume at each depth and sum across layers.

# In[7]:


# Define depth range every 100 m from 0 to 4000 meters
depth_range = np.linspace(0,4000,41)

#Bin data along depth bins
buitenhuis['Depth_bin'] = pd.cut(buitenhuis['Depth'], depth_range)

#For each bin, calculate the average number of cells per liter
buitenhuis_bins = buitenhuis.groupby(['Depth_bin']).mean()['Bact/L']

#Multiply each average concentration by the total volume at each bin: 100 meters depth times the surface area of the oceac

buitenhuis_bins *= 100*ocean_area*liters_in_m3

#Sum across all bins to get the total estimate for the number of cells of marine prokaryotes
buitenhuis_total = buitenhuis_bins.sum()
print('Total number of cells based on Buitenhuis et al.: %.1e' % buitenhuis_total)


# For Lloyd et al., we rely on the sum of the total number of bacteria and archaea. The estimate for the number of bacteria and archaea is based on the regression of the concentration of bacteria and archaea with depth. We use the equations reported in Lloyd et al. to extrapolate the number of cells of bacteria and archaea across the average ocean depth of 4000 m.

# In[8]:


# Define the regression equation for the number of bacteria in the top 64 m:
def bac_surf(depth):
    result = np.zeros_like(depth)
    for i,x in enumerate(depth):
        if x==0 :
            result[i] = 5.54
            
        else:
            result[i] = np.log10(x)*0.08+5.54
    return 10**result

# Define the regression equation for the number of bacteria in water deeper than 64 m:
bac_deep = lambda x: 10**(np.log10(x)*-1.09+7.66)

# Define the regression equation for the number of bacteria in the top 389 m:
def arch_surf(depth):
    result = np.zeros_like(depth)
    for i,x in enumerate(depth):
        if x==0 :
            result[i] = 4.1
            
        else:
            result[i] = np.log10(x)*0.1+4.1
    return 10**result

# Define the regression equation for the number of bacteria in water below 389 m:
arch_deep = lambda x: 10**(np.log10(x)*-0.8+6.43)

# Estimate the total number of bacteria in the top 64 m by first estimating the concentration using the 
# regression equation, multiplying by the volume at each depth, which is 1 m^3 times the surface
# Area of the ocean, and finally summing across different depths
total_bac_surf = (bac_surf(np.linspace(0,64,65))*ml_in_m3*ocean_area).sum()

# We repeat the same procedure for the total number of bacteria in waters deeper than 64 m, and for the total
# Number of archaea
total_bac_deep = (bac_deep(np.linspace(65,4000,4000-65+1))*ml_in_m3*ocean_area).sum()
total_arch_surf = (arch_surf(np.linspace(0,389,390))*ml_in_m3*ocean_area).sum()
total_arch_deep = (arch_deep(np.linspace(390,4000,4000-390+1))*ml_in_m3*ocean_area).sum()

# Sum across bacteria and archaea to get the estimate for the total number of bacteria and archaea in the ocean
lloyd_total = total_bac_surf+total_bac_deep+total_arch_surf+total_arch_deep
print('Total number of cells based on Lloyd et al.: %.1e' % lloyd_total)


# The estimate of the total number of cells in Lloyd et al. is based on FISH measurements, but in general not all cells which are DAPI positive are also stained with FISH. To correct for this effect, we estimate the average FISH yield across samples, and divide our estimate from the FISH measurements by the average FISH yield.

# In[9]:


fish_yield = lloyd['FISH yield'].dropna()

# Values which are not feasible are turned to the maximal value. We do not use 1 because of numerical reasons
fish_yield[fish_yield >=1] = 0.999

# calculate the statistics on the fish_visible/fish_invisible value and not the 
# fish_visible/(fish_visible+fish_invisible) value because the first is not bound by 0 and 1
# We transform the values to log space to calculate the geometric mean
alpha_fish_yield = np.log10(1./(1./fish_yield[fish_yield<1]-1.))
mean_alpha_yield = np.average(-alpha_fish_yield.dropna())
mean_yield = 1./(1.+10**mean_alpha_yield)

print('The mean yield of FISH is %.1f' % mean_yield)
lloyd_total /= mean_yield
print('After correcting for FISH yield, the estimate for the total number of bacteria and archaea based on Lloyd et al is %.1e' % lloyd_total)



# Our best estimate for the total number of marine bacteria and archaea is the geometric mean of the estimates from Aristegui et al., Buitenhuis et al. and Lloyd et al.

# In[10]:


estimates = [aristegui_total,buitenhuis_total,lloyd_total]
best_estimate = 10**(np.log10(estimates).mean())

print('Our best estimate for the total number of marine bacteria and archaea is %.1e' %best_estimate)


# # Uncertainty analysis
# 
# To calculate the uncertainty associated with the estimate for the total number of of bacteria and archaea, we first collect all available uncertainties and then take the largest value as our best projection for the uncertainty. 
# 
# ## Intra-study uncertainties 
# We first survey the uncertainties reported in each of the studies. Aristegui et al. report a standard error of ≈10% for the average cell concentration per unit area. Buitenhuis et al. and Lloyd et al. do not report uncertainties.
# 
# ## Interstudy uncertainties
# 
# We estimate the 95% multiplicative error of the geometric mean of the values from the three studies.

# In[11]:


mul_CI = geo_CI_calc(estimates)

print('The interstudy uncertainty is about %.1f-fold' % mul_CI)


# We thus take the highest uncertainty from our collection which is ≈1.4-fold.
# Our final parameters are:

# In[12]:


print('Total number of marine bacteria and archaea: %.1e' % best_estimate)
print('Uncertainty associated with the total number of marine bacteria and archaea: %.1f-fold' % mul_CI)

old_results = pd.read_excel('../marine_prok_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[0] = pd.Series({
                'Parameter': 'Total number of marine bacteria and archaea',
                'Value': int(best_estimate),
                'Units': 'Cells',
                'Uncertainty': "{0:.1f}".format(mul_CI)
                })

result.to_excel('../marine_prok_biomass_estimate.xlsx',index=False)


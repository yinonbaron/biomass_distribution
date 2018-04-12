
# coding: utf-8

# In[1]:


# Load dependencies 
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '../../../statistics_helper')
from fraction_helper import *
from openpyxl import load_workbook
pd.options.display.float_format = '{:,.1e}'.format
# Genaral parameters used in the estimate
ocean_area = 3.6e14
liters_in_m3 = 1e3
ml_in_m3 = 1e6


# # Estimating the fraction of marine archaea out of the total marine prokaryote population

# In order to estimate the fraction of archaea out of the total population of marine bacteria and archaea, we rely of two independent methods: fluorescent in-situ hybridization (FISH) and 16S rDNA sequencing. For each one of the methods, we calculate the fraction of archaea out of the total population of marine bacteria and archaea in the three depth layers of the ocean - the epieplagic (< 200 meters depth), the mesopelagic (200-1000 meters depth) and bathypelagic (1000-4000 meters depth).
# 
# ### FISH based estimate
# For our FISH based estimate we rely on data from [Lloyd et al.](http://dx.doi.org/10.1128/AEM.02090-13). Here is a sample of the data:

# In[2]:


# Load the dataset
lloyd = pd.read_excel('marine_arch_frac_data.xlsx','Lloyd',skiprows=1)
lloyd.head()


# The data in Lloyd et al. contains estimates for the number of bacteria and archaea. Lloyd et al. generated regression equations for the concentration of bacteria and archaea as a function of depth. We use these equations to estimate the total number of archaea and bacteria at each of the three depth layers.

# In[3]:


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

# Define the regression equation for the number of archaea in the top 389 m:
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

# Estimate the total number of bacteria and archaea in the epipelagic layer by first estimating the concentration using the 
# regression equation, multiplying by the volume at each depth, which is 1 m^3 times the surface
# Area of the ocean, and finally summing across different depths
total_bac_epi = (bac_surf(np.linspace(0,64,65))*ml_in_m3*ocean_area).sum() + (bac_deep(np.linspace(65,200,200-65+1))*ml_in_m3*ocean_area).sum()
total_arch_epi = (arch_surf(np.linspace(0,200,201))*ml_in_m3*ocean_area).sum()

# Calculate the fraction of archaea in the epipelagic layer
FISH_arch_frac_epi = total_arch_epi/(total_arch_epi+total_bac_epi)


# We repeat the same procedure for the total number of bacteria and archaea in the mesopelagic layer
# Number of archaea
total_bac_meso = (bac_deep(np.linspace(201,1000,1000-200+1))*ml_in_m3*ocean_area).sum()
total_arch_meso = (arch_surf(np.linspace(201,389,390-201+1))*ml_in_m3*ocean_area).sum() + (arch_deep(np.linspace(390,1000,1000-390+1))*ml_in_m3*ocean_area).sum()

# Calculate the fraction of archaea in the mesopelagic layer
FISH_arch_frac_meso = total_arch_meso/(total_arch_meso+total_bac_meso)

# We repeat the same procedure for the total number of bacteria and archaea in the mesopelagic layer
# Number of archaea
total_bac_bathy = (bac_deep(np.linspace(1001,4000,4000-1001+1))*ml_in_m3*ocean_area).sum()
total_arch_bathy = (arch_deep(np.linspace(1001,4000,4000-1001+1))*ml_in_m3*ocean_area).sum()

# Calculate the fraction of archaea in the bathypelagic layer
FISH_arch_frac_bathy = total_arch_bathy/(total_arch_bathy+total_bac_bathy)

print('The fraction of archaea in the epipelagic layer based on FISH is %.1f percent' % (FISH_arch_frac_epi*100))
print('The fraction of archaea in the mesopelagic layer based on FISH is %.1f percent' % (FISH_arch_frac_meso*100))
print('The fraction of archaea in the bathypelagic layer based on FISH is %.1f percent' % (FISH_arch_frac_bathy*100))


# ### 16S rDNA sequencing
# 
# To estimate the fraction of archaea out of the total population of marine bacteria and archaea, we rely on data from [Sunagawa et al.](http://science.sciencemag.org/content/348/6237/1261359) for the epipelagic and mesopelagic layers, and data from [Salazar et al.](http://dx.doi.org/10.1038/ismej.2015.137) for the bathypelagic layer.

# In[4]:


sunagawa = pd.read_excel('marine_arch_frac_data.xlsx','Sunagawa',skiprows=1,index_col=0)
salazar = pd.read_excel('marine_arch_frac_data.xlsx','Salazar')


# Here are samples from the data in Sunagawa et al.:

# In[5]:


sunagawa.head()


# Here are samples from the data in Salazar et al.:

# In[6]:


salazar.head()


# As we are working with fractions here, we shall use a utility that will calculate mean and uncertainty of fractions. For details regarding the procedure look at the documentation of the relevant functions.
# For the epipelagic layer, we will use the sum of the fractions of Thaumarcheota and Euryarchaeota, two main archaeal phyla. We will use the geometric mean of the fractions in surface waters and the deep chlorophyll maximum.

# In[7]:


sunagawa_sum = (sunagawa['Thaumarcheota'] + sunagawa['Euryarchaeota'])/100
seq_arch_frac_epi = frac_mean(sunagawa_sum.loc[['DCM','SRF']])
seq_arch_frac_meso = frac_mean(sunagawa_sum.loc['MESO'])
print('The fraction of archaea in the epipelagic layer based on 16S rDNA sequencing is %.1f percent' % (seq_arch_frac_epi*100))
print('The fraction of archaea in the mesopelagic layer based on 16S rDNA sequencing is %.1f percent' % (seq_arch_frac_meso*100))


# For the bathypelagic layer, we estimate the fraction of archaea based on 16S rDNA sequencing by using the geometric mean of the data in Salazar et al.

# In[8]:


seq_arch_frac_bathy = frac_mean(salazar['Archaea'])
print('The fraction of archaea in the bathypelagic layer based on 16S rDNA sequencing is %.1f percent' % (seq_arch_frac_bathy*100))


# Our best estimate for the fraction of archaea out of the total population of marine bacteria and archaea at each layer is the geometric mean of the estimates of the fraction of archaea based on FISH and on 16S rDNA sequencing, corrected for the lower rDNA operon copy number

# In[9]:


best_arch_frac_epi = frac_mean(np.array([FISH_arch_frac_epi,seq_arch_frac_epi*2]))
best_arch_frac_meso = frac_mean(np.array([FISH_arch_frac_meso,seq_arch_frac_meso*2]))
best_arch_frac_bathy = frac_mean(np.array([FISH_arch_frac_bathy,seq_arch_frac_bathy*2]))
print('The best estimate for the fraction of archaea in the epipelagic layer is %.1f percent' % (best_arch_frac_epi*100))
print('The best estimate for the fraction of archaea in the mesopelagic layer is %.1f percent' % (best_arch_frac_meso*100))
print('The best estimate for the fraction of archaea in the bathypelagic layer is %.1f percent' % (best_arch_frac_bathy*100))


# ### Estimating the fraction of the population in each depth layer
# In order to calculate the fraction of archaea out of the total population of marine bacteria and archaea, we need to estimate the fraction of cells in epipelagic, mesopelagic and bathypelagic layers. To do so we use the same sources used for estimating the total number of marine bacteria and archaea, namely, Aristegui et. al, Buitenhuis et al. and Lloyd et al. 

# In[10]:


# Load the datasets
buitenhuis = pd.read_excel('../cell_num/marine_prok_cell_num_data.xlsx','Buitenhuis',skiprows=1)
aristegui = pd.read_excel('../cell_num/marine_prok_cell_num_data.xlsx','Aristegui',skiprows=1)


# For Lloyd et al., we already calculated the total number of bacteria and archaea at each layer, so we can estimate what is the relative fraction of cells in each layer

# In[11]:


# For lloyd et al. we calculate fraction of the sum of bacteria and archaea in each layer out of the 
# total number of bacteria and archaea

lloyd_total_bac_arch_epi = total_arch_epi + total_bac_epi
lloyd_total_bac_arch_meso = total_arch_meso + total_bac_meso
lloyd_total_bac_arch_bathy = total_arch_bathy + total_bac_bathy
lloyd_total_bac_arch = lloyd_total_bac_arch_epi+lloyd_total_bac_arch_meso+lloyd_total_bac_arch_bathy

lloyd_epi_frac = lloyd_total_bac_arch_epi/lloyd_total_bac_arch
lloyd_meso_frac = lloyd_total_bac_arch_meso/lloyd_total_bac_arch
lloyd_bathy_frac = lloyd_total_bac_arch_bathy/lloyd_total_bac_arch

print('The fraction of cells in the epipelagic layer according to Lloyd et al. is %.1f  percent' % (lloyd_epi_frac*100))
print('The fraction of cells in the mesopelagic layer according to Lloyd et al. is %.1f  percent' % (lloyd_meso_frac*100))
print('The fraction of cells in the bathypelagic layer according to Lloyd et al. is %.1f  percent' % (lloyd_bathy_frac*100))

For Buitenhuis et al., we bin the data along the depth of each sample in 100 m bins. We calculate the average concentration of cells at each bin. For each bin, we calculate the total number of cells in the bin by multiplying the average concentration by the total volume of water in the bin. We calculate the total number of cells in each layer by dividing the bins to each of the layers and summing across all the bins that belong to the same layer.
# In[12]:


# Define depth range every 100 m from 0 to 4000 meters
depth_range = np.linspace(0,4000,41)

# Bin data along depth bins
buitenhuis['Depth_bin'] = pd.cut(buitenhuis['Depth'], depth_range)

# For each bin, calculate the average number of cells per liter
buitenhuis_bins = buitenhuis.groupby(['Depth_bin']).mean()['Bact/L']

# Multiply each average concentration by the total volume at each bin: 100 meters depth time the surface area of the oceac

buitenhuis_bins *= 100*ocean_area*liters_in_m3

# For the epipelagic layer, sum across the first three bins
buitenhuis_total_epi = buitenhuis_bins.iloc[0:3].sum()

# For the mesopelagic layer, sum across the relevant bins
buitenhuis_total_meso = buitenhuis_bins.iloc[3:11].sum()

# For the bathypelagic layer, sum across the remaining bins
buitenhuis_total_bathy = buitenhuis_bins.iloc[12:].sum()

#Calculate the total number of cells
buitenhuis_total = buitenhuis_bins.sum()

# Calculate relative fractions
buitenhuis_frac_epi = buitenhuis_total_epi/buitenhuis_total
buitenhuis_frac_meso = buitenhuis_total_meso/buitenhuis_total
buitenhuis_frac_bathy = buitenhuis_total_bathy/buitenhuis_total
print('Total fraction of cells in the epipelagic layer based on Buitenhuis et al.: %.1f percent' % (buitenhuis_frac_epi*100))
print('Total fraction of cells in the mesopelagic layer based on Buitenhuis et al.: %.1f percent' % (buitenhuis_frac_meso*100))
print('Total fraction of cells in the bathypelagic layer based on Buitenhuis et al.: %.1f percent' % (buitenhuis_frac_bathy*100))


# For Aristegui et al. the data is already binned along each layer, so we just calculate the relative fraction of each layer

# In[13]:


aristegui_total = aristegui['Cell abundance (cells m-2)'].sum()
aristegui_frac_epi = aristegui.iloc[0]['Cell abundance (cells m-2)']/aristegui_total
aristegui_frac_meso = aristegui.iloc[1]['Cell abundance (cells m-2)']/aristegui_total
aristegui_frac_bathy = aristegui.iloc[2]['Cell abundance (cells m-2)']/aristegui_total
print('Total fraction of cells in the epipelagic layer based on Aristegui et al.: %.1f percent' % (aristegui_frac_epi*100))
print('Total fraction of cells in the mesopelagic layer based on Aristegui et al.: %.1f percent' % (aristegui_frac_meso*100))
print('Total fraction of cells in the bathypelagic layer based on Aristegui et al.: %.1f percent' % (aristegui_frac_bathy*100))


# Our best estimate for the fraction of bacterial and archaeal cells located at each layer is the geometric mean of estiamtes for our three resources - Lloyd et al., Buitenhuis et al., and Aristegui et al.

# In[14]:



best_frac_epi = frac_mean(np.array([lloyd_epi_frac,buitenhuis_frac_epi,aristegui_frac_epi]))
best_frac_meso = frac_mean(np.array([lloyd_meso_frac,buitenhuis_frac_meso,aristegui_frac_meso]))
best_frac_bathy = frac_mean(np.array([lloyd_bathy_frac,buitenhuis_frac_bathy,aristegui_frac_bathy]))

print('The best estimate for the fraction of cells in the epipelagic layer is %.1f percent' % (best_frac_epi*100))
print('The best estimate for the fraction of cells in the mesopelagic layer is %.1f percent' % (best_frac_meso*100))
print('The best estimate for the fraction of cells in the bathypelagic layer is %.1f percent' % (best_frac_bathy*100))


# Our best estimate for the fraction of archaea out of the total population of marine bacteria and archaea is the weighted sum of the fraction of archaea in each layer and the fraction of total cells in each layer

# In[15]:


best_arch_frac = best_arch_frac_epi*best_frac_epi + best_arch_frac_meso*best_frac_meso+best_arch_frac_bathy*best_frac_bathy
print('Our best estimate for the fraction of archaea out of the total population of marine bacteria and archaea is %.1f percent' %(best_arch_frac*100))


# # Uncertainty analysis
# 
# In order to assess the uncertainty associated with our estimate for the fraction of marine archaea out of the total population of marine bacteria and archaea, we gather all possible indices of uncertainty. We compare the uncertainty of values within each one of the methods and the uncertainty stemming from the variability of the values provided by the two methods. 
# 
# ## Intra-study uncertainty
# We first look at the uncertainty of values within the FISH method and the 16S sequencing method.
# 
# ### FISH method
# For the FISH method, as we use regression lines to extrapolate the number of archaea and bacteria across the depth profile. We do not have a good handle of the uncertainty of this procedure. We thus use an alternative measure for the uncertainty of the fraction of archaea. Lloyd et al. reports in each site the fraction of archaea out of the total population of bacteria and archaea. We use the variation of the values between sites as a measure of the uncertainty of the values for the fraction of archaea and bacteria using FISH.

# In[16]:


# Set zero values to a small number for numerical stability of the fraction
lloyd_arc_frac = lloyd['Fraction Arc CARDFISH'].dropna()
lloyd_arc_frac[lloyd_arc_frac == 0] = 0.001

print('The intra-study uncertainty of measurements using FISH for the fraction of archaea is %.1f-fold' % frac_CI(lloyd_arc_frac))
print('The intra-study uncertainty of measurements using FISH for the fraction of bacteria is %.2f-fold' % frac_CI(1.-lloyd_arc_frac))


# ### 16S rDNA sequencing
# 
# For the 16S rDNA sequencing method, we rely of two main resources - Sunagawa et al. for the epipelagic and mesopelagic layers, and Salazar et al. for the bathypelagic layer. No uncertainties are reported by Sunagawa et al., and thus we rely on the variability of values in Salazar et al. as a measure of the uncertainty of the values for the fraction of archaea using 16S rDNA sequencing

# In[17]:


print('The intra-study uncertainty of measurements using 16S rDNA sequencing for the fraction of archaea is %.1f-fold' % frac_CI(salazar['Archaea']))
print('The intra-study uncertainty of measurements using 16S rDNA sequencing for the fraction of bacteria is %.2f-fold' % frac_CI(1.-salazar['Archaea']))


# ## Interstudy uncertainty
# 
# We calculate the uncertainty (95% multiplicative confidence interval) between the estimates using the two methods - FISH and 16S rDNA sequencing.

# In[18]:


# For each layer, calculate the uncertainty between methods
from fractions import *
epi_mul_CI_arch = frac_CI(np.array([FISH_arch_frac_epi,seq_arch_frac_epi]))
meso_mul_CI_arch = frac_CI(np.array([FISH_arch_frac_meso,seq_arch_frac_meso]))
bathy_mul_CI_arch = frac_CI(np.array([FISH_arch_frac_bathy,seq_arch_frac_bathy]))
print('The uncertainty of the fraction of archaea out of the total population of bacteria and archaea in the epipelagic layer is %.1f-fold' %epi_mul_CI_arch)
print('The uncertainty of the fraction of archaea out of the total population of bacteria and archaea in the mesopelagic layer is %.1f-fold' %meso_mul_CI_arch)
print('The uncertainty of the fraction of archaea out of the total population of bacteria and archaea in the bathypelagic layer is %.1f-fold' %bathy_mul_CI_arch)

epi_mul_CI_bac = frac_CI(np.array([1.-FISH_arch_frac_epi,1.-seq_arch_frac_epi]))
meso_mul_CI_bac = frac_CI(np.array([1.-FISH_arch_frac_meso,1.-seq_arch_frac_meso]))
bathy_mul_CI_bac = frac_CI(np.array([1.-FISH_arch_frac_bathy,1.-seq_arch_frac_bathy]))
print('The uncertainty of the fraction of bacteria out of the total population of bacteria and archaea in the epipelagic layer is %.1f-fold' %epi_mul_CI_bac)
print('The uncertainty of the fraction of bacteria out of the total population of bacteria and archaea in the mesopelagic layer is %.1f-fold' %meso_mul_CI_bac)
print('The uncertainty of the fraction of bacteria out of the total population of bacteria and archaea in the bathypelagic layer is %.1f-fold' %bathy_mul_CI_bac)


# As our best estimates for the uncertainty associated with the fraction of archaea and bacteria out of the total population of marine bacteria and archaea, we use the highest uncertainty out of the uncertainties of the three depth layers.
# 
# The highest interstudy uncertainty for the fraction of archaea is ≈1.8-fold, which is higher than the highest intra-study uncertainty of ≈1.2-fold, so we use ≈1.8-fold as our best projection of the uncertainty associated with the fraction of archaea out of the total population of marine bacteria and archaea. 
# Similarly, the highest interstudy uncertainty for the fraction of bacteria is ≈1.2-fold, which is higher than the highest intra-study uncertainty of ≈1.03-fold, so we use ≈1.2-fold as our best projection of the uncertainty associated with the fraction of bacteria out of the total population of marine bacteria and archaea. 
# 
# Our final parameters are:

# In[19]:


print('Fraction of marine archaea out of the total population of marine bacteria and archaea: %.1f percent' %(best_arch_frac*100))
print('Fraction of marine bacteria out of the total population of marine bacteria and archaea: %.1f percent' %(100.-best_arch_frac*100))
print('Uncertainty associated with the fraction of marine archaea: %.1f-fold' % np.max([epi_mul_CI_arch,meso_mul_CI_arch,bathy_mul_CI_arch]))
print('Uncertainty associated with the fraction of marine bacteria: %.1f-fold' % np.max([epi_mul_CI_bac,meso_mul_CI_bac,bathy_mul_CI_bac]))

old_results = pd.read_excel('../marine_prok_biomass_estimate.xlsx')
result = old_results.copy()


if (result.shape[0]==0):
    result = pd.DataFrame(index= range(2), columns=['Parameter','Value','Units','Uncertainty'])


result.loc[2] = pd.Series({
                'Parameter': 'Fraction of archaea',
                'Value': "{0:.1f}".format(best_arch_frac),
                'Units': 'Unitless',
                'Uncertainty': "{0:.1f}".format(np.max([epi_mul_CI_arch,meso_mul_CI_arch,bathy_mul_CI_arch]))
                })

result.loc[3] = pd.Series({
                'Parameter': 'Fraction of bacteria',
                'Value': "{0:.1f}".format(1.0 - best_arch_frac),
                'Units': 'Unitless',
                'Uncertainty': "{0:.1f}".format(np.max([epi_mul_CI_bac,meso_mul_CI_bac,bathy_mul_CI_bac]))
                })


result.to_excel('../marine_prok_biomass_estimate.xlsx',index=False)

# We need to use the results on the amount of cells in the epipelagic layer for our estimate of
# the total biomass of marine fungi, so we feed these results to the data used in the estimate
# of the biomass of marine fungi
marine_fungi_data = pd.read_excel('../../../fungi/marine_fungi/marine_fungi_data.xlsx','Bacteria biomass')

marine_fungi_data.loc[0] = pd.Series({
                'Parameter': 'Fraction of prokaryotes in epipelagic realm',
                'Value': best_frac_epi,
                'Units': 'Unitless',
                'Uncertainty': frac_CI(np.array([lloyd_epi_frac,buitenhuis_frac_epi,aristegui_frac_epi]))
                })
writer = pd.ExcelWriter('../../../fungi/marine_fungi/marine_fungi_data.xlsx', engine = 'openpyxl')
book = load_workbook('../../../fungi/marine_fungi/marine_fungi_data.xlsx')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)


marine_fungi_data.to_excel(writer, sheet_name = 'Bacteria biomass',index=False)
writer.save()



# coding: utf-8

# In[1]:

# Load dependencies
import pandas as pd
import sys
sys.path.insert(0,'../../statistics_helper/')
from excel_utils import *
from openpyxl import load_workbook


# # Estimating the biomass of molluscs
# To estimate the biomass of molluscs, we estimate the biomass of two major components of mollusc biomass - pteropods and cephalopods. In this work we assume the contribution of other types of molluscs is limited compared to pteropods and cephalopods.
# 
# ## Pteropods
# Our estimate of the global biomass of pteropods is based on data from the MAREDAT database ([Buitenhuis et al.](http://search.proquest.com/openview/0e8e5672fa28111df473268e13f2f757/1?pq-origsite=gscholar&cbl=105729)). 
# 
# Buitenhuis et al. generated two estimates for the global biomass of pteropods by using a characteristic biomass concentration for each depth (either a median or average of the values in the database) and applying it across the entire volume of ocean at that depth. This approach results in two types of estimates for the global biomass of pteropods: a so called “minimum” estimate which uses the median concentration of biomass from the database, and a so called “maximum” estimate which uses the average biomass concentration. Because the distributions of values in the database are usually highly skewed by asymmetrically high values, the median and mean are loosely associated by the MAREDAT authors with a minimum and maximum estimate. The estimate based on the average value is more susceptible to biases in oversampling singular locations such as blooms of plankton species, or of coastal areas in which biomass concentrations are especially high, which might lead to an overestimate. On the other hand, the estimate based on the median biomass concentration might underestimate global biomass as it will reduce the effect of biologically relevant high biomass concentrations. Therefore, our best estimate of the biomass of pteropods is the geometric mean of the “minimum” and “maximum” estimates. Buitenhuis et al. reports a "minimum" estimate of 0.026 Gt C and a "maximum" estimate of 0.67 Gt C. We calculate the geometric mean of those estimates:

# In[2]:

from scipy.stats import gmean

# The estimate of pteropod biomass based on average biomass density
average_biomass = 0.67e15

# The estimate of pteropod biomass based on median biomass density
median_biomass = 0.026e15

# Our best estimate for the biomass of pteropods is the geometric mean of the average-based
# and median-based estimates
pteropod_estimate = gmean([average_biomass,median_biomass])

print('Our best estimate for the total biomass of pteropods is ≈%.2f Gt C' %(pteropod_estimate/1e15))


# ## Cephalopods
# Our estimate of the total biomass of cephalopods is based on an estimate by [Rodhouse & Nigmatullin](http://dx.doi.org/10.1098/rstb.1996.0090), which put cephalopod biomass at ≈0.05 Gt C.

# In[3]:

# Estimate for the total biomass of cephalopods from Rodhouse & Nigmatullin
cephalopod_biomass = 0.05e15


# Our best estimate for the total biomass of molluscs is the sum of our estimates for the total biomass of pteropods and cephalopods:

# In[4]:

best_estimate = pteropod_estimate +cephalopod_biomass
print('Our best estimate for the total biomass of molluscs is %.1f Gt C' %(best_estimate/1e15))


# # Estimating the total number of molluscs
# To estimate the total number of molluscs, we consider the total biomass of pteropods and divide it by the average carbon content of a single pteropod. To estimate the characteristic carbon content of a single pteropod, we rely on data from [Bednaršek et al.](https://doi.org/10.5194/essd-4-167-2012). Bednaršek et al. measured biomass of population densities pteropods per cubic meter. We divide these two measurements by one another to estimate the carbon content of a single pteropod. We use the mean across all samples as our best estimate for the characteristic carbon content of a single pteropod.

# In[5]:

# Load data from Bednaršek et al.
data = pd.read_excel('carbon_content_data.xlsx',skiprows=4)

# Calculate the characteristic carbon content of a single pteropod
best_cc = data['Biomass (mg/m3)'].mean()/data['Abundace (ind./m3)'].mean()*1e-3

# Calculate the total number of molluscs
tot_molluscs_num = pteropod_estimate/best_cc

print('Our best estimate for the total number of pteropods is ≈%.1e' %tot_molluscs_num)


# In[6]:

# Feed results to the chordate biomass data
old_results = pd.read_excel('../animal_biomass_estimate.xlsx',index_col=0)
result = old_results.copy()
result.loc['Molluscs',(['Biomass [Gt C]','Uncertainty'])] = (best_estimate/1e15,None)
result.to_excel('../animal_biomass_estimate.xlsx')

# Feed results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Animals','Molluscs'), 
               col=['Biomass [Gt C]', 'Uncertainty'],
               values=[best_estimate/1e15,None],
               path='../../results.xlsx')

# Feed results to Table S1
update_results(sheet='Table S1', 
               row=('Animals','Molluscs'), 
               col='Number of individuals',
               values= tot_molluscs_num,
               path='../../results.xlsx')

# We need to use the results on the biomass of pteropods for our estimate
# of the total biomass of marine arthropods, so we feed these results to 
# the data used in the estimate of the total biomass of marine arthropods
path = '../arthropods/marine_arthropods/marine_arthropods_data.xlsx'
marine_arthropods_data = pd.read_excel(path,'Other macrozooplankton')

marine_arthropods_data.loc[1] = pd.Series({
                'Parameter': 'Biomass of pteropods',
                'Value': pteropod_estimate,
                'Units': 'g C',
                'Uncertainty': None
                })
writer = pd.ExcelWriter(path, engine = 'openpyxl')
book = load_workbook(path)
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)


marine_arthropods_data.to_excel(writer, sheet_name = 'Other macrozooplankton',index=False)
writer.save()



# coding: utf-8

# In[1]:

# Load dependencies
import pandas as pd
import sys
sys.path.insert(0,'../../statistics_helper/')
from openpyxl import load_workbook
from excel_utils import *


# # Estimating the biomass of Cnidarians
# To estimate the total biomass of cnidarians, we combine estimates for two main groups which we assume dominate the biomass of cnidarains = planktonic cnidarians (i.e. jellyfish) and corals. We describe the procedure for estimating the biomass of each group
# 
# ## Planktonic cnidarians
# Our estimate of the total biomass of plaktonic cnidarians is based on [Lucas et al.](http://dx.doi.org/10.1111/geb.12169), which assembled a large dataset of abundance mauresments of different dypes of gelatinous zooplankton. Globally, they estimate ≈0.04 Gt C of gelatinous zooplankton, of which 92% are contributed by cnidarians. Therefore, we estimate the total biomass of planktonic cnidarians at ≈0.04 Gt C.
# 

# In[2]:

planktonic_cnidarian_biomass = 0.04e15


# ## Corals
# The procedure we take to estimate the total biomass of corals in coral reefs is to first calculate the total surface area of coral tissue globally, and then convert this value to biomass by the carbon mass density of coral tissue per unit surface area. We estimate the total surface area of corals worldwide using two approaches. 
# 
# The first approach estimates the total surface area of corals using the total area of coral reefs (in $m^2$) from [Harris et al.](http://dx.doi.org/10.1016/j.margeo.2014.01.011). 

# In[3]:

# Total surface area of coral reefs
coral_reef_area = 0.25e12


# We estimate that 20% of the reef area is covered by corals based on [De'ath et al.](http://dx.doi.org/10.1073/pnas.1208909109).

# In[4]:

# Coverage of coral reef area by corals
coverage = 0.2


# This gives us the projected area of corals. Corals have a complex 3D structure that increases their surface area. To take this effect into account, we use a recent study that estimated the ratio between coral tissue surface area and projected area at ≈5 ([Holmes & Glen](http://dx.doi.org/10.1016/j.jembe.2008.07.045)).

# In[5]:

# The conversion factor from projected surface area to actual surface area
sa_3d_2a = 5


# Multiplying these factors, we get an estimate for the total surface area of corals:

# In[6]:

# Calculate the total surface area of corals
method1_sa = coral_reef_area*coverage*sa_3d_2a

print('Our estimate of the global surface area of corals based on our first method is ≈%.1f×10^11 m^2' % (method1_sa/1e11))


# The second approach uses an estimate of the global calcification rate in coral reefs based on [Vecsei](http://dx.doi.org/10.1016/j.gloplacha.2003.12.002). 

# In[7]:

# Global annual calcufocation rate of  corals [g CaCO3 yr^-1]
annual_cal = 0.75e15


# We divide this rate by the surface area specific calcification rate of corals based on values from [McNeil](http://dx.doi.org/10.1029/2004GL021541) and [Kuffner et al.](http://dx.doi.org/10.1007/s00338-013-1047-8). Our best estimate for the surface area specific calcification rate is the geometric mean of values from the two sources above.

# In[8]:

from scipy.stats import gmean
# Surface area specific calcification rate from McNeil, taken from figure 1 [g CaCO3 m^-2 yr^-1]
mcneil_cal_rate = 1.5e4

# Surface area specific calcification rate from Kuffner et al., taken from first
# Sentence of Discussion [g CaCO3 m^-2 yr^-1]
kuffner_cal_rate = 0.99e4

# Our best estimate for the surface area specific calcification rate is the geometric mean of the two values
best_cal_rate = gmean([mcneil_cal_rate,kuffner_cal_rate])

# Calculate the surface area of corals
method2_sa = annual_cal/best_cal_rate

print('Our estimate of the global surface area of corals based on our second method is ≈%.1f×10^11 m^2' % (method2_sa/1e11))


# As our best estimate for the global surface area of corals we use the geometric mean of the estimates from the two methods:

# In[9]:

best_sa = gmean([method1_sa,method2_sa])
print('Our best estimate of the global surface area of corals is ≈%.1f×10^11 m^2' % (best_sa/1e11))


# To convert the total surface area to biomass, we use estimates for the tissue biomass per unit surface area of corals from [Odum & Odum](http://dx.doi.org/10.2307/1943285):

# In[10]:

# Tissue biomass based on Odum & Odum [g C m^-2]
carbon_per_sa = 400

# Multiply our best estimate for the surface area of corals by the tissue biomass
coral_biomass = best_sa*carbon_per_sa

print('Our best estimate for the biomass of corals is ≈%.2f Gt C' %(coral_biomass/1e15))


# An important caveat of this analysis is that it doesn’t include contribution of corals outside coral reefs, like those located in seamounts. Nevertheless, we account for this biomass of corals which are out of formal coral reefs when calculating the total benthic biomass.
# 
# Our best estimate of the total biomass of cnidarians is the sum of the biomass of planktonic cnidarians and corals:

# In[11]:

best_estimate = planktonic_cnidarian_biomass + coral_biomass

print('Our best estimate for the biomass of cnidarians is ≈%.1f Gt C' %(best_estimate/1e15))


# # Estimating the total number of cnidarians
# To estimate the total number of cnidarians, we divide the total biomass of jellyfish by the characteristic carbon content of a single jellyfish. We do not consider corals as they are colonial organisms, and therefore it is hard to robustly define an individual. To estimate the characteristic carbon content of a single jellyfish, we rely on the data from Lucas et al.. We calculate the mean and median carbon content of all the species considered in the study, and use the geometric mean or the median and mean carbon contents as our best estimate of the characteristic carbon content of a single jellyfish.

# In[12]:

# Load data from Lucas et al.
data = pd.read_excel('carbon_content_data.xls', 'Biometric equations', skiprows=1)

# Calculate the median and mean carbon contents
median_cc = (data['mg C ind-1'].median()*1e-3)
mean_cc = (data['mg C ind-1'].mean()*1e-3)

# Calculate the geometric mean of the median and mean carbon contents
best_cc = gmean([median_cc,mean_cc])

# Calculate the total number of jellyfish
tot_cnidaria_num = planktonic_cnidarian_biomass/best_cc

print('Our best estimate for the total number of cnidarians is ≈%.1e.' %tot_cnidaria_num)


# In[13]:

# Feed results to the chordate biomass data
old_results = pd.read_excel('../animal_biomass_estimate.xlsx',index_col=0)
result = old_results.copy()
result.loc['Cnidarians',(['Biomass [Gt C]','Uncertainty'])] = (best_estimate/1e15,None)
result.to_excel('../animal_biomass_estimate.xlsx')

# Feed results to Table 1 & Fig. 1
update_results(sheet='Table1 & Fig1', 
               row=('Animals','Cnidarians'), 
               col=['Biomass [Gt C]', 'Uncertainty'],
               values=[best_estimate/1e15,None],
               path='../../results.xlsx')

# Feed results to Table S1
update_results(sheet='Table S1', 
               row=('Animals','Cnidarians'), 
               col='Number of individuals',
               values= tot_cnidaria_num,
               path='../../results.xlsx')

# We need to use the results on the biomass of gelatinous zooplankton 
# for our estimate of the total biomass of marine arthropods, so we 
# feed these results to the data used in the estimate of the total 
# biomass of marine arthropods
path = '../arthropods/marine_arthropods/marine_arthropods_data.xlsx'
marine_arthropods_data = pd.read_excel(path,'Other macrozooplankton')

marine_arthropods_data.loc[0] = pd.Series({
                'Parameter': 'Biomass of gelatinous zooplankton',
                'Value': planktonic_cnidarian_biomass,
                'Units': 'g C',
                'Uncertainty': None
                })
writer = pd.ExcelWriter(path, engine = 'openpyxl')
book = load_workbook(path)
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)


marine_arthropods_data.to_excel(writer, sheet_name = 'Other macrozooplankton',index=False)
writer.save()


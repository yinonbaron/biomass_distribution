
# coding: utf-8

# In[1]:

# Load dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean
import sys
sys.path.insert(0,'../../statistics_helper/')
from fraction_helper import *
from CI_helper import *
from excel_utils import *
pd.options.display.float_format = '{:,.1e}'.format


# # Estimating the biomass of marine fungi
# To estimate the total biomass of marine fungi, we consider different locations in which marine fungi might reside, and estimate the total biomass of fungi in each region. The main regions we consider are epipelagic and deep-sea planktonic fungi, and particle-attached fungi.
# 
# ## Epipelagic fungi
# To estimate the total biomass of epipelagic free-living fungi, we rely on studies using two independent methods: qPCR and direct counts of the concentration of fungi.
# 
# ### qPCR-based method
# Our qPCR-based estimate measured the ratio between DNA copy numbers for bacteria and fugni in the West Pacific Warm Pool ([Wang et al.](https://doi.org/10.1371/journal.pone.0101523)). Here is a sample of the data:

# In[2]:

qPCR_data = pd.read_excel('marine_fungi_data.xlsx','Wang',skiprows=1)
qPCR_data.head()


# We calculate the ratio of fungal DNA copy number to bacterial DNA copy number:

# In[3]:

# Calculate the total DNA copy number of fungi
fungal_DNA = qPCR_data['Basidiomycota [ng µl^-1]']+qPCR_data['Ascomycota [ng µl^-1]']

# Calculate the mean ratio of fungal DNA copy number and bacterial DNA copy number
qPCR_fungal_fraction = (fungal_DNA/qPCR_data['Bacteria [ng µl^-1]']).mean()

print('The ratio of fungal DNA copy number and bacterial DNA copy number is ≈%.0f' %(qPCR_fungal_fraction*100) + '%')


# ### Direct count method
# As an independent method for estimating the total biomass of marine fungi in the epipelagic layer, we use a study which measured the carbon concentration of fungi in the epipelagic layer in upwelling ecosystem off Chile using direct counts ([Gutiérrez et al.]( https://doi.org/10.1007/s00227-010-1552-z)). We calculate the average concentration of fungal carbon in relation to the carbon concentration of prokaryotes in the same site:

# In[4]:

# Load data on direct counts of fungal carbon concentration
direct_data = pd.read_excel('marine_fungi_data.xlsx','Gutiérrez',skiprows=1)

# Calculate the mean fungal carbon concentration
mean_fungal_conc = direct_data['Fungi carbon concentration [µg C L^-1]'].mean()

# Calculate the mean carbon concentration of prokaryotes
mean_prok_conc = direct_data['Prokaryote carbon concentration [µg C L^-1]'].mean()

direct_fungal_fraction = mean_fungal_conc/mean_prok_conc

print('The ratio of fungal carbon and bacterial carbon is ≈%.0f' %(direct_fungal_fraction*100) + '%')


# As our best estimate for the ratio of fungal and prokaryote carbon, we use the geometric mean of the ratios estimated based on qPCR and direct counts:

# In[5]:

best_fungal_fraction = gmean([qPCR_fungal_fraction,direct_fungal_fraction])
print('The ratio of fungal carbon and bacterial carbon is ≈%.0f' %(best_fungal_fraction*100) + '%')


# To estimate the total biomass of fungi using qPCR, we rely on our estimate from the total biomass of bacteria and archaea in the top 200 meters, which we estimate in the marine bacteria and archaea section:

# In[6]:

# Load total biomass of marine bacteria and archaea
marine_prok_biomass = pd.read_excel('../../bacteria_archaea/marine/marine_prok_biomass_estimate.xlsx')

# Load our estimate of the fraction of prokaryote biomass in the epipelagic layer
epi_frac = pd.read_excel('marine_fungi_data.xlsx','Bacteria biomass')

# Calculate the biomass of prokaryotes in the epipelagic realm
epi_prok_biomass = marine_prok_biomass.iloc[0:2,1].prod()*epi_frac['Value']*1e-15

print('Our estimate for the total biomass of bacteria and archaea in the epipelagic layer is ≈%.1f Gt C' %(epi_prok_biomass/1e15))


# We estimate the total biomass of fungi in the epipelagic layer by multiplying the total biomass of prokaryotes by the ratio of fungal and prokaryote biomass we calculated:

# In[7]:

best_epi_fungi = epi_prok_biomass*best_fungal_fraction

print('Our estimate for the total biomass of free-living epipelagic fungi based of qPCR is ≈%.2f Gt C' %(best_epi_fungi/1e15))


# ## Deep-sea fungi
# In the deep ocean, recent studies have quantified the contribution of fungi to the total 18S rDNA of microbial eukaryotes ([Pernice et al.](http://dx.doi.org/10.1038/ismej.2015.170)). Pernice et al. estimate ≈15% of the 18S rDNA sequences are fungal. The biomass concentration of deep-sea microbial eukaryotes was measured by [Pernice et al.](https://dx.doi.org/10.1038/ismej.2014.168). Here are the results of the measurements:

# In[8]:

pernice_data = pd.read_excel('marine_fungi_data.xlsx','Pernice',skiprows=1)
pernice_data


# We estimate the total biomass of microbial eukaryotes by multiplying the the measured biomass densities by the depth range of the measurements, and applying the concentrations to the total ≈3.6×10$^{14}\ m^2$ of ocean.

# In[9]:

depth_range = pernice_data['Max depth [m]']-pernice_data['Min depth [m]']

# Convert units: mL to m^3, pg C to g C
unit_conversion = 1e6*1e-12
ocean_area = 3.6e14

# Calculate the total biomass of deep-sea microbial eukaryotes
miceuk_biomass = (depth_range*pernice_data['Microbial eukaryotes biomass density [pg C mL^-1]']).sum()*unit_conversion*ocean_area

print('Our best estimate for the biomass of deep-sea microbial eukaryotes is ≈%.1f Gt C' %(miceuk_biomass/1e15))


# To estimate the biomass of deep-sea fungi, we multiply our estimate of the total biomass of deep-sea microbial eukaryotes with the estimate by Pernice et al. of the fraction of the 18S rDNA sequences of deep-sea microbial eukaryotes contributed by fungi:

# In[10]:

deep_sea_fungi = miceuk_biomass*0.15

print('Our estimate of the biomass of deep-sea fungi based on 18S rDNA sequencing is ≈%.2f Gt C' %(deep_sea_fungi/1e15))


# Pernice et al. were mainly focused on measuring the biomass of heterotrophic protists, and thus they might capture only unicellular fungi and not filamentous fungi. To take into account the possibility of  deep-sea filamentous fungi, we extend our estimate of the ratio between planktonic fungi and prokaryotes to the mesopelagic and bathypelagic realms.

# In[11]:

# Estimate the total biomass of prokaryotes in the mesopelagic and bathypelagic layers
meso_bathy_prok_biomass = marine_prok_biomass.iloc[0:2,1].prod()*1e-15*(1-epi_frac['Value'])

# Apply the ratio between fungal and prokaryote biomass to the mesopelagic and bathypelagic layers
meso_bathy_fungi = best_fungal_fraction*meso_bathy_prok_biomass

print('Our estimate of the biomass of deep-sea fungi based on the ratio between fungal and prokaryote biomass is ≈%.2f Gt C' %(meso_bathy_fungi/1e15))


# As our best estimate of the biomass of deep-sea planktonic fungi, we use the geometric mean of the two estimates based on 18S rDNA sequencing and the ratio between fungal and prokaryote biomass:

# In[12]:

best_deep_fungi = gmean([deep_sea_fungi,meso_bathy_fungi])
print('Our best estimate of the biomass of deep-sea fungi is ≈%.2f Gt C' %(best_deep_fungi/1e15))


# ## Particle-attached fungi
# To estimate the total biomass of particle-attached fungi, we rely on measurements of the biomass ratio between fungi and prokaryotes on marine particles in the bathypelagic layer ([Bochdansky et al.](http://dx.doi.org/10.1038/ismej.2016.113)). Bochdansky et al. use several different methods to estimate the biomass of fungi on particles, and provide a range of estimates for the ratio between the biomass of fungi and prokaryotes for each method. Here are the estimates provided in Bochdansky et al.:

# In[13]:

poc_fungi_biomass_data = pd.read_excel('marine_fungi_data.xlsx','Bochdansky',skiprows=1,index_col=0)
poc_fungi_biomass_data


# To estimate the ratio between the biomass of particle-attached fungi and prokaryotes in the bathypelagic layer, we first calculate the geometric mean of the range provided by Bochdansky et al. for each method:

# In[14]:

method_mean_fungi_ratio = poc_fungi_biomass_data.apply(gmean,axis=1)
method_mean_fungi_ratio


# As our best estimate of the ratio between the biomass of particle-attached fungi and prokaryotes in the bathypelagic layer, we use the geometric mean of the mean estimates from each method used in Bochdansky et al.:

# In[15]:

best_poc_fungi_ratio = gmean(method_mean_fungi_ratio)
print('Our best estimate of the ratio between the biomass of particle-attached fungi and prokaryotes in the bathypelagic layer is ≈%.1f' %best_poc_fungi_ratio)


# We could not find reliable data on the ratio between the biomass of particle-attached fungi and prokaryotes in shallower layers of the ocean, and thus we apply this ratio throughout all the layers of the ocean. We estimate the total biomass of particle-attached fungi in the ocean by using our estimate of the total biomass of particle-attached prokaryotes, and multiplying it by our best estimate for the ratio between the biomass of fungi and prokaryotes:

# In[16]:

# Use our estimate of the total biomass of particle-attached prokaryotes
poc_prok_biomass = marine_prok_biomass.iloc[[0,1,4],1].prod()*1e-15

# Calculate the total biomass of particle-attached fungi
poc_fungi_biomass = poc_prok_biomass*best_poc_fungi_ratio

print('Our best estimate of the total biomass of particle-attached fungi is ≈%.1f Gt C' %(poc_fungi_biomass/1e15))


# Our best estimate of the total biomass of marine fungi is a sum of our estimates for the biomass of epipelagic planktonic fungi, deep-sea planktonic fungi and particle-attached fungi:

# In[17]:

best_estimate = poc_fungi_biomass + best_epi_fungi + best_deep_fungi
print('Our best estimate of the total biomass of marine fungi is ≈%.1f Gt C' %(best_estimate/1e15))


# # Uncertainty analysis
# The available data on the biomass of marine fungi is scarce, and thus we chose to use a crude estimate of an order of magnitude as our projection for the uncertainty associated with the estimate of the total biomass of marine fungi. Our final parameters are

# In[18]:

mul_CI = 10


print('Biomass of marine fungi: %.1f Gt C' %(best_estimate/1e15))
print('Uncertainty associated with the estimate of the total biomass of marine fungi ≈%.0f-fold' % mul_CI)

old_results = pd.read_excel('../fungi_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[2] = pd.Series({
                'Parameter': 'Biomass of marine fungi',
                'Value': float(best_estimate),
                'Units': 'Gt C',
                'Uncertainty': "{0:.1f}".format(mul_CI)
                })

result.to_excel('../fungi_biomass_estimate.xlsx',index=False)


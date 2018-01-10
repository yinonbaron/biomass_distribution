
# coding: utf-8

# # Estimating the fraction of archaea out of the total soil prokaryote population
# In order to estimate the fraction of archaea out of the total population of soil bacteria and archaea, we rely of four independent methods: fluorescent in-situ hybridization (FISH), CARD-FISH and 16S rDNA sequencing and 16S rDNA qPCR.
# 
# ## FISH-based estimate
# In order to estimate the fraction of archaea out of the total biomass of soil bacteria and archae, we collected data from several studies. Here is a sample of the data:

# In[1]:

# Load dependencies
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '../../statistics_helper/')
from fraction_helper import *
from CI_helper import *


# Load FISH data
FISH_data = pd.read_excel('soil_bac_arch_data.xlsx','FISH')
FISH_data.head()


# We Calculate the geometric mean of the fractions for each study in each habitat to generate characteristic values for each study:

# In[2]:

FISH_study_mean = FISH_data.groupby(['Habitat','DOI'])['Fraction of archaea'].apply(frac_mean)


# We then calculate the geometric mean between different studies in the same habitat to generate characteristic values for each habitat:

# In[3]:

FISH_habitat_mean = FISH_study_mean.groupby('Habitat').apply(frac_mean)


# Finally, we calculate the geometric mean between the characteristic values in each habitat as our best estimate of the fraction of archaea out of the total biomass of soil bacteria and archaea based on FISH:

# In[4]:

FISH_mean = frac_mean(FISH_habitat_mean)

print('Our best estimate of the fraction of archaea out of the total biomass of soil bacteria and archaea based on FISH is ≈%.0f percent' %(FISH_mean*100))


# ## CARD-FISH-based estimate
# In order to estimate the fraction of archaea out of the total biomass of soil bacteria and archae, we collected data from several studies. Here is a sample of the data:

# In[5]:

# Load CARD-FISH data
CARDFISH_data = pd.read_excel('soil_bac_arch_data.xlsx','CARD-FISH')
CARDFISH_data.head()


# We Calculate the geometric mean of the fractions for each study in each habitat to generate characteristic values for each study:

# In[6]:

CARDFISH_study_mean = CARDFISH_data.groupby('DOI')['Fraction of archaea'].apply(frac_mean)


# Finally, we calculate the geometric mean between the characteristic values in each study as our best estimate of the fraction of archaea out of the total biomass of soil bacteria and archaea based on CARD-FISH:

# In[7]:

CARDFISH_mean = frac_mean(CARDFISH_study_mean)
print('Our best estimate of the fraction of archaea out of the total biomass of soil bacteria and archaea based on CARD-FISH is ≈%.0f percent' %(CARDFISH_mean*100))


# ## 16S rDNA sequencing-based estimate
# For our 16S rDNA sequencing-based estimate, we rely on a study which reported values for the fraction of archaea out of the total population of soil bacteria and archaea in 146 soils from across the globe ([Bates et al.](http://dx.doi.org/10.1038/ismej.2010.171)). We calculate the geometric mean of values within each biome, and then calculate the geometric mean of the characteristic values of each biome. We account for the lower rRNA operon copy number in archaea ([Sun et al.](http://dx.doi.org/10.1128/AEM.01282-13)) by multiplying the measured fractions by a factor of 2. 

# In[8]:

# 16S sequencing data from Bates et al. corrected for lower operon copy number
bates_data = pd.read_excel('soil_bac_arch_data.xlsx','bates',skiprows=1)

# Calculate the average fraction of archaea out of the total biomass of soil bacteria and archaea
# Correct for the lower rDNA operon content in archaea
seq = frac_mean(bates_data.groupby('Biome')['Fraction of archaea'].apply(frac_mean))*2


# ## 16S rDNA qPCR-based estimate
# For our 16S qPCR-based estimate, we rely on a recent study which reported the fraction of archaea out of the total population of soil bacteria and archaea in grasslands, forests and croplands in Korea ([Hong & Cho](http://dx.doi.org/10.1371/journal.pone.0133763)). The mean fraction of archaea reported by Hong & Cho is ≈3%.

# In[9]:

# qPCR data from Hong & Cho
qpcr = 0.027


# We use the geomtric mean of our estimates from the four different methods as our best estimate of the fraction of archaea out of the total biomass of soil bacteria and archaea

# In[10]:

best_frac = frac_mean(np.array([seq,qpcr,FISH_mean,CARDFISH_mean]))

print('Our best estimate for the fraction of archaea out of the total biomass of soil bacteria and archaea is ≈%.0f percent' %(best_frac*100))


# We multiply the fraction of archaea out of the total biomass of soil bacteria and archaea by our estimate for the total biomass of soil bacteria and archaea to estimate the total biomass of soil archaea:

# In[11]:

# Load fungi biomass estimate
fungi_biomass_estimate = pd.read_excel('../../fungi/fungi_biomass_estimate.xlsx')

# Calculate the total biomass of soil bactria and archaea
soil_prok_biomass = fungi_biomass_estimate['Value'][0]*(1-fungi_biomass_estimate['Value'][1])

# Calculate the total biomass of soil archaea
best_soil_arch_biomass = soil_prok_biomass*best_frac

# Calculate the total biomass of soil bacteria
best_soil_bac_biomass = soil_prok_biomass*(1-best_frac)

print('Our best estimate for the total biomass of soil archaea is ≈%.1f Gt C' %(best_soil_arch_biomass/1e15))
print('Our best estimate for the total biomass of soil bacteria is ≈%.1f Gt C' %(best_soil_bac_biomass/1e15))


# # Uncertainty analysis
# We collect uncertainties associated with our estimate of the fraction of archaea out of the total biomass of soil bacteria and archae at different levels - intra-study uncertainty, inter-study uncertainty, inter-habitat uncertainty, and inter-method uncertainty. We use the heighest uncertainty out of this collection as our best projection for the uncertainty associated with our estimate of the fraction of archaea out of the total biomass of soil bacteria and archaea

# ## Intra-study uncertainty
# We calculate the 95% confidence interval of the geometric mean of values within each study. The cases in which we have multiply measurements within the same study are FISH, CARD-FISH and 16S rDNA sequencing. For 16S rDNA qPCR we rely on the standard deviation reported in Hong & Cho.
# ### FISH
# We calculate the 95% confidence interval of the geometric mean of values within each study. We use the maximal uncertainty as our best projection of the intra-study uncertainty of studies using FISH:

# In[12]:

FISH_intra_arch_CI = FISH_data.groupby(['Habitat','DOI'])['Fraction of archaea'].apply(frac_CI)
FISH_data['Fraction of bacteria'] = 1 - FISH_data['Fraction of archaea']
FISH_intra_bac_CI = FISH_data.groupby(['Habitat','DOI'])['Fraction of bacteria'].apply(frac_CI)
print('Our best projection of the intra-study uncertainty associated with the fraction of archaea out of the total biomass of bacteria and archaea based on FISH is ≈%.1f-fold.' %FISH_intra_arch_CI.max())
print('Our best projection of the intra-study uncertainty associated with the fraction of bacteria out of the total biomass of bacteria and archaea based on FISH is ≈%.1f-fold.' %FISH_intra_bac_CI.max())


# ### CARD-FISH
# We calculate the 95% confidence interval of the geometric mean of values within each study. We use the maximal uncertainty as our best projection of the intra-study uncertainty of studies using CARD-FISH:

# In[13]:

CARDFISH_data['Fraction of bacteria'] = 1 - CARDFISH_data['Fraction of archaea']
CARDFISH_intra_arch_CI = CARDFISH_data.groupby('DOI')['Fraction of archaea'].apply(frac_CI)
CARDFISH_intra_bac_CI = CARDFISH_data.groupby('DOI')['Fraction of bacteria'].apply(frac_CI)
print('Our best projection of the intra-study uncertainty associated with the fraction of archaea out of the total biomass of bacteria and archaea based on CARD-FISH is ≈%.1f-fold.' %CARDFISH_intra_arch_CI.max())
print('Our best projection of the intra-study uncertainty associated with the fraction of bacteria out of the total biomass of bacteria and archaea based on CARD-FISH is ≈%.1f-fold.' %CARDFISH_intra_bac_CI.max())


# ### 16S rDNA sequencing
# We calculate the 95% confidence interval of the geometric mean of values reported in Bates et al.:

# In[14]:

bates_data['Fraction of bacteria'] = 1 - bates_data['Fraction of archaea']
seq_intra_arch_CI = frac_CI(bates_data['Fraction of archaea'])
seq_intra_bac_CI = frac_CI(bates_data['Fraction of bacteria'])
print('Our best projection of the intra-study uncertainty associated with the fraction of archaea out of the total biomass of bacteria and archaea based on 16S rDNA sequencing is ≈%.1f-fold.' %seq_intra_arch_CI)
print('Our best projection of the intra-study uncertainty associated with the fraction of bacteria out of the total biomass of bacteria and archaea based on 16S rDNA sequencing is ≈%.3f-fold.' %seq_intra_bac_CI)


# ### 16S rDNA qPCR
# We rely on the standard deviation reported in Hong & Cho of 1.5%. We use 1.96 stantard deviations as our best projection of the intra-study uncertainty associated with the fraction of archaea out of the total biomass of soil bacteria and archaea:

# In[15]:

# Calculate the multiplicative error using 1.96 standard deviations to approximate 95%
# confidence interval
qpcr_intra_arch_CI = (qpcr+1.96*0.015)/qpcr
qpcr_intra_bac_CI = ((1-qpcr)+1.96*0.015)/(1-qpcr)
print('Our best projection of the intra-study uncertainty associated with the fraction of archaea out of the total biomass of bacteria and archaea based on 16S rDNA qPCR is ≈%.1f-fold.' %qpcr_intra_arch_CI)
print('Our best projection of the intra-study uncertainty associated with the fraction of bacteria out of the total biomass of bacteria and archaea based on 16S rDNA qPCR is ≈%.2f-fold.' %qpcr_intra_bac_CI)


# ## Inter-study uncertainty
# For our FISH and CARD-FISH-based estimates, we rely in several studies. We calculate the 95% confidence interval around the geometric mean of the values from different studies within the same habitat as our best projection of the inter-study uncertainty associates with the fraction of archaea out of the total biomass of soil bacteria and archaea.

# In[16]:

FISH_interstudy_arch_CI = FISH_study_mean.groupby('Habitat').apply(frac_CI)
FISH_interstudy_bac_CI = (1-FISH_study_mean).groupby('Habitat').apply(frac_CI)

print('Our best projection of the inter-study uncertainty associated with the fraction of archaea out of the total biomass of bacteria and archaea based on FISH is ≈%.1f-fold.' %FISH_interstudy_arch_CI.max())
print('Our best projection of the inter-study uncertainty associated with the fraction of bacteria out of the total biomass of bacteria and archaea based on FISH is ≈%.1f-fold.' %FISH_interstudy_bac_CI.max())

CARDFISH_interstudy_arch_CI = frac_CI(CARDFISH_study_mean)
CARDFISH_interstudy_bac_CI = frac_CI(1-CARDFISH_study_mean)

print('Our best projection of the inter-study uncertainty associated with the fraction of archaea out of the total biomass of bacteria and archaea based on CARD-FISH is ≈%.1f-fold.' %CARDFISH_interstudy_arch_CI.max())
print('Our best projection of the inter-study uncertainty associated with the fraction of bacteria out of the total biomass of bacteria and archaea based on CARD-FISH is ≈%.1f-fold.' %CARDFISH_interstudy_bac_CI.max())


# ## Inter-habitat uncertainty
# For the FISH-based estimate, we also rely on characteristic values in different habitats to estimate the fraction of archaea of of the total biomass of soil bacteria and archaea. We calculate the 95% confidence interval around the geometric mean of the characteristic values from different habitats as a measure of the inter-habitat uncertainty associated with our estimate of the fraction of archaea out of the total biomass of soil bacteria and archaea. 

# In[17]:

FISH_inter_habitat_arch_CI = frac_CI(FISH_habitat_mean)
FISH_inter_habitat_bac_CI = frac_CI(1-FISH_habitat_mean)

print('Our best projection of the inter-habitat uncertainty associated with the fraction of archaea out of the total biomass of bacteria and archaea based on FISH is ≈%.1f-fold.' %FISH_inter_habitat_arch_CI)
print('Our best projection of the inter-habitat uncertainty associated with the fraction of bacteria out of the total biomass of bacteria and archaea based on FISH is ≈%.1f-fold.' %FISH_inter_habitat_bac_CI)


# ## Inter-method uncertainty
# We calculate the 95% confidence interval around the geometric mean of the estimates from the four different values as our best projection of the 

# In[18]:

inter_arch_CI = frac_CI(np.array([seq,qpcr,FISH_mean,CARDFISH_mean]))
inter_bac_CI = frac_CI(1-np.array([seq,qpcr,FISH_mean,CARDFISH_mean]))
print('Our best projection of the inter-method uncertainty associated with the fraction of archaea out of the total biomass of bacteria and archaea is ≈%.1f-fold.' %inter_arch_CI)
print('Our best projection of the inter-method uncertainty associated with the fraction of bacteria out of the total biomass of bacteria and archaea is ≈%.1f-fold.' %inter_bac_CI)


# We use the maximal uncertainty out of the collection of uncertainties calculated abouce as our best projection of the uncertainty associated with the estimate of the fraction of archaea out of the total biomass of soil bacteria and archaea.

# In[19]:


arch_frac_mul_CI = np.max([FISH_intra_arch_CI.max(),CARDFISH_intra_arch_CI.max(),seq_intra_arch_CI,qpcr_intra_arch_CI,FISH_interstudy_arch_CI.max(),CARDFISH_interstudy_arch_CI.max(),FISH_inter_habitat_arch_CI,inter_arch_CI])
bac_frac_mul_CI = np.max([FISH_intra_bac_CI.max(),CARDFISH_intra_bac_CI.max(),seq_intra_bac_CI,qpcr_intra_bac_CI,FISH_interstudy_bac_CI.max(),CARDFISH_interstudy_bac_CI.max(),FISH_inter_habitat_bac_CI,inter_bac_CI])

print('Our best projection of the uncertainty associated with the fraction of archaea out of the total biomass of bacteria and archaea is ≈%.1f-fold.' %arch_frac_mul_CI)
print('Our best projection of the uncertainty associated with the fraction of bacteria out of the total biomass of bacteria and archaea is ≈%.1f-fold.' %bac_frac_mul_CI)


# We combine the uncertainty associated with the fraction of archaea out of the total biomass of soil bacteria and archaea with the uncertainty of the total biomass of soil bacteria and archaea as our best projection of the uncertainty associated with the our estimate of the total biomass of soil archaea.

# In[20]:

# Our best projection for the uncertainty associated with the total biomass of soil bacteria and archaea
soil_prok_CI = CI_prod_prop(np.array([fungi_biomass_estimate['Uncertainty'][0],fungi_biomass_estimate['Uncertainty'][1]]))

# Combine the uncertainty of the total biomass of soil prokaryotes with the uncertainty
# of the fraction of archaea out of the total biomass of soil prokaryotes
arch_mul_CI = CI_prod_prop(np.array([bac_frac_mul_CI,soil_prok_CI]))
bac_mul_CI = CI_prod_prop(np.array([arch_frac_mul_CI,soil_prok_CI]))

print('Our best projection of the uncertainty associated with our estimate of the biomass of soil archaea is ≈%.1f-fold.' %arch_mul_CI)
print('Our best projection of the uncertainty associated with our estimate of the biomass of soil bacteria is ≈%.1f-fold.' %bac_mul_CI)


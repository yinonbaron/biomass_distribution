
# coding: utf-8

# In[1]:

# Load dependencies
import pandas as pd
import numpy as np
import gdal
from scipy.stats import gmean
import sys
sys.path.insert(0,'../../statistics_helper/')
from fraction_helper import *
from CI_helper import *
from excel_utils import *
pd.options.display.float_format = '{:,.1e}'.format


# # Estimating the total biomass of terrestrial protists
# After searching the literature, we could not find a comprehensive account of the biomass of protists in soils. We generated a crude estimate of the total biomass of protists in soil based on estimating the total number of individual protists in the soil, and on the characteristic carbon content of a single protist.
# 
# In order to calculate the total biomass of soil protists we calculate a characteristic number of individual protists for each one of the morphological groups of protists (flagellates, ciliates, and naked and testate ameobae). We combine these estimates with estimates for the carbon content of each morphological group.
# 
# ## Number of protists
# To estimate the total number of protists, we assembled data on the number of protists in soils which contains 160 measurements from 42 independent studies. Here is a sample of the data:

# In[2]:

# Load data
data = pd.read_excel('terrestrial_protist_data.xlsx','Density of Individuals')
data.head()


# To estimate the total number of protists, we group our samples to different habitats and to the study in which they were taken. We calculate the characteristic number of each of the groups of protists per gram of soil. To do this we first derive a representative value for each study in case there was more than one measurement done in it. We calculate the representative value for each study in each habitat. Then we calculate the average of different representative values from different studies within the same habitat. We calculate the averages either by using the arithmetic mean or the geometric mean.

# In[3]:

# Define the function to calculate the geometric mean of number of each group of protists per gram
def groupby_gmean(input):
    return pd.DataFrame({'Number of ciliates [# g^-1]': gmean(input['Number of ciliates [# g^-1]'].dropna()),
                        'Number of naked amoebae [# g^-1]': gmean(input['Number of naked amoebae [# g^-1]'].dropna()),
                        'Number of testate amoebae [# g^-1]': gmean(input['Number of testate amoebae [# g^-1]'].dropna()),
                        'Number of flagellates [# g^-1]': gmean(input['Number of flagellates [# g^-1]'].dropna())},index=[0])

# Define the function to calculate the arithmetic mean of number of each group of protists per gram
def groupby_mean(input):
    return pd.DataFrame({'Number of ciliates [# g^-1]': np.nanmean(input['Number of ciliates [# g^-1]'].dropna()),
                        'Number of naked amoebae [# g^-1]': np.nanmean(input['Number of naked amoebae [# g^-1]'].dropna()),
                        'Number of testate amoebae [# g^-1]': np.nanmean(input['Number of testate amoebae [# g^-1]'].dropna()),
                        'Number of flagellates [# g^-1]': np.nanmean(input['Number of flagellates [# g^-1]'].dropna())},index=[0])

# Group the samples by habitat and study, and calculate the geometric mean
grouped_data_gmean = data.groupby(['Habitat','DOI']).apply(groupby_gmean)

# Group the samples by habitat and study, and calculate the arithmetic mean
grouped_data_mean = data.groupby(['Habitat','DOI']).apply(groupby_mean)

# Group the representative values by habitat, and calculate the geometric mean
habitat_gmean = grouped_data_gmean.groupby('Habitat').apply(groupby_gmean)

# Group the representative values by habitat, and calculate the arithmetic mean
habitat_mean = grouped_data_mean.groupby('Habitat').apply(groupby_mean)

habitat_gmean.set_index(habitat_gmean.index.droplevel(1),inplace=True)
habitat_mean.set_index(habitat_mean.index.droplevel(1),inplace=True)


# Here is the calculated geometric mean number of cells per gram for each habitat and each group of protists:

# In[4]:

habitat_gmean


# For some groups, not all habitats have values. We fill values for missing data by the following scheme. For missing values in the boreal forest biome, we use values from the temperate forest biome. If we have data for the group of protists from the "General" habitat, which is based on expert assessment of the characteristic number of individuals for that group per gram of soil, we fill the missing values with the value for the "General" habitat.
# 
# The only other missing data was for ciliates in tropical forests and tundra. For tropical forest, we used the values from temperate forests. For tundra, we use the mean over all the different habitats to fill the value:

# In[5]:

# Fill missing values for boreal forests
habitat_mean.loc['Boreal Forest',['Number of ciliates [# g^-1]','Number of flagellates [# g^-1]','Number of naked amoebae [# g^-1]']] = habitat_mean.loc['Temperate Forest',['Number of ciliates [# g^-1]','Number of flagellates [# g^-1]','Number of naked amoebae [# g^-1]']]
habitat_gmean.loc['Boreal Forest',['Number of ciliates [# g^-1]','Number of flagellates [# g^-1]','Number of naked amoebae [# g^-1]']] = habitat_gmean.loc['Temperate Forest',['Number of ciliates [# g^-1]','Number of flagellates [# g^-1]','Number of naked amoebae [# g^-1]']]

# Fill missing values for naked amoebae
habitat_mean.loc[['Shrubland','Tropical Forest','Tundra','Woodland'],'Number of naked amoebae [# g^-1]'] = habitat_mean.loc['General','Number of naked amoebae [# g^-1]']
habitat_gmean.loc[['Shrubland','Tropical Forest','Tundra','Woodland'],'Number of naked amoebae [# g^-1]'] = habitat_gmean.loc['General','Number of naked amoebae [# g^-1]']

# Fill missing values for flagellates
habitat_gmean.loc[['Desert','Grassland','Shrubland','Tropical Forest','Woodland'],'Number of flagellates [# g^-1]'] = habitat_gmean.loc['General','Number of flagellates [# g^-1]']
habitat_mean.loc[['Desert','Grassland','Shrubland','Tropical Forest','Woodland'],'Number of flagellates [# g^-1]'] = habitat_mean.loc['General','Number of flagellates [# g^-1]']

# Fill missing values for ciliates
habitat_gmean.loc['Tropical Forest','Number of ciliates [# g^-1]'] = habitat_gmean.loc['Temperate Forest','Number of ciliates [# g^-1]']
habitat_mean.loc['Tropical Forest','Number of ciliates [# g^-1]'] = habitat_mean.loc['Temperate Forest','Number of ciliates [# g^-1]']
habitat_gmean.loc['Tundra','Number of ciliates [# g^-1]'] = gmean(habitat_mean['Number of ciliates [# g^-1]'].dropna())
habitat_mean.loc['Tundra','Number of ciliates [# g^-1]'] = habitat_mean['Number of ciliates [# g^-1]'].dropna().mean()
habitat_gmean


# We have estimates for the total number of individual protists per gram of soil. In order to calculate the total number of individual protists we need to first convert the data to number of individuals per $m^2$. To convert number of individuals per gram of soil to number of individuals per $m^2$, we calculate a global average soil density in the top 15 cm based on [Hengl et al.](https://dx.doi.org/10.1371%2Fjournal.pone.0105992).
# 

# In[6]:

# Load soil density map from Hengl et al. (in the top 15 cm, reduced in resolution to 1 degree resolution)
gtif = gdal.Open('bulk_density_data.tif')
bulk_density_map = np.array(gtif.GetRasterBand(1).ReadAsArray())

# Fill missing values with NaN
bulk_density_map[bulk_density_map == bulk_density_map[0,1]] = np.nan
# Mean soil bulk density from Hengl et al. [in g per m^3]
bulk_density = np.nanmean(bulk_density_map[:])*1000
print('Our best estimate for the global mean bulk density of soil in the top 15 cm is ≈%.1e g m^3' %bulk_density)


# Measuring the density of individuals per gram of soil does not take into account the distribution on biomass along the soil profile. Most of the measurements of the number of individual protists per gram of soil are done in shallow soil depths. We calculate the average sampling depth across studies:

# In[7]:

# Calculate the average sampling depth 
sampling_depth = data.groupby('DOI').mean().mean()['Sampling Depth [cm]']

print('The average sampling depth of soil protists is ≈%.0f cm' %sampling_depth)


# It is not obvious what is the fraction of the total biomass of soil protists that is found in the top 8 cm of soil. To estimate the fraction of the biomass of soil protists found in the top 8 cm, we rely on two methodologies. The first is based on the distribution of microbial biomass with depth as discussed in Xu et al. Xu et al. extrapolate the microbial biomass across the soil profile based on empirical equations for the distribution of root biomass along soil depth from [Jackson et al.](http://dx.doi.org/10.1007/BF00333714). The empirical equations are biome-specific, and follow the general form: $$Y = 1-\beta^d$$ Where Y is the cumulative fraction of roots, d is depth in centimeters, and $\beta$ is a coefficient fitted for each biome. On a global scale, the best fit for $\beta$ as reported in Jackson et al., is ≈0.966. We use this coefficient to calculate the fraction of total biomass of soil protists found in the top 8 cm: 

# In[8]:

# The beta coefficient from Jackson et al.
jackson_beta = 0.966

# Calculate the fraction of the biomass of soil protists found in the top 8 cm
jackson_fraction = 1 - jackson_beta** sampling_depth

print('Our estimate for the fraction of biomass of soil protists found in soil layers sampled, based on Jackson et al. is ≈%.0f percent' %(jackson_fraction*100))


# As a second estimate for the fraction of the total biomass of soil protists found in the top 8 cm, we rely on an empirical equation from [Fierer et al.](http://dx.doi.org/10.1111/j.1461-0248.2009.01360.x), which estimates the  fraction microbial biomass found below sampling depth d:
# $$ f = [-0.132×ln(d) + 0.605]×B$$
# Where f is the fraction microbial biomass found below sampling depth d (in cm). We use this equation to calculate the fraction of the total biomass of soil protists found in the top 8 cm:
# 

# In[9]:

# The fraction of microbial biomass found in layer shallower than depth x based on Fierer et al.
fierer_eq = lambda x: 1-(-0.132*np.log(x)+0.605)
fierer_frac = fierer_eq(sampling_depth)
print('Our estimate for the fraction of biomass of soil protists found in soil layers sampled, based on Fierer et al. is ≈%.0f percent' %(fierer_frac*100))


# As our best estimate for the fraction of the total biomass of soil protists found in layers shallower than 8 cm, we use the geometric mean of the estimates based on Jackson et al. and Fierer et al.:

# In[10]:

best_depth_frac = frac_mean(np.array([jackson_fraction,fierer_frac]))
print('Our best estimate for the fraction of biomass of soil protists found in soil layers sampled is ≈%.0f percent' %(best_depth_frac*100))


# To convert the measurements per gram of soil to number of individuals per $m^2$, we calculate the average sampling depth across studies. We calculate the volume of soil held within this sampling depth. We use the bulk density to calculate the total weight of soil within one $m^2$ of soil with depth equal to the sampling depth. We multiply the estimates per gram of soil by the total weight of soil per $m^2$. To account for biomass present in lower layers, we divide the total number of individual protists per $m^2$ by our best estimate for the fraction of the total biomass of soil protists found in layer shallower than 8 cm.

# In[11]:

# convert number of individuals per gram soil to number of individuals per m^2
habitat_per_m2_gmean = (habitat_gmean*bulk_density*sampling_depth/100/best_depth_frac)
habitat_per_m2_mean = (habitat_mean*bulk_density*sampling_depth/100/best_depth_frac)


# To calculate the total number of protists we multiply the total number of individuals per unit area of each type of protist in each habitat by the total area of each habitat taken from the book [Biogeochemistry: An analysis of Global Change](https://www.sciencedirect.com/science/book/9780123858740) by Schlesinger & Bernhardt. The areas of each habitat are:

# In[12]:

habitat_area = pd.read_excel('terrestrial_protist_data.xlsx','Biome area', skiprows=1,index_col=0)
habitat_area


# One habitat for which we do not have data is the savanna. We use the mean of the values for the tropical forest, woodland, shrubland and grassland as an estimate of the total biomass in the savanna.

# In[13]:

habitat_per_m2_gmean.loc['Tropical Savanna'] = gmean(habitat_per_m2_gmean.loc[['Tropical Forest','Woodland','Shrubland','Grassland']])
habitat_per_m2_mean.loc['Tropical Savanna'] = habitat_per_m2_mean.loc[['Tropical Forest','Woodland','Shrubland','Grassland']].mean(axis=0)

tot_num_gmean = habitat_per_m2_gmean.mul(habitat_area['Area [m^2]'],axis=0)
tot_num_mean = habitat_per_m2_mean.mul(habitat_area['Area [m^2]'],axis=0)


# We generated two types of estimates for the total number of soil protists: an estimate which uses the arithmetic mean of the number of individuals at each habitat, and an estimate which uses the geometric mean of the number of individuals at each habitat. The estimate based on the arithmetic mean is more susceptible to sampling bias, as even a single measurement which is not characteristic of the global population (such as samples which are contaminated with organic carbon sources, or samples which have some technical biases associated with them) might shift the average concentration significantly. On the other hand, the estimate based on the geometric mean might underestimate global biomass as it will reduce the effect of biologically relevant high biomass concentrations. As a compromise between these two caveats, we chose to use as our best estimate the geometric mean of the estimates from the two methodologies.

# In[14]:

tot_num_protist = gmean([tot_num_mean.sum(),tot_num_gmean.sum()])


# ## Carbon content of protists
# We estimate the characteristic carbon content of a single protist from each of the morphological groups of protists  based on data from several sources. Here is a sample of the data:

# In[15]:

cc_data =  pd.read_excel('terrestrial_protist_data.xlsx', 'Carbon content')
cc_data.head()


# We combine this data with an additional source from [Finlay & Fenchel](http://dx.doi.org/10.1078/1434-4610-00060). We calculate the average cell length for each group. 

# In[16]:

# Load data from Finlay & Fenchel
ff_data = pd.read_excel('terrestrial_protist_data.xlsx', 'Finlay & Fenchel', skiprows=1)

# Define the function to calculate the weighted average for each group of protists
def weighted_av_groupby(input):
    return np.average(input['Length [µm]'],weights=input['Abundance [# g^-1]'])

cell_lengths = ff_data.groupby('Protist type').apply(weighted_av_groupby)


# We convert the cell length to biovolume according the the allometric relation decribed in Figure 10 of Finlay & Fenchel. The relation between cell volume and cell length is given by the equation: 
# $$V = 0.6×L^{2.36}$$
# Where V is the cell volume in $µm^3$ and L is the cell length in µm.

# In[17]:

cell_volumes = 0.6*cell_lengths**2.36
cell_volumes


# We convert cell volumes to carbon content assuming ≈150 fg C µm$^3$:

# In[18]:

ff_carbon_content = cell_volumes*150e-15
pd.options.display.float_format = '{:,.1e}'.format
ff_carbon_content


# We add these numbers as an additional source for calculating the carbon content of protists:

# In[19]:

cc_data.loc[cc_data.index[-1]+1] = pd.Series({'Reference': 'Finlay & Fenchel',
                   'DOI': 'http://dx.doi.org/10.1078/1434-4610-00060',
                   'Carbon content of ciliates [g C cell^-1]': ff_carbon_content.loc['Ciliate'],
                   'Carbon content of naked amoebae [g C cell^-1]': ff_carbon_content.loc['Naked amoebae'],
                   'Carbon content of testate amoebae [g C cell^-1]': ff_carbon_content.loc['Testate amoebae'],
                   'Carbon content of flagellates [g C cell^-1]': ff_carbon_content.loc['Flagellate']
                  })


# We calculate the geometric mean of carbon contents for first for values within each study and then for the average values between studies:

# In[20]:

def groupby_gmean(input):
    return pd.DataFrame({'Carbon content of ciliates [g C cell^-1]': gmean(input['Carbon content of ciliates [g C cell^-1]'].dropna()),
                        'Carbon content of naked amoebae [g C cell^-1]': gmean(input['Carbon content of naked amoebae [g C cell^-1]'].dropna()),
                        'Carbon content of testate amoebae [g C cell^-1]': gmean(input['Carbon content of testate amoebae [g C cell^-1]'].dropna()),
                        'Carbon content of flagellates [g C cell^-1]': gmean(input['Carbon content of flagellates [g C cell^-1]'].dropna())},index=[0])


study_mean_cc = cc_data.groupby('DOI').apply(groupby_gmean)
mean_cc = study_mean_cc.reset_index().groupby('level_1').apply(groupby_gmean)


# In[21]:

gmean(study_mean_cc['Carbon content of flagellates [g C cell^-1]'].dropna())
mean_cc.T


# To estimate the total biomass of soil protists based on the total number of individuals and their carbon content, we multiply our estimate for the total number of individuals for each morphological type by its characteristic carbon content. We sum over all morophological types of protists to generate our best estimate for the global biomass of soil protists

# In[22]:

# Calculate the total biomass of protists
best_estimate = (tot_num_protist*mean_cc).sum(axis=1)

print('Our best estimate of the total biomass of soil protists is ≈%.1f Gt C' %(best_estimate/1e15))


# # Uncertainty analysis
# To assess the uncertainty associated with our estimate of the total biomass of terrestrial protists, we collect available uncertainties for the values reported within studies and between studies. We use the highest uncertainty out of this collection of uncertainties as our best projection for the uncertainty associated we the estimate of the total biomass of terrestrial protists.
# 
# ## Number of individuals
# We assemble different measures of uncertainty at different levels - for values within the same study, for studies within the same habitat, and between habitats.
# 
# ### Intra-study uncertainty
# For each study which reports more than one value, we calculate 95% confidence interval around the geometric mean of those values. We take the maximal uncertainty in each habitat as our measure of the intra-study uncertainty

# In[23]:

pd.options.display.float_format = '{:,.1f}'.format

# Define the function ot calculate the 95% confidence interval around the
# geometric mean of number of each group of protists per gram
def groupby_geo_CI(input):
    return pd.DataFrame({'Number of ciliates [# g^-1]': geo_CI_calc(input['Number of ciliates [# g^-1]'].dropna()),
                        'Number of naked amoebae [# g^-1]': geo_CI_calc(input['Number of naked amoebae [# g^-1]'].dropna()),
                        'Number of testate amoebae [# g^-1]': geo_CI_calc(input['Number of testate amoebae [# g^-1]'].dropna()),
                        'Number of flagellates [# g^-1]': geo_CI_calc(input['Number of flagellates [# g^-1]'].dropna())},index=[0])

# Group the samples by habitat and study, and calculate the 95% confidence
# interval around the geometric mean of values within each study
intra_study_num_CI = data.groupby(['Habitat','DOI']).apply(groupby_geo_CI)

# Use the maximal uncertainty in each habitat as a measure of the intra-study uncertainty
intra_num_CI = intra_study_num_CI.groupby('Habitat').max()


# ### Interstudy uncertainty
# We calculate 95% confidence interval around the geometric mean of the average values from different studies.

# In[24]:

# Group the representative values by habitat, and calculate the 95% confidence interval
# around the geometric mean of values within habitat
inter_study_habitat_num_CI = grouped_data_gmean.groupby('Habitat').apply(groupby_geo_CI)
inter_study_habitat_num_CI.set_index(inter_study_habitat_num_CI.index.droplevel(level=1),inplace=True)
inter_study_habitat_num_CI


# ### Inter-habitat uncertainty
# We first use the maximum of the intra-study and interstudy uncertainty in each habitat as our best projection for the uncertainty associated with the estimate of the total number of protists in the habitat. For habitats with missing uncertainty projections, we use the geometric mean of the uncertainties for the same group of protists in other habitats.

# In[25]:

# Use the maximum of the intra-study and interstudy uncertainty as our best projection of the uncertainty 
# of the number of protists in each habitat
tot_num_habitat_CI = inter_study_habitat_num_CI.where(inter_study_habitat_num_CI > intra_num_CI, intra_num_CI).fillna(inter_study_habitat_num_CI)

# Fill missing values for each habitat with the geometric mean of the uncertainties for the same group of 
# protists in the other habitats
tot_num_habitat_CI['Number of ciliates [# g^-1]'].fillna(gmean(tot_num_habitat_CI['Number of ciliates [# g^-1]'].dropna()),inplace=True)
tot_num_habitat_CI['Number of flagellates [# g^-1]'].fillna(gmean(tot_num_habitat_CI['Number of flagellates [# g^-1]'].dropna()),inplace=True)
tot_num_habitat_CI['Number of naked amoebae [# g^-1]'].fillna(gmean(tot_num_habitat_CI['Number of naked amoebae [# g^-1]'].dropna()),inplace=True)
tot_num_habitat_CI['Number of testate amoebae [# g^-1]'].fillna(gmean(tot_num_habitat_CI['Number of testate amoebae [# g^-1]'].dropna()),inplace=True)

# Fill the uncertainty of the values for the tropical savanna with the geometric mean the uncertainties 
# for the same group of protists in the other habitats
tot_num_habitat_CI.loc['Tropical Savanna'] = gmean(tot_num_habitat_CI)
tot_num_habitat_CI


# We propagate the uncertainties associated with the estimates of the total number of protists per gram soil in each habitat to the estimate of the sum across all habitats:

# In[26]:

tot_num_habitat_CI = tot_num_habitat_CI.loc[tot_num_gmean.dropna().index.values]

ciliate_num_per_g_CI = CI_sum_prop(estimates=tot_num_gmean.dropna()['Number of ciliates [# g^-1]'],mul_CIs=tot_num_habitat_CI['Number of ciliates [# g^-1]'])
flagellate_num_per_g_CI = CI_sum_prop(estimates=tot_num_gmean.dropna()['Number of ciliates [# g^-1]'],mul_CIs=tot_num_habitat_CI['Number of ciliates [# g^-1]'])
naked_amoebea_num_per_g_CI = CI_sum_prop(estimates=tot_num_gmean.dropna()['Number of naked amoebae [# g^-1]'],mul_CIs=tot_num_habitat_CI['Number of naked amoebae [# g^-1]'])
testate_amoebea_num_per_g_CI = CI_sum_prop(estimates=tot_num_gmean.dropna()['Number of testate amoebae [# g^-1]'],mul_CIs=tot_num_habitat_CI['Number of testate amoebae [# g^-1]'])
num_per_g_CI = pd.Series([ciliate_num_per_g_CI,flagellate_num_per_g_CI,naked_amoebea_num_per_g_CI,testate_amoebea_num_per_g_CI], index= tot_num_habitat_CI.columns)
num_per_g_CI


# ### Inter-method uncertainty
# We generated two types of estimates for the total number of individual protists per gram of soil - one based on the arithmetic mean and one based on the geometric mean of values. As our best estimate we used the geometric mean of the arithmetic mean and geometric mean-based estimates. We calculate the 95% confidence interval around the geometric mean of the two types of estimates as a measure of the uncertainty this procedure introduces into the estimate of the total number of protists:

# In[27]:

inter_method_num_CI = geo_CI_calc(pd.DataFrame([tot_num_mean.sum(),tot_num_gmean.sum()]))
inter_method_num_CI


# We use the maximum of the uncertainty stemming from the intra-study and interstudy variability and the inter-method uncertainty as our best projection of the uncertainty associated with our estimate of the number of individual protists per gram of soil:

# In[28]:

best_num_CI = np.max([num_per_g_CI,inter_method_num_CI],axis=0)
best_num_CI = pd.Series(best_num_CI,index= inter_method_num_CI.index)
best_num_CI


# To convert the total number of individual protists per gram soil to an estimate of the total number of protists per $m^2$, we rely on the bulk density of soil and on an estimate of the fraction of the total biomass of soil protists in the top 8 cm of soil. We now assess the uncertainty associated with each of those parameters.
# 
# ### Bulk density of soil
# We do not have a good estimate for the uncertainy associated with the bulk density of soils. We thus use a crude uncertainty of ≈2-fold as a measure of the uncertainty associated with the bulk density of soils.
# 
# ### Fraction of biomass of protists in top 8 cm
# To estimate the fraction of the total biomass of soil protists present in the top 8 cm of soils, we rely on two estimates - one based on data from Jackson et al. and one based on data from Fierer et al. As a measure of the uncertainty associated with the estimate of the fraction of the total biomass of soil protists present in the top 8 cm of soils, we calculate the 95% confidence interval around the geometric mean of the two estmates:

# In[29]:

# We use a crude estimate of ≈2-fold as our measure of the uncertainty associated with
# the average bulk density of soils
bulk_density_CI = 2

# Calculate the 95% confidence interval around the geometric mean of our estimates for
# the fraction of the total soil biomass present in the top 8 cm
depth_frac_CI = frac_CI(np.array([jackson_fraction,fierer_frac]))
print('Our projection for the uncertainty associated with our estimate of the fraction of the total biomass of soil protists found in the top 8 cm of soil is ≈%.1f-fold' %depth_frac_CI)


# We combine the uncertainties associated with the total number of individual protists per gram soil with the uncertainties associated with the average bulk density of soil and the uncertainty associated with the fraction of the total biomass of soil protists found in the top 8 cm of soil:

# In[30]:

ciliate_num_CI = CI_prod_prop(np.array([best_num_CI['Number of ciliates [# g^-1]'],bulk_density_CI,depth_frac_CI]))
flagellates_num_CI = CI_prod_prop(np.array([best_num_CI['Number of flagellates [# g^-1]'],bulk_density_CI,depth_frac_CI]))
naked_amoebae_num_CI = CI_prod_prop(np.array([best_num_CI['Number of naked amoebae [# g^-1]'],bulk_density_CI,depth_frac_CI]))
testate_amoebae_num_CI = CI_prod_prop(np.array([best_num_CI['Number of testate amoebae [# g^-1]'],bulk_density_CI,depth_frac_CI]))
tot_num_CI = pd.Series([ciliate_num_CI,flagellates_num_CI,naked_amoebae_num_CI,testate_amoebae_num_CI], index= tot_num_habitat_CI.columns)
tot_num_CI


# ## Carbon content
# We assemble different measures of uncertainty at different levels - for values within the same study and for values between studies.
# ### Intra-study uncertainty
# For studies which report more than one measurement, we calculate the 95% confidence interval around the mean of the values. We use the maximal uncertainty as a measure of the intra-study uncertainty associated with the carbon content of protists.

# In[31]:

def groupby_geo_CI(input):
    return pd.DataFrame({'Carbon content of ciliates [g C cell^-1]': geo_CI_calc(input['Carbon content of ciliates [g C cell^-1]'].dropna()),
                        'Carbon content of naked amoebae [g C cell^-1]': geo_CI_calc(input['Carbon content of naked amoebae [g C cell^-1]'].dropna()),
                        'Carbon content of testate amoebae [g C cell^-1]': geo_CI_calc(input['Carbon content of testate amoebae [g C cell^-1]'].dropna()),
                        'Carbon content of flagellates [g C cell^-1]': geo_CI_calc(input['Carbon content of flagellates [g C cell^-1]'].dropna())},index=[0])


cc_intra_CI = cc_data.groupby('DOI').apply(groupby_geo_CI).max()


# ### Interstudy uncertainty
# We calculate the 95% confidence interval around the mean carbon content from different studies. We use the maximal uncertainty as a measure of the interstudy uncertainty associated with the carbon content of protists.

# In[32]:

cc_inter_CI = geo_CI_calc(study_mean_cc)
cc_inter_CI


# We use the maximum of the intra-study and interstudy uncertainties as our best projection of the uncertainty associated with the estimate of the carbon content of protists.

# In[33]:

best_cc_CI = np.max([cc_intra_CI,cc_inter_CI],axis=0)
best_cc_CI = pd.Series(best_cc_CI,index=cc_inter_CI.index)
best_cc_CI


# ## Calculating the total uncertainty
# We propagate the uncertainty in the total number of protists and in the carbon content of protists to the total estimate of the biomass of protists. We first calculate the uncertainty associated with the estimate of biomass of each of the groups of protists:

# In[34]:

ciliate_biomass_CI = CI_prod_prop(np.array([ciliate_num_CI,best_cc_CI['Carbon content of ciliates [g C cell^-1]']]))
flagellates_biomass_CI = CI_prod_prop(np.array([flagellates_num_CI,best_cc_CI['Carbon content of flagellates [g C cell^-1]']]))
naked_amoebae_biomass_CI = CI_prod_prop(np.array([naked_amoebae_num_CI,best_cc_CI['Carbon content of naked amoebae [g C cell^-1]']]))
testate_amoebae_biomass_CI = CI_prod_prop(np.array([testate_amoebae_num_CI,best_cc_CI['Carbon content of testate amoebae [g C cell^-1]']]))


# We then propagate the uncertainty associated with the biomass of each protist group to the estimate of the total biomass of protists:

# In[35]:

mul_CI = CI_sum_prop(estimates=(tot_num_protist*mean_cc).values.squeeze(), mul_CIs= np.array([ciliate_biomass_CI, flagellates_biomass_CI, naked_amoebae_biomass_CI, testate_amoebae_biomass_CI]))
print('Our best projection for the uncertainty associated with the estimate of the total biomass of terrestrial protists is ≈%0.f-fold' % mul_CI)


# Our final parameters are:

# In[36]:


print('Biomass of terrestrial protists: %.1f Gt C' %(best_estimate/1e15))
print('Uncertainty associated with the estimate of the total biomass of terrestrial protists: ≈%.0f-fold' % mul_CI)


old_results = pd.read_excel('../protists_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[0] = pd.Series({
                'Parameter': 'Biomass of terrestrial protists',
                'Value': float(best_estimate)/1e15,
                'Units': 'Gt C',
                'Uncertainty': mul_CI
                })

result.to_excel('../protists_biomass_estimate.xlsx',index=False)



# coding: utf-8

# In[1]:

# Import dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean
import sys
sys.path.insert(0, '../../../statistics_helper')
from openpyxl import load_workbook
from CI_helper import *
from fraction_helper import *
pd.options.display.float_format = '{:,.2f}'.format


# # Estimateing the biomass contribution of particle-attached bacteria and archaea in the ocean
# In order to estimate the total biomass of bacteria and archaea attached to particulate organic matter (POM), we assemble studies which report the local contribution of particle-attached bacteria and archaea to the total number of cells. We focus here on the two main categories of POM - macroaggregates (>0.5 mm in diameter) and microaggregates (smaller then 0.5 mm in diameter ). We estimate the biomass contribution of bacteria and archaea attached to each size category, and then sum up the contributions to estimate the total biomass of particle-attached bacteria and archaea in the ocean. We first survey data on the fraction of the total number of cells which is attached to either macro- or microaggregates. We then estimate the carbon content of particle-attached cells relative to free-living cells.
# 
# ## Fraction of number of cells which is particle-attached
# ### Macroaggregates
# In order to estimate the total biomass of bacteria and archaea attached to macroaggregates, we rely a collection of data from several studies which report the fraction of the total number of bacteria and archaea which is attached to macroaggregates. Here is a sample of the data:

# In[2]:

# Load data
macro = pd.read_excel('poc_data.xlsx','Macroaggregates')
macro.head()


# To generate our best estimate for the fraction of cells attached to macroaggregates, we first calculate the average fraction of particle-attached cells within each study. We calculate both the arithmetic mean fraction as well as the geometric mean fraction of cells.

# In[3]:

# Calculate the mean fraction of particle-attached cells whitin each study
macro_study_mean = macro.groupby('Reference')['Fraction of cells in aggregates'].apply(np.nanmean)
macro_study_gmean = macro.groupby('Reference')['Fraction of cells in aggregates'].apply(frac_mean)


# We then calculate the mean fraction of particle-attached cells between different studies. We calculate both the arithmetic mean fraction as well as the geometric mean fraction of cells. We thus generate two estimates for the fraction of particle-attached cells out of the total population of marine bacteria and archaea- one based on arithmetic means and one based on geometric means. The estimate based on the arithmetic mean is more susceptible to sampling bias, as even a single measurement which is not characteristic of the global population (such as samples which are contaminated with organic carbon sources, or samples which have some technical biases associated with them) might shift the average concentration significantly. On the other hand, the estimate based on the geometric mean might underestimate global biomass as it will reduce the effect of biologically relevant high biomass concentrations. As a compromise between these two caveats, we chose to use as our best estimate the geometric mean of the arithmetic and geometric mean estimates.

# In[4]:

# Calculate the mean fraction of particle-attached cells between different studies
macro_mean = np.nanmean(macro_study_mean)
macro_gmean = frac_mean(macro_study_gmean)

# Use the geometric mean of the arithmetic and geometric mean based estimates as our best estimate
best_macro_frac = frac_mean(np.array([macro_mean,macro_gmean]))

print('Our best estimate for the fraction of the toal number of marine bacteria and archaea which is attached to macroaggregates is ≈%.0f percent' %(best_macro_frac*100))


# Our samples of the populations of attached cells are mainly representative of the epipelagic and mesopelagic realms, but we did not find measurements of the concenetration of attached bacterial and archaeal cells in the bathypelagic realm. We therefore assume the distribution of particle attached cells is similar in the bathypelagic realm. To give some support of this assumption, we compare the average macroaggregate concentrations measured in the studies on which we rely to measurements of the concentration of macroaggregates in the deep-sea. We calculate the average concentration of macroaggregates measured in the deep-sea:

# In[5]:

# Load data on the concentration of macroaggregates in the deep-sea
deep_sea_macro = pd.read_excel('poc_data.xlsx','Macroaggregate concentration')

# Calculate the mean concentration of macroaggregates in the deep-sea
mean_deep_macro = geo_CI_calc(deep_sea_macro.groupby('Reference')['Macroaggregate concentration [# L^-1]'].apply(np.nanmean))

print('The average concentration of macroaggregates in the deep-sea is ≈%.0f aggregates per liter' %mean_deep_macro)


# This number is similar to the average number we get from the studies on which we rely our estimate:

# In[6]:

mean_shallow_macro = gmean(macro.groupby('Reference')['Concentration of macroaggregates [# L^1-]'].apply(np.nanmean).dropna())

print('The average concentration of macroaggregates in reported in the studies on which we rely is ≈%.0f aggregates per liter' %mean_shallow_macro)


# ### Microaggregates
# In order to estimate the total biomass of bacteria and archaea attached to microaggregates, we collected data from several studies which report the fraction of the total number of bacteria and archaea which  is attached to macroaggregates. Here is a sample of the data:

# In[7]:

# Load the data on microaggregates
micro = pd.read_excel('poc_data.xlsx','Microaggregates')
micro.head()


# In a similar manner to our procedure regarding macroaggregates, we calculate the arithmetic and geometric means of the fraction of particle-attached cells within each study:

# In[8]:

# Calculate the mean fraction of particle-attached cells whitin each study
micro_study_mean = micro.groupby('Reference')['Fraction of attached cells'].apply(np.nanmean)
micro_study_gmean = micro.groupby('Reference')['Fraction of attached cells'].apply(frac_mean)


# We then calculate the mean fraction of particle-attached cells between different studies. We calculate both the arithmetic mean fraction as well as the geometric mean fraction of cells. We thus generate two estimates for the fraction of particle-attached cells out of the total population of marine bacteria and archaea- one based on arithmetic means and one based on geometric means. We use as our best estimate the geometric mean of the estimates from the two methodologies.

# In[9]:

# Calculate the mean fraction of particle-attached cells between different studies
micro_mean = micro_study_mean.mean()
micro_gmean = frac_mean(micro_study_gmean)

# Use the geometric mean of the arithmetic and geometric mean based estimates as our best estimate
best_micro_frac = frac_mean(np.array([micro_mean,micro_gmean]))

print('Our best estimate for the fraction of the toal number of marine bacteria and archaea which is attached to microaggregates is ≈%.0f percent' %(best_micro_frac*100))


# ## Carbon content of particle-attached cells
# Several studies have indicated that particle-attached cells are more bigger in volume, and thus more carbon rich. To estimate the carbon content of particle-attached cells we use two strategies. The first is based on studies  which report the carbon content of particle-attached cells relative to free-living cells. We assume the carbon content of bacteria and archaea which are attached to microaggregates and macroaggregates is similar. 
# 
# ### Relative carbon content
# We first calculate the geometric mean of the size of particle-attached cells relative to free-living cells within each study. Then we calculate the geometric mean of the values reported by different studies as our best estimate for the size of particle-attached cells relative to free-living cells.

# In[10]:

# Calculate the geometric mean of the relative size of particle attached cells within each study
rel_size_study = macro.groupby(['Location','Reference'])['Size of cells relative to free-living cells'].apply(gmean)

# Calculate the geometric mean of the values reported in different studies as our best estimate
best_rel_size = gmean(rel_size_study.dropna())

print('Our best estimate for the size of particle-attached cells relative to free-living cells is ≈%1.f-fold' % best_rel_size)


# ### Volume of particle-attached cells
# We assembled studies estimating the volume of particle-attached cells. We convert this volume to carbon content using the allometric relation reported by [Simon & Azam](http://dx.doi.org/10.3354/meps051201). The allometric model is:
# $$C = 88.1 \times V^{0.59}$$
# We first calculate the geometric mean of volumes within each study:

# In[11]:

# Calculate the geometric mean of the volume of particle-attached cells reported within each study
vol_study = macro.groupby('Reference')['Volume of cells [µm^3]'].apply(gmean)


# We then calculate the geometric mean of volumes reported in different studies. We convert our best estimate to the volume of particle-attached cells to carbon content based on the formula reported in Simon & Azam. We calculate the carbon content of particle-attached cells relative to free-living cells based on our estimate for the carbon content of free-living bacteria and archaea in the ocean of ≈11 fg C (see the relevant section in the Supplementary Information for more details).

# In[12]:

# Calculate the geometric mean of volumes reported in different studies
best_vol = gmean(vol_study.dropna())

# The allometric model reported by Simon & Azam
sa_model = lambda x: 88.1*x**0.59

# Convert our best estimate for the volume of particle-attached cells to carbon content
best_cc = sa_model(best_vol)

# Our best estimate for the carbon content of free-living marine bacteria and archaea 
free_living_cc = pd.read_excel('../marine_prok_biomass_estimate.xlsx').iloc[1,1]

# Calculate the relative carbon content of particle-attached cells.
vol_rel_size = best_cc/free_living_cc

print('Our best estimate for the carbon content of particle-attached cells relative to free-living cells based on volume is ≈%1.f-fold' % vol_rel_size)


# We use the geometric mean of the two estimates of the carbon content of particle-attached cells relative to free-living cells as our best estimate:

# In[13]:

best_rel_cc= gmean([best_rel_size,vol_rel_size])
print('Our best estimate for the carbon content of particle-attached cells relative to free-living cells is ≈%1.f-fold' % best_rel_cc)


# To estimate the fraction of the total biomass of marine bacteria and archaea which is particle-attached, we sum up the fraction of the total number of cells contributed by cells attached to micro- and macroaggregates, and multiply it by the relative carbon content of particle-attached cells:

# In[14]:

best_estimate = (best_macro_frac+best_micro_frac)*best_rel_cc

print('Our best estimate for the fraction of the total biomass of marine bacteria and archaea which is particle-attached is ≈%.0f percent' %(best_estimate*100))


# # Uncertainty analysis
# To project the uncertainty associated with our estimate of the fraction of the total biomass of marine bacteria and archaea which is particle-attached, we first project the uncertainty associated with the two factors of our estimate - the fraction of the total number of cells which is particle-attached and the relative carbon content of particle-attached cells
# 
# ## Fraction of cells
# We first assess the uncertainty associated with the estimate of the fraction of the total number of cells which is attached to microaggregates and macroaggregates. We then propagate the uncertainty from each fraction to our estimate of the total fraction of cells. We begin with the uncertainty associated with our estimate of the total number of cells which are attached to microaggregates.
# 
# ### Microaggregates
# We collect both the intra-study uncertainty and the interstudy uncertainty associated with our estimate of the fraction of the total number of marine bacteria and archaea which are attached to microaggregates. We use the maximum of this collection of uncertainties as our best projection of the uncertainty associated with our estimate of the fraction of the total number of marine bacteria and archaea whcih are attached to microaggregates.
# #### Intra-study uncertainty
# We calculate the 95% confidence interval around the mean fraction of microaggregate-attached cells within each study:

# In[15]:

# Calculate the 95% confidence interval around the mean fraction of cells attached to microaggregates 
# within each study
micro_study_CI = micro.groupby('Reference')['Fraction of attached cells'].apply(frac_CI)


# #### Interstudy uncertainty
# We calculate the 95% confidence interval around the mean fraction of microaggregate-attached cells between differnt studies:

# In[16]:

# Calculate the 95% confidence interval around the mean fraction of cells attached to microaggregates 
# between different studies
micro_CI = frac_CI(micro_study_gmean)


# #### Inter-method uncertainty
# We calculate the 95% confidence interval around the geometric mean between the estimate based on arithmetic means and geometric means of the fraction of cells attached to microaggregates:

# In[17]:

# Calculate the 95% confidence interval around the geometric mean of the estimates based on arithmetic means
# and geometric means
micro_inter_method_CI = frac_CI(np.array([micro_mean,micro_gmean]))


# We use the maximum of the collection of uncertainties as our best projection for the uncertainty associated with our estimate of the fraction of the total number of bacteria and archaea which is attached to microaggregates:

# In[18]:

micro_frac_CI = np.max([micro_inter_method_CI,micro_study_CI.max(),micro_CI])
print('Our best projection for the uncertainty associated with our estimate of the total number of bacteria and archaea which is attached to microaggregates is ≈%.1f-fold' %micro_frac_CI)


# ### Macroaggregates
# We collect both the intra-study uncertainty and the interstudy uncertainty associated with our estimate of the fraction of the total number of marine bacteria and archaea which are attached to macroaggregates. We use the maximum of this collection of uncertainties as our best projection of the uncertainty associated with our estimate of the fraction of the total number of marine bacteria and archaea whcih are attached to macroaggregates.
# #### Intra-study uncertainty
# We calculate the 95% confidence interval around the mean fraction of macroaggregate-attached cells within each study:

# In[19]:

# Calculate the 95% confidence interval around the mean fraction of cells attached to macroaggregates 
# within each study
macro_study_CI = macro.groupby('Reference')['Fraction of cells in aggregates'].apply(frac_CI)


# #### Interstudy uncertainty
# We calculate the 95% confidence interval around the mean fraction of macroaggregate-attached cells between differnt studies:

# In[20]:

# Calculate the 95% confidence interval around the mean fraction of cells attached to microaggregates 
# between different studies
macro_CI = frac_CI(macro_study_gmean)


# #### Inter-method uncertainty
# We calculate the 95% confidence interval around the geometric mean between the estimate based on arithmetic means and geometric means of the fraction of cells attached to microaggregates:

# In[21]:

# Calculate the 95% confidence interval around the geometric mean of the estimates based on arithmetic means
# and geometric means
macro_inter_method_CI = frac_CI(np.array([macro_mean,macro_gmean]))


# We use the maximum of the collection of uncertainties as our best projection for the uncertainty associated with our estimate of the fraction of the total number of bacteria and archaea which is attached to macroaggregates:

# In[22]:

macro_frac_CI = np.max([macro_inter_method_CI,macro_study_CI.max(),macro_CI])
print('Our best projection for the uncertainty associated with our estimate of the total number of bacteria and archaea which is attached to macroaggregates is ≈%.1f-fold' %macro_frac_CI)


# We propagate the uncertainties associated with the estimates of the fraction of the total number of marine bacteria and archaea attached to micro- and macroaggregates to the final estimate of the fraction of marine bacteria and archaea which is particle-attached:

# In[23]:

# Propagate the uncertainties of the fraction of cells attached to micro- and macroaggregates
# to the estiamte of the fraction of cells which is particle-attached
num_frac_CI = CI_sum_prop(estimates=np.array([best_micro_frac,best_macro_frac]),mul_CIs=np.array([micro_frac_CI,macro_frac_CI]))
print('Our best projection for the uncertainty associated with our estimate of the total number of bacteria and archaea which is particle-attached is ≈%.1f-fold' %num_frac_CI)


# ## Relative carbon content
# We assess the uncertainty associated with the estimate of the relative carbon content of particle-attached cells. We used two independent methods to estimate the relative carbon content. We assess the unertainty associate with each one of them.
# ### Relative size-based
# We collect both the intra-study uncertainty and the interstudy uncertainty associated with our estimate of the size of particle-attached cells relative to free-livign cells. 
# #### Intra-study
# We calculate the 95% confidence interval around the mean size of particle-attached cells reltive to free-living cells within each study:

# In[24]:

size_intra_CI = macro.groupby(['Location','Reference'])['Size of cells relative to free-living cells'].apply(geo_CI_calc)


# #### Inter-study
# We calculate the 95% confidence interval around the mean size of particle-attached cells reltive to free-living cells between different studies:

# In[25]:

size_inter_CI = geo_CI_calc(rel_size_study.dropna())


# ### Volume-based
# We collect both the intra-study uncertainty and the interstudy uncertainty associated with our estimate of the volume of particle-attached cells. 
# #### Intra-study
# We calculate the 95% confidence interval around the mean volume of particle-attached cells within each study:

# In[26]:

vol_intra_CI = macro.groupby('Reference')['Volume of cells [µm^3]'].apply(geo_CI_calc)


# #### Inter-study
# We calculate the 95% confidence interval around the mean volume of particle-attached cells between different studies:

# In[27]:

vol_inter_CI = geo_CI_calc(vol_study.dropna())


# ### Inter-method uncertainty
# We calculate the 95% confidence interval around the geometric mean between the size-based estimate and the volume based estimate:

# In[28]:

cc_inter_method_CI = geo_CI_calc(np.array([vol_rel_size,best_rel_size]))


# We use the maximum of the collection of uncertainties for both the volume-based methoda and the size based method as our best projection of the uncertainty associated with our estimate of the relative carbon content of particle-attached bacteria and archaea:

# In[29]:

cc_CI = np.max([cc_inter_method_CI,vol_inter_CI,vol_intra_CI.max(),size_inter_CI,size_intra_CI.max()])
print('Our best projection for the uncertainty associated with our estimate of the relative carbon content of particles-attached bacteria and archaea is ≈%.1f-fold' %cc_CI)


# We combine our projections for the uncertainty associated with our estimate of the fraction of the total number of cells which is particle-attached and our estimate of the relative carbon content of particle-attached cells.

# In[30]:

mul_CI = CI_prod_prop(np.array([cc_CI,num_frac_CI]))
print('Our best projection for the uncertainty associated with our estimate of the fraction of the total biomass of marine bactetia and archaea which is particle-attached is ≈%.1f-fold' %mul_CI)


# Our final parameters are:

# In[31]:

print('Fraction of the total biomass of marine bacteria and archaea which is particle-attahced: %.1e' % best_estimate)
print('Uncertainty associated with the fraction of the biomass of marine bacteria and archaea which is particle-attached: %.1f-fold' % mul_CI)

old_results = pd.read_excel('../marine_prok_biomass_estimate.xlsx')
result = old_results.copy()

if (result.shape[0]==0):
    result = pd.DataFrame(index= range(4), columns=['Parameter','Value','Units','Uncertainty'])

result.loc[4] = pd.Series({
                'Parameter': 'Fraction of the total biomass of marine bacteria and archaea which is particle-attached',
                'Value': best_estimate,
                'Units': 'Unitless',
                'Uncertainty': "{0:.1f}".format(mul_CI)
                })

result.to_excel('../marine_prok_biomass_estimate.xlsx',index=False)

# We need to use the results on the carbon content of particle-attached cells
# for our estimate of the total biomass of particle-attached protists, 
# so we feed these results to the data used in the estimate of the total
# biomass of particle-attached protists
path = '../../../protists/marine_protists/marine_protists_data.xlsx'
marine_protists_data = pd.read_excel(path,'POC prokaryotes')

marine_protists_data.loc[0] = pd.Series({
                'Parameter': 'Carbon content of particle-attached prokaryotes',
                'Value': best_cc,
                'Units': 'fg C cell^-1',
                'Uncertainty': cc_CI
                })
writer = pd.ExcelWriter(path, engine = 'openpyxl')
book = load_workbook(path)
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)


marine_protists_data.to_excel(writer, sheet_name = 'POC prokaryotes',index=False)
writer.save()


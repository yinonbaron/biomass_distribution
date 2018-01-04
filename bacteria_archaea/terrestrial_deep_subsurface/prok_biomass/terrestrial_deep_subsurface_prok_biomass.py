
# coding: utf-8

# # Estimating the total biomass of bacteria and archaea in the terrestrial deep subsurface
# This notebook details the procedure for estimating the total biomass of  of prokaryotes (bacteria and archaea) in the terrestrial deep subsurface. Our estimate is based on the data on cellconcentration in the terrestrial deep subsurface collected by [McMahon & Parnell](http://dx.doi.org/10.1111/1574-6941.12196), as well as data on the global volume of groundwater from [Gleeson et al.](http://dx.doi.org/10.1038/ngeo2590).
# 
# ## Number of cells
# To estimate the total number of cells of bacteria and archaea in the terrestrial deep subsurface, we follow a similar methodology to that detailed in McMahon & Parnell. We use ≈100 measurements of cell concentration in groundwater samples from depths of 0-2000 m. We bin the samples based on their depths to 250 meter bins. For each bin we calculate both the arithmetic and geometric means. Depth bins missing from the data were extrapolated by using a regression equation that predicts the concentration of cells from the depth of the sample. This yields two estimates for the characteristic cell concentration at each depth bin.

# In[1]:


import pandas as pd
import numpy as np
from scipy.stats import gmean
from scipy.optimize import curve_fit
import sys
sys.path.insert(0, '../../../statistics_helper')
from CI_helper import *

# Load original data from Figure 1 of McMahon & Parnell
mp_data = pd.read_csv('terrestrial_deep_subsurface_prok_cell_num.csv',skiprows=1)

# Define depth bins every 250 meter 
bins = np.linspace(0,2000,9)

# Filter deeper then 2km
mp_data_filt = mp_data[mp_data['Depth [m]'] < 2000]

# Bin data based on depth bins
mp_data_filt['Depth bin'] = pd.cut(mp_data_filt['Depth [m]'],bins)
depth_binned = mp_data_filt.groupby('Depth bin')

# Calculate the mean concentration at each depth bin
bin_mean = depth_binned['Cell concentration [cells mL-1]'].mean().dropna()
bin_geo_mean = depth_binned['Cell concentration [cells mL-1]'].apply(gmean)

# To estimate the last bin (1750-2000), which doesn't have data, we either use the fit produced by McMahon & Parnell
# or fit a function to the geometric means

# The fit of McMahon & Parnell from Figure 1
mp_fit = lambda x: np.exp(-(x-5771.2)/390.6)

# Extrapolate the average cell concentration based on the fit by McMahon & Parnell
extrapolated_mean = pd.DataFrame({'Depth bin': '(1750.0, 2000.0]', 'Cell concentration [cells mL-1]': mp_fit(1875)},index=[0])

# Add the extrapolated value to the depth averages
bin_mean = bin_mean.reset_index().append(extrapolated_mean,ignore_index=True).set_index('Depth bin')


# Define an exponential function to fit the data
def depth_func_log(x, a, b):
    return np.log(a) - b*x

# Fit the geometric means
xdata = bins[1:-1]-125
popt2, pcov2 = curve_fit(depth_func_log, xdata, np.log(bin_geo_mean[:-1]))

# Extrapolate the geometric mean cell concentration based on the fit we calculated
extrapolated_geo_mean = np.exp(depth_func_log(1875, *popt2))

# Add the extrapolated value to the depth averages
tmp = bin_geo_mean.reset_index()
tmp['Cell concentration [cells mL-1]'][7] = extrapolated_geo_mean
bin_geo_mean = tmp.set_index('Depth bin')


# To calculate the total number of cells in groundwater from the characteristic concentrations at each depth bin, we use estimates of the total volume of ground water, and the fraction of the total ground water at each depth bin.
# 
# We rely of data from Gleeson et al. which estimate $≈2.2×10^{22}$ mL of groundwater in the top 2 km of the terrestrial crust. Glesson et al. also estimate the fraction of the total volume of groundwater found at each depth. To estimate the fraction of groundwater found at each bin, we fit a function to the data provided in Figure 1 of Gleeson et al., and integrate it over the depth range of each depth bin. We then normalize the numbers by the integral over the entire 2000 meter range to calculate the fraction of water found at each depth bin.
# 
# We multiply the average cell concentration at each bin by the total volume of groundwater at each bin, and sum over all bins to calculate the total number of cells in groundwater. We have two estimates for the total number of cells in groundwater, one based on arithmetic means of cell concentrations at each bin and the second based on geometric means.

# In[2]:



# Total volume of groundwater [mL], based on Gleeson et al.
tot_gw_vol = 2.26e22

# Load data from Gleeson et al. on the distribution of groundwater with depth
gw_depth_dist = pd.read_csv('gleeson_fraction_gw_data.csv', skiprows=1)

# Generate functions to fit the data an calculate partial integrals
def func(x,a,b,c):
    return a*np.exp(-b*x)+c

def frac_func(x0,x1,a,b,c):
    integral = lambda x: -a/b*np.exp(-b*x) + c*x
    int_x = integral(x1) - integral(x0)
    int_total = integral(2000) - integral(0)
    fraction = int_x/int_total
    return fraction

# Fit the data with the fiting function
popt, pcov = curve_fit(func, gw_depth_dist['depth [m]'], gw_depth_dist['fraction'],bounds=(0, [0.2, 2., 0.5]))

# Calculate the fraction of groundwater in each bin
depth_gw_fraction = []
lower_depth_range = np.linspace(0,1750,8)
upper_depth_range = np.linspace(250,2000,8)
for ix, y in enumerate(lower_depth_range):
    depth_gw_fraction.append(frac_func(lower_depth_range[ix],upper_depth_range[ix], *popt))
depth_gw_fraction = np.array(depth_gw_fraction)



cell_mean = (bin_mean['Cell concentration [cells mL-1]']*depth_gw_fraction).sum()
cell_geo_mean = (bin_geo_mean['Cell concentration [cells mL-1]']*depth_gw_fraction).sum()

tot_cell_gw_mean = cell_mean*tot_gw_vol
tot_cell_gw_geo_mean = cell_geo_mean*tot_gw_vol

print('Our estimate for the total of number of cells cells in groundwater based on arithmetic means of cell concentrations is  %.0e cells.' %tot_cell_gw_mean)
print('Our estimate for the total of number of cells cells in groundwater based on geometric means of cell concentrations is  %.0e cells.' %tot_cell_gw_geo_mean)

# We need this data for also for estimating the total biomass of phages in the terrestrial deep subsurface,
# so we export these results as data for the section estimating the total number of phages in the 
# terrestrial deep subsurface
writer = pd.ExcelWriter('../../../viruses/phage_num/terrestrial_deep_subsurface/terrestrial_deep_subsurface_prok_num.xlsx', engine='xlsxwriter') 

export_mean = bin_mean['Cell concentration [cells mL-1]'].reset_index()
export_mean['Depth bin'] = export_mean['Depth bin'].astype(str)
export_geo_mean = bin_geo_mean['Cell concentration [cells mL-1]'].reset_index()
export_geo_mean['Depth bin'] = export_geo_mean['Depth bin'].astype(str)
export_data_frame = export_mean.merge(export_geo_mean,on='Depth bin')
export_data_frame.columns = ['Depth bin [m]','Mean cell concentration [cells mL-1]','Geometric mean cell concentration [cells mL-1]']
export_data_frame.to_excel(writer,sheet_name='Cell concentration')
export_water_vol = pd.concat([export_data_frame['Depth bin [m]'].astype(str),pd.Series(depth_gw_fraction*tot_gw_vol)],axis=1)
export_water_vol.columns = ['Depth bin [m]','Water volume [mL]']
export_water_vol.iloc[7,0] = '(1750.0, 2000.0]'
export_water_vol.to_excel(writer,sheet_name='Water volume')
writer.save()
writer.close()


# Most of the cells in the terrestrial subsurface are actually found attached to surfaces and not free-living in groundwater. McMahon & Parnell rely on data from the literature of the attached to unattached cell number ratio, and report a range of $10^2-10^3$ for this range. We use as our best estimate for this ratio the geometric mean of this range, which is roughly 300. Multiplying the total number of cells in groundwater by this ratio gives us an estimate for the total number of bacteria and archaea in the terrestrial deep subsurface. 

# In[3]:


# Fraction of attached/unattached cells (geometric mean of 10^2 and 10^3)
attached_unattached_ratio = gmean([1e2,1e3])

# Calculate the total number of cells in the terrestrial deep subsurface
tot_cell_num_mean = tot_cell_gw_mean*attached_unattached_ratio
tot_cell_num_geo_mean = tot_cell_gw_geo_mean*attached_unattached_ratio

print('Our estimate for the total of number of cells cells in the terrestrial deep subsurface based on arithmetic means of cell concentrations is  %.0e cells.' %tot_cell_num_mean)
print('Our estimate for the total of number of cells cells in the terrestrial deep subsurface based on geometric means of cell concentrations is  %.0e cells.' %tot_cell_num_geo_mean)


# We generated two types of estimates for the total number of cells in the terrestrial deep subsurface: an estimate which uses the arithmetic mean of cell concentrations at each depth bin, and an estimate which uses the geometric mean of cell concentrations at each depth bin. The estimate based on the arithmetic mean is more susceptible to sampling bias, as even a single measurement which is not characteristic of the global population (such as samples which are contaminated with organic carbon sources, or samples which have some technical biases associated with them) might shift the average concentration significantly. On the other hand, the estimate based on the geometric mean might underestimate global biomass as it will reduce the effect of biologically relevant high biomass concentrations. As a compromise between these two caveats, we chose to use as our best estimate the geometric mean of the estimates from the two methodologies.

# In[4]:


best_tot_cell_num = gmean([tot_cell_num_mean,tot_cell_num_geo_mean])
print('Our best estimate for the total of number of cells cells in the terrestrial deep subsurface %.1e cells.' %best_tot_cell_num)


# 
# ## Carbon content of a single prokaryote
# McMahon & Parnell estimate the characteristic carbon content of single bacterial and arhcaeal cells in the terrestrial deep subsurface at 26 fg C cell$^{-1}$, based on carbon content of cultivated cells under starvation. This value is consistent with our estimates for the carbon content of cells in the marine and marine deep subsurface environments.
# 
# To estimate the total biomass of bacteria and archaea in the terrestrial deep subsurface, we muliply our best estimate for the total number of cells in the terrestrial deep subsurface by the characteristic carbon content of cells in the terrestrial deep subsurface. Our best estimate is ≈60 Gt C.

# In[5]:


# The characteristic carbon content of a single prokaryote in the terrestrial deep subsurface
carb_content = 26e-15

# Calculate the biomass of bacteria and archaea in the terrestrial deep subsurface
best_estimate = best_tot_cell_num*carb_content
print('We estimate a total biomass of bacteria and archaea in the terrestrial deep subsurface of %.0f Gt C' %(best_estimate/1e15))


# # Uncertainty analysis
# To assess the uncertainty of our estimate of the total biomass of bacteria and archaea in the terrestrial deep subsurface, we calculate the uncertainty associated with each of the components of the estimate: the average cell concentration in groundwater, the total amount of groundwater, the ratio of attached to unattached cells, and the carbon content of single cells.
# 
# ## Average cell concentration
# McMahon & Parnell do not supply an uncertainty estimate for the average concentration of cells in the terretrial deep subsurface. The only effect estimated by McMahon & Parnell related to the average concentration of cells, was the effect of different compaction coefficients, determining the relative fraction of water located at different depths on the average cells concentration. By varying the compaction coeffieinct, McMahon & Parnell reported an effect of ≈30% on the average concentration of cells.
# To calculate the uncertainty associated with the process of estimating average cell concentrations at each depth bin, we collect uncertainties stemming from different sources.
# 
# ### Intra-depth bin uncertainty
# Based on the data of cell concentrations, we estimate the 95% confidence interval for the average cell concentration at each depth bin, and propagate this uncertainty to the total number of cells. We estimate the 95% confidence interval for both the arithmetic mean and geometric mean of the cell concentration at each depth bin.
# We estimate the uncertainty around the estimate of cell concentration at each depth bin, and then propagate the uncertainty at each depth bin to the final estimate of the average cell concentration. 

# In[6]:


# Define a function that will estimate the 95% confidence interval for the arithmetic mean of each bin
def bin_se(input):
    se = input['Cell concentration [cells mL-1]'].std(ddof=1)/np.sqrt(input.shape[0])
    mean = input['Cell concentration [cells mL-1]'].mean()
    return (1.96*se+mean)/mean

# Define a function that will estimate the 95% confidence interval for the geometric mean of each bin
def bin_geo_CI_calc(input):
    return geo_CI_calc(input['Cell concentration [cells mL-1]'])

# Calculate the 95% confidence interval for the arithmetic mean at each bin
bin_mean_CI = depth_binned.apply(bin_se).dropna()

# Calculate the 95% confidence interval for the geometric mean at each bin
bin_geo_mean_CI = depth_binned.apply(bin_geo_CI_calc).dropna()

# Propoagate the uncertainty at each bin to the average cell concentration
av_conc_mean_CI = CI_sum_prop(bin_mean['Cell concentration [cells mL-1]'][:-1]*depth_gw_fraction[:-1],bin_mean_CI)
print('The uncertainty associated with the arithmetic mean of cell concentrations at each depth bin is ≈%.1f-fold' %av_conc_mean_CI)

# Propoagate the uncertainty at each bin to the average cell concentration
av_conc_geo_mean_CI = CI_sum_prop(bin_geo_mean['Cell concentration [cells mL-1]'][:-1]*depth_gw_fraction[:-1],bin_geo_mean_CI)
print('The uncertainty associated with the geometric mean of cell concentrations at each depth bin is ≈%.1f-fold' %av_conc_geo_mean_CI)


# ### Inter-method uncertainty
# For our best estimate of the total number of cells in the terrestrial deep subsurface, we used the geometric mean of the two estimates - the one based on arithmetic means of cells concentrations at each depth bin and the one based on the geometric mean of cell concentrations at each depth bin. We estimate the 95% confidence interval fo the geometric mean of these two estimates, which is ≈
# We calculate an uncertainty of ≈1.3-fold from this source. Combining these two sources together, we estimate ≈1.4-fold uncertainty associated with the average concentration of cells of bacteria and archaea in the terrestrial deep subsurface.

# In[7]:


inter_method_CI = geo_CI_calc(np.array([tot_cell_num_mean,tot_cell_num_geo_mean]))
print('The total uncertainty of the geometric mean of our estimates based on the two different methodologies for calculating the average cell concentration at each depth bin is ≈%.1f-fold' %inter_method_CI)


# As our best projection for the uncertainty associated with the average concentration of cells in groundwater, we take the maximum uncertainty from the intra-depth bin and inter-method uncertainties, which is ≈2.3-fold.

# In[8]:


av_cell_CI = np.max([av_conc_mean_CI,av_conc_geo_mean_CI,inter_method_CI])
print('Our best projection for the uncertainty associated with the average concentration of cell in groundwater is ≈%.1f-fold' %av_cell_CI)


# ## Total volume of groundwater
# As a measure of the uncertainty associated with the total volume of groundwater, we use the range reported in Gleeson et al. of ≈2.2-fold. This range does not represent 95% confidence interval, but rather a 25% and 75% range.  As no 95% confidence interval is available, we assume the distribution of estimates of the global volume of groundwater is nearly gaussian, and take about two standard deviations as our estimate for the 95% confidence interval. We calculate the fold change of the 95% confidence interval relative to the mean estimate.

# In[9]:


# We take the lower and upper range reported by Gleeson et al.
lower_gleeson = 1.6e22
upper_gleeson = 3.0e22

# Calculate the relative fold change of the 95% confidence interval
gw_upper_CI = upper_gleeson*1.96/tot_gw_vol
gw_lower_CI = lower_gleeson*1.96/tot_gw_vol

# Our estimate for the 95% confidence interval is the mean of the upper and lower fold changes
gw_CI = np.mean([gw_upper_CI,gw_lower_CI])

print('Our estimate for the uncertainty associated with the total volume of groundwater is ≈%.0f-fold' % gw_CI)


# ## Ratio of attached to unattached cells
# McMahon & Parnell report a range of $10^2-10^3$ for the attached to unattached cell ratio. As we chose to use the goemetric mean of this range for our estimate, we use the 95% confidence interval around the geometric mean of the two extremes of the range, as a measure of the uncertainty associated with the ratio of attached to unattached cells.
# 
# ## Carbon content of single cells
# McMahon & Parnell do not suply an uncertainty analysis for the carbon content of single cells in the terrestrial deep subsurface. Our estimate for carbon content of subseafloor sediments is similar to the value used by McMahon & Parnell. Therefore, we use the values for the uncertainty associated with the carbon content of cells in subseafloor sediments as a measure of the uncertainty associated with the carbon content of cells in the terrestrial deep subsurface. The uncertainty we calculated for the carbon content of cell in subseafloor sediments is ≈2.2-fold.

# In[10]:


attached_unattached_CI = geo_CI_calc(np.array([100,1000]))

carbon_content_CI = 2.2

mul_CI = CI_prod_prop(np.array([av_cell_CI,gw_CI,attached_unattached_CI,carbon_content_CI]))
print('The uncertainty associated with the biomass of bacteria and archaea in the terrestrial deep subsurface is ≈%.0f-fold' % mul_CI)


# ## Additional sources of uncertainty
# Combining all the uncertainty of the factors above, we calculate an uncertainty of ≈14-fold in the biomass of bacteria and archaea in the terrestrial deep subsurface.
# As we state in the Supplementary Information, there are other sources of uncertainty that for which we are not able to provide a quantitative estimate. The procedure of binning cell concentrations with depth and fitting an equation which extrapolates cell concentrations across all depths has uncertainty associated with it, and while we did calculate some uncertainty associated with this process, it probably does not represent the entire uncertainty associated with this process. The uncertainty stemming from possible contribution from groundwater deeper than 2 km is also hard to quantify, as the cell concentration at those depths and the volume of groundwater are poorly explored. We thus chose to project an uncertainty of ≈20-fold as our best projection of the uncertainty associated with the biomass of bacteria and archaea in the terrestrial deep subsurface.

# In[11]:


# Modify the uncertainty of the estimate
mul_CI = 20

print('Total biomass of terrestrial deep subsurface bacteria and archaea: %.0f Gt C' % (best_estimate/1e15))
print('Uncertainty associated with the total biomasss of terrestrial deep subsurface bacteria and archaea: %.0f-fold' % mul_CI)

old_results = pd.read_excel('../terrestrial_deep_subsurface_prok_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[0] = pd.Series({
                'Parameter': 'Total biomass of bacteria and archaea in the terrestrial deep subsurface',
                'Value': int(best_estimate),
                'Units': 'g C',
                'Uncertainty': "{0:.1f}".format(mul_CI)
                })

result.to_excel('../terrestrial_deep_subsurface_prok_biomass_estimate.xlsx',index=False)



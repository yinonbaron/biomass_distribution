
# coding: utf-8

# In[1]:

# Load dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
import sys
sys.path.insert(0, '../../statistics_helper/')
from CI_helper import *
pd.options.display.float_format = '{:,.0f}'.format


# # Estimating the characteristic size of phages
# In order to estimate the characteristic size of phages, we rely of data from quantitative transmission electron microscopy (qTEM) measurement of samples from 41 sites across the world's oceans, reported by [Brum et al.](http://dx.doi.org/10.1126/science.1261498). We extracted the data from figure 1 in Brum et al.:

# In[2]:

# Load the data extracted from Brum et al.
data = pd.read_excel('phage_size_data.xlsx',skiprows=1)
data.head()


# We use the geometric mean of the median diameters from each site as our best estimate for the characteristic diameter of phages:

# In[3]:

phage_rad = gmean(data['Median diameter [nm]'])/2
print('Our best estimate for the radius of a phage is ≈%i nm.' %(phage_rad))


# In[4]:

r = (data['95% diameter [nm]']-data['Median diameter [nm]']).mean()


# ## Estimating the carbon content of phages
# To estimate the carbon content of phages, we rely on a biophysical model described in [Jover et al.](http://dx.doi.org/10.1038/nrmicro3289), which describes the carbon content of a phage as a function of its radius. The relation between the radius of phages and their total number of carbon atoms described in Jover et al. is: 
# $$ C_{head} = \frac{4\pi(r_c-h)^3C_{bp}fill}{3v_{bp}} + \frac{4\pi d_C(3r_c^2h-3h^2r_c+h^3)}{3}$$
# Where $C_{head}$ is the total number of carbon atoms, $r_c$ is the radius of the phage, h is the thickness of the phage capsid, $C_{bp}$ is the number of carbon atoms in a single base pair of DNA, *fill* is that fraction of the phage volume that is filled with DNA, $v_{bp}$ is the volume of a single base pair of DNA, and $d_C$ is the number of carbon atoms per volume of protein.
# 
# To get from the total number of carbon atoms to an estimate of the carbon content of a single phage, we can multiply the total number of atoms by the molecular weight of carbon, and divide by Avogadro's number.
# 
# Jover et al. supply estimates for each of the parameters in the model, as well as their respective uncertainties. We plug into this model our estimates for the radius of phages in order to get an estimate for the carbon content of phages, as well as the uncertainty associated with this esitmate. We use 1.96 times the uncertainty reported in Jover et al. to calculate 95% confidence interval for the carbon content estimate.

# In[5]:

# Import uncertainties library to deal with the error propagation
from uncertainties import ufloat

##############################
# Define the model parameters#
##############################

# The phage radius we calculated in the phage size section [nm]
r_c = phage_rad

# The thickness of the phage capsid [nm]
h = ufloat(2.5,0.3*1.96)

# The number of caron atoms in a single DNA base pair
C_bp = ufloat(19.5,0.1*1.96)

# The fraction of the phage capsid filled with DNA
fill = ufloat(0.53,0.04*1.96)

# The volume of a single base pair [nm^3]
v_bp = ufloat(0.34*np.pi,0)

# The number of carbon atoms per volume of proteins [# nm^-3]
d_C = ufloat(31,1*1.96)

#Avogadro's number [molecules per mol]
Na = 6e23 

# Molecular weight of carbon [g per mol]
M_C = 12

# Define the eqation for deriving the carbon content of a phage as a function of it's radius
func = lambda x: ((4*np.pi*(x-h)**3*C_bp*fill)/(3*v_bp) + 4*np.pi*d_C*(3*x**2*h-3*h**2*x+h**3)/3)*M_C/Na

#C_head = (4*np.pi*(r_c-h)**3*C_bp*fill)/(3*v_bp) + 4*np.pi*d_C*(3*r_c**2*h-3*h**2*r_c+h**3)/3

# Calculate our best estimate for the carbon content of a single phage
best_estimate = func(r_c)

print(func(r_c)*1e31)
print('Our best estimate for the carbon content of a single phage is ≈{:10.1e} g'.format(best_estimate))


# # Uncertainty analysis
# To assess the uncertainty associated with the estimate of the radius of a single phage, we use the variability of capsid radii in the sites reported in Brum et al. We calculate the relative multiplicative uncertainty of the variation within a site and between sites. We take the higher uncertainty of the two as our best estimate for the uncertainty associated with the radius of phages.

# In[6]:

intra_CI = 1+gmean((data['95% diameter [nm]'] - data['5% diameter [nm]'])/data['Median diameter [nm]']/2)
inter_CI = geo_CI_calc(data['Median diameter [nm]'])

print('The intra site uncertainty in the radius of phages is ≈%0.1f-fold' %intra_CI)
print('The intra sample uncertainty in the radius of phages is ≈%0.2f-fold' %inter_CI)

rad_CI = np.max([intra_CI,inter_CI])


# In each site Brum et al. sampled ≈100 phages, so the intra-site uncertainty should be much lower. Nevertheless, the uncertainty we calculated doesn’t take into consideration the fact that viruses from other environments might have different size ranges. Even though phages isolated from deep terrestrial deep subsurface seem to be in the same size range range ([Eydal et al.](http://dx.doi.org/10.1038/ismej.2009.66)), we chose to use the 95% variability within each site as a measure of the uncertainty in the radius of a single pahge, to take into account possible variability of phage sizes in other environments.
# 
# To propagate the uncertainty in the radius of a single phage into the uncertainty in the carbon content of a single phage, we use a numerical approach. We chose to use this approach as propagating the uncertainty in the radius of phages creates a probability distribution of the carbon content of a single phage which is not gaussian, and thus the uncertainty ranges a normal error propagation procedure will output will be non-informative. Namely, the additive standard error that we will get will be higher than the nominal estimate, but in reality there is no phage with a netagive radius length.
# Therefore, in order to quanitfy the uncertainty of the carbon content of a single phage stemming from the uncertainty in our estimate for the radius of a single phage, we sample 1000 times from a log-normal distribution of radii with a mean that is equal to our best estimate for the radius of a phage, and a multiplicative standard diviation which is equal to the uncertainty for the radius of a phage we project. We feed these sampled radii into our model and calculate a carbon content for each radius, resulting in a distribution of carbon content estimates. We take the multiplicative ratio between the 2.5% and 97.5% percentiles and our best estimate for the carbon content as our best estimate for the uncertainty of the carbon content of a single phage stemming from the uncertainty in our estimate for the radius of a single phage.

# In[7]:

# Sample 1000 from a log-normal distribution of radii
rad_dist = np.random.lognormal(np.log(phage_rad),np.log(rad_CI)/1.96,1000)

# Calculate the carbon content for each radius
cc_dist = func(rad_dist)

# Calculate the upper and lower multiplicative ratios of the carbon content
upper_CI = np.percentile([x.nominal_value for x in cc_dist],97.5)/best_estimate
lower_CI = best_estimate/np.percentile([x.nominal_value for x in cc_dist],2.5)

rad_cc_CI = np.mean([upper_CI,lower_CI]).nominal_value

print('Our best estimate for the uncertainty of the carbon content of a single phage stemming from the uncertainty in our estimate for the radius of a single phage is ≈%.1f-fold' %rad_cc_CI)


# The uncertainty associated with the parameters of the model is ≈1.2-fold:

# In[8]:

model_param_CI =  1+best_estimate.std_dev*1.96/best_estimate.nominal_value
print('The uncertainty associated with the parameters of the model is %.1f-fold' %model_param_CI)


# We combine these two uncertainties as our best projection for the uncertainty associated with the carbon content of a single phage:

# In[9]:

mul_CI = CI_prod_prop(np.array([rad_cc_CI,model_param_CI]))
print('Our best projection for the uncertainty associated with the carbon content of a single phage is ≈%.1f-fold' %mul_CI)


# Our final parameters are:

# In[10]:

print('Our best estimate for the carbon content of a single phage: %.0e g' % best_estimate.nominal_value)
print('Uncertainty associated with the estiamte of the carbon content of a single phage: %.0f-fold' % mul_CI)

old_results = pd.read_excel('../phage_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[0] = pd.Series({
                'Parameter': 'Carbon content of a single phage',
                'Value': best_estimate.nominal_value,
                'Units': 'g C per individual',
                'Uncertainty': mul_CI
                })

result.to_excel('../phage_biomass_estimate.xlsx',index=False)


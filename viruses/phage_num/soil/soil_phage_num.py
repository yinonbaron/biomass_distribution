
# coding: utf-8

# In[1]:

# Load dependencies
import pandas as pd
from scipy.stats import gmean
import sys
sys.path.insert(0, '../../../statistics_helper/')
from CI_helper import *


# # Estimating the total number of phages in soils
# We could not come by many data for the abundance of phages in soil. Our estimates are based on the data available to us, which is mainly from [Williamson](http://dx.doi.org/10.1007/978-3-642-14512-4_4) and [Parikka et al.](http://dx.doi.org/10.1111/brv.12271). 
# 
# Based on these data, the values for the concentration of phages in soils appears to be ~$10^8-10^9$ phages per gram of soil. Assuming bulk soil density of ≈1.5 g cm$^3$, and soil depth of 10 meters (based on [Shangguan et al.](http://dx.doi.org/10.1002/2016MS000686)), we estimate the total number of phages per $m^2$ to be:

# In[2]:

# Lower and upper bounds for the concentration of phages per gram
lower_concentration = 1e8
upper_concentration = 1e9

# Typical bulk density of soil in g per cm^3
bulk_density = 1.5

# Total number of cm^3 in m^3
cm3_m3 = 1e6

# Soil depth in meters
depth = 10
# Calculate the total number of phages per m^2
lower_phage_per_m2 = lower_concentration*bulk_density*cm3_m3*depth
upper_phage_per_m2 = upper_concentration*bulk_density*cm3_m3*depth

print('The lower bound of the number of phages per m^2 of soil is ≈%.1e phages' %lower_phage_per_m2)
print('The upper bound of the number of phages per m^2 of soil is ≈%.1e phages' %upper_phage_per_m2)


# As our best estimate of the number of phages per $m^2$, we use the geometric mean of the lower and upper bounds. We apply this phage concentration across the entire ice-free land surface of the Earth, which is ≈$1.3×10^{14} m^2$ to estimate the total number of phages in soils:

# In[3]:

# Use the geometric mean of the lower and upper phage concentrations as our best estimate
best_phage_per_m2 = gmean([lower_phage_per_m2,upper_phage_per_m2])

# The area of ice-free land surface in m^2
area = 1.3e14

best_estimate = best_phage_per_m2*area

print('Our best estimate for the total number of phages in soils is ≈%.1e phages' % best_estimate)


# # Uncertainty analysis
# There are no good indicators for the uncerainty of our estimate of the total number of phages in soils. The range of ~$10^8-10^9$ phages per gram of soil introduces an uncertainty of about an order of magnitude. The specific values of the bulk density of soils, as well as the depth of soils also have uncertainty associated with them, which is hard to quantify. Our estimate is likely to be an overestimate, as it likely that the concentration of phages in deeper soil layers will be lower than in shallower layers, as is for prokaryotes.
# We thus project very crudely an uncertainty of one and a half orders of magnitude associated with our estimate of the number of phages in soils.
# 
# Our final parameters are:

# In[4]:

mul_CI = 10**1.5

print('Our best estimate for the total number of phages in soils: %.0e Gt C' % best_estimate)
print('Uncertainty associated with the estiamte of the total number of phages in soils: %.0f-fold' % mul_CI)

old_results = pd.read_excel('../phage_num_estimate.xlsx')
result = old_results.copy()
result.loc[2] = pd.Series({
                'Parameter': 'Total number of phages in soils',
                'Value': best_estimate,
                'Units': 'Number of individuals',
                'Uncertainty': mul_CI
                })

result.to_excel('../phage_num_estimate.xlsx',index=False)


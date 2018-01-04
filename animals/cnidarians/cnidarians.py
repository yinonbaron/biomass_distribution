
# coding: utf-8

# # Estimating the biomass of Cnidarians
# To estimate the total biomass of cnidarians, we combine estimates for two main groups which we assume dominate the biomass of cnidarains = planktonic cnidarians (i.e. jellyfish) and corals. We describe the procedure for estimating the biomass of each group
# 
# ## Planktonic cnidarians
# Our estimate of the total biomass of plaktonic cnidarians is based on [Lucas et al.](http://dx.doi.org/10.1111/geb.12169), which assembled a large dataset of abundance mauresments of different dypes of gelatinous zooplankton. Globally, they estimate ≈0.04 Gt C of gelatinous zooplankton, of which 92% are contributed by cnidarians. Therefore, we estimate the total biomass of planktonic cnidarians at ≈0.04 Gt C.
# 

# In[1]:


planktonic_cnidarian_biomass = 0.04e15


# ## Corals
# The procedure we take to estimate the total biomass of corals in coral reefs is to first calculate the total surface area of coral tissue globally, and then convert this value to biomass by the carbon mass density of coral tissue per unit surface area. We estimate the total surface area of corals worldwide using two approaches. 
# 
# The first approach estimates the total surface area of corals using the total area of coral reefs from [Harris et al.](http://dx.doi.org/10.1016/j.margeo.2014.01.011). 

# In[2]:


# Total surface area of coral reefs
coral_reef_area = 0.25e12


# We estimate that 20% of the reef area is covered by corals based on [De'ath et al.](http://dx.doi.org/10.1073/pnas.1208909109).

# In[3]:


# Coverage of coral reef area by corals
coverage = 0.2


# This gives us the projected area of corals. Corals have a complex 3D structure that increases their surface area. To take this effect into account, we use a recent study that estimated the ratio between coral tissue surface area and projected area at ≈5 ([Holmes & Glen](http://dx.doi.org/10.1016/j.jembe.2008.07.045)).

# In[4]:


# The conversion factor from projected surface area to actual surface area
sa_3d_2a = 5


# Multiplying these factors, we get an estimate for the total surface area of corals:

# In[5]:


# Calculate the total surface area of corals
method1_sa = coral_reef_area*coverage*sa_3d_2a

print('Our estimate of the global surface area of corals based on our first method is ≈%.1f×10^11 m^2' % (method1_sa/1e11))


# The second approach uses an estimate of the global calcification rate in coral reefs based on [Vecsei](http://dx.doi.org/10.1016/j.gloplacha.2003.12.002). 

# In[6]:


# Global annual calcufocation rate of  corals [g CaCO3 yr^-1]
annual_cal = 0.75e15


# We divide this rate by the surface area specific calcification rate of corals based on values from [McNeil](http://dx.doi.org/10.1029/2004GL021541) and [Kuffner et al.](http://dx.doi.org/10.1007/s00338-013-1047-8). Our best estimate for the surface area specific calcification rate is the geometric mean of values from the two sources above.

# In[7]:


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

# In[8]:


best_sa = gmean([method1_sa,method2_sa])
print('Our best estimate of the global surface area of corals is ≈%.1f×10^11 m^2' % (best_sa/1e11))


# To convert the total surface area to biomass, we use estimates for the tissue biomass per unit surface area of corals from [Odum & Odum](http://dx.doi.org/10.2307/1943285):

# In[9]:


# Tissue biomass based on Odum & Odum [g C m^-2]
carbon_per_sa = 400

# Multiply our best estimate for the surface area of corals by the tissue biomass
coral_biomass = best_sa*carbon_per_sa

print('Our best estimate for the biomass of corals is ≈%.2f Gt C' %(coral_biomass/1e15))


# An important caveat of this analysis is that it doesn’t include contribution of corals outside coral reefs, like those located in seamounts. Nevertheless, we account for this biomass of corals which are out of formal coral reefs when calculating the total benthic biomass.
# 
# Our best estimate of the total biomass of cnidarians is the sum of the biomass of planktonic cnidarians and corals:

# In[10]:


best_estiamte = planktonic_cnidarian_biomass + coral_biomass

print('Our best estimate for the biomass of cnidarians is ≈%.1f Gt C' %(best_estiamte/1e15))


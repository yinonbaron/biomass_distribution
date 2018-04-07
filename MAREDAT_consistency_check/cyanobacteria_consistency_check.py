
# coding: utf-8

# In[1]:

# Load dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean


# # Consistency check between the MAREDAT data and cyanobacteria abundance data
# We use a recent study by [Flombaum et al.](http://dx.doi.org/10.1073/pnas.1307701110) which estimated the total number of cyanobacteria worldwide. Flombaum et al. estimate ≈$3×10^{27}$ Prochlorococcus cells and ≈$7×10^{26}$ Synechococcus cells.
# 
# In order to estimate the total biomass of cyanobacteria, we use data from [Buitenhuis et al](https://ueaeprints.uea.ac.uk/40778/), to estimate the carbon content of Prochlorococcus and Synechococcus. Buitenhuis et al. reports values from the literature on the carbon content of Prochlorococcus and Synechococcus. We use the geometric mean of the estimates from different studies as our best estimate of the carbon content of Prochlorococcus and Synechococcus:

# In[2]:

# Load data from Buitenhuis et al.
carbon_content = pd.read_excel('cyanobacteria_data.xlsx',skiprows=1)

# Calculate the geometric mean of the carbon content of Prochlorococcus and Synechococcus
pro_cc = gmean(carbon_content['Prochlorococcus [fg C cell^-1]'].dropna())*1e-15
syn_cc = gmean(carbon_content['Synechococcus [fg C cell^-1]'].dropna())*1e-15


# We multiply the total number of cells of Prochlorococcus and Synechococcus by the carbon content of Prochlorococcus and Synechococcus to estimate their total biomass. The total biomass of cyanobacteria is the sum of the total biomass of Prochlorococcus and Synechococcus:

# In[3]:

# The total number of Prochlorococcus and Synechococcus from Flombaum et al.
pro_cell_num = 3e27
syn_cell_num = 7e26

# Calculate the total biomass of Prochlorococcus and Synechococcus
pro_tot_biomass = pro_cc*pro_cell_num
syn_tot_biomass = syn_cc*syn_cell_num

# Calculate the total biomass of cyanobacteria
cyano_biomass = pro_tot_biomass + syn_tot_biomass
print('The total biomass of cyanobacteria is ≈%.1f Gt C' %(cyano_biomass/1e15))


# We note in the section detailing our estimate of the total biomass of marine protists that the total biomass of picophytoplankton based on the MAREDAT database is ≈0.42 Gt C. Buithenhuis et al. estimate, based on data from the MAREDAT database, that cyanobacteria account for 31-51% out of the total biomass of picophytoplankton, which are equivalent to:

# In[4]:

# The estimate of the biomass of picophytoplankton based on MAREDAT data
picophyto_biomass = 0.42e15

# The fraction of cyanobacteria out of the total biomass of picophytoplankton based
# on MAREDAT data
cyano_fraction = [0.31,0.51]

# The estimate of the total biomass of cyanobacteria
cyano_maredat = picophyto_biomass*np.mean(cyano_fraction)
print('The estimate of the biomass of cyanobacteria based on the MAREDAT database is %.1f Gt C' %(cyano_maredat/1e15))


# The estimate based on the data from Flumbaum et al. and the estimate based on the MAREDAT database are less than 2-fold apart.

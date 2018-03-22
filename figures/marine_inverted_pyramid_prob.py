
# coding: utf-8

# In[1]:


# Load dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
import sys
sys.path.insert(0, '../statistics_helper/')
from CI_helper import *
from excel_utils import *


# # Quantifying the probability of the marine trophic pyramids being inverted
# In order to quantify the probability of consumer biomass in the marine environment being lrager than producer biomass, we randomly sample from the distribution of our estimates for the biomass of each taxon of producer of consumer biomass. For each taxon with no uncertainty estimate, we assume its uncertainty is an order of magnitude.
# 

# In[2]:


# Load results
results = pd.read_excel('../results.xlsx','Fig2B')

# Extract marine producers biomass data
marine_producers = results.iloc[20:25,0:3]
marine_producers.columns = results.iloc[19,0:3]

# Extract marine consumers biomass data
marine_consumers = results.iloc[20:30,3:]
marine_consumers.columns = results.iloc[19,0:3]


sample_size = 100000

# Define the funcion that samples from the distribution of biomass of each taxon for producers and consumers
def sample_biomass(estimates,sample_size):
    ans = np.empty([sample_size,estimates.shape[0]])
    for x,ind in enumerate(estimates.index):        
        ans[:,x:x+1] = np.random.lognormal(mean = np.log(estimates.loc[ind,'Biomass']), sigma = np.log(estimates.loc[ind,'Uncertainty'])/1.96,size=sample_size).reshape([-1,1])
    return ans.sum(axis=1)

# Sample from the distribution of estimates for each of the taxa of the producers and consumers
marine_consumer_sample = sample_biomass(marine_consumers,sample_size)
marine_producer_sample = sample_biomass(marine_producers,sample_size)

# Calculate the probability that marine consumers have larger biomass than marine producers
inverted_prob = (marine_consumer_sample>marine_producer_sample).sum()/sample_size

print('The probability marine consumers have larger biomass than marine producers is ≈%.0f' %(inverted_prob*100) + "%")


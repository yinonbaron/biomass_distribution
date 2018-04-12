
# coding: utf-8

# In[1]:


# Load dependencies
import pandas as pd
import numpy as np


# # Consistency check between the MAREDAT data and *Tara* Oceans data
# Our estimates of the global biomass of several marine taxa are based on data from the MAREDAT database. As stated in the specific sections relying on data from the database, there are many sources of uncertainty associated with the estimates stemming from the MAREDAT data. Many of those sources of uncertainty are hard to quantify, and no uncertainty estimate is provided in the literature on estimates based on the MAREDAT database.
# 
# Thus, we perform consistency checks for the MAREDAT data against independent sources of data, to increases our confidence in our estimates and to provide a measure of the uncertainty associated with our estimates.
# 
# In this document we conduct a comparison between the estimates of biomass based on the MAREDAT database and data from [de Vargas et al.](http://dx.doi.org/10.1126/science.1261605). the data in de Vargas et al. is based on 18S rDNA sequencing of different populations of plankton collected by the *Tara* Oceans campaign. 
# 
# The dataset in de Vargas et al. divides the plankton community based on size ranges (pico-nano-, nano-, micro- and meso-plankton). de Vargas et al. provides only number of reads for each taxon. The fraction of reads that a taxon has out of the total number of reads can be used as a proxy for the biomass fraction of the taxon, but not as a proxy of its absolute biomass. Relying on 18S rDNA sequence abundance as a proxy for biomass is not a well established practice, and has its own biases, but we chose to use it for the sake of comparing it to independent approaches such as the MAREDAT database. Each plankton size fraction sampled in the study was sequenced to approximately the same sequencing depth (≈120 million reads). This means that the 18S read data can provide a possible proxy for the biomass fraction of a certain taxon within a size fraction, but not across size fractions.
# 
# We focus on comparing the MAREDAT and de Vargas et al. data in two case studies: the biomass of diatoms and the total biomass of nanoplakton and microplankton.
# 
# ## Diatoms
# We begin by describing how to compare the biomass estimates of diatoms based on de Vargas et al. and the MAREDAT dataset. Our aim is to calculate the relative fraction of diatoms out of the total biomass of organisms in the same size range as diatoms. As the data in those two datasets is structured differently, we first need to make corrections to the data so a valid comparison will be available.
# 
# ### MAREDAT
# In de Vargas et al., diatoms appear mainly in the nanoplankton (5-20 µm in diameter) and microplankton (20-180 µm) size fractions. In order to make a comparison to the MAREDAT database we need to find the corresponding groups in the MAREDAT database. The corresponding groups in the MAREDAT database are the microzooplankton and the diatom groups (zooplankton between 5 and 200 µm in diameter). As calculated in the marine protists sections, our estimates for the respective biomass of microzooplankton and diatoms are ≈0.6 Gt C and ≈0.3 Gt C. Thus, according to the MAREDAT data diatoms account for about 30% of the total biomass of plankton in the 5-200 µm size fraction.
# 
# ### de Vargas et al.
# We use data on the total number of reads of different taxa in each size fraction. The data originates from de Vargas et al. from Database W6 in the companion website, as well as from Figure 3 in the main text. Here is a sample of the data:

# In[2]:


# Load data on the total number of reads of each taxon from de Vargas et al.
data = pd.read_excel('tara_oceans_data.xlsx','de Vargas W6',skiprows=1)
data.head()


# We also use data on the total number of reads from each size fraction from Figure 2 in de Vargas et al.:

# In[3]:


#Load data on the total number of reads in each size fraction
tot_reads = pd.read_excel('tara_oceans_data.xlsx','Total number of reads', skiprows=1)
tot_reads


# In de Vargas et al., diatoms appear mainly in the nanoplankton (5-20 µm in diameter) and microplankton (20-180 µm) size fractions. However, the microzooplankton biomass estimates in the MAREDAT database do not include copepods, which were moved to the mesozooplankton group. Fragile protists such as Rhizaria, are probably also undersampled in the MAREDAT database. Therefore, to correct for these effects such that we could compare the MAREDAT and Tara Oceans datasets, we remove metazoa (dominated by arthropods) and Rhizaria reads from the relevant size fractions in the Tara Oceans dataset (nano and microplakton):
# 

# In[4]:


# Calculate the total number of reads for the Nano and Micro fractions
read_data = pd.DataFrame()
read_data['Nano reads'] = data['Total # of reads']*data['Nano fraction']
read_data['Micro reads'] = data['Total # of reads']*data['Micro fraction']

# Subtract the total sum of rhizaria and metazoa from the total number of reads
corrected_total_reads = tot_reads[['Nano reads','Micro reads']] - read_data[data['Group'] == 'Metazoa'] - read_data[data['Rhizaria'] == True].sum()

print('The fraction of diatoms out of the total number of reads in nanoplankton and microplankton')
read_data.loc[1]/corrected_total_reads


# After correcting for those biases, the biomass fraction of diatoms in microplankton in the Tara Oceans dataset is between 16%-33%, which fits well with the estimate from the MAREDAT database of ≈30%.
# 
# ## Nanoplankton and Microplankton biomass
# In this section we generate an independent estimate of the total biomass of nanoplankton and microplankton, based on several data sources. We begin with the independently measured biomass of Rhizaria. The independent measurement using microscopy by  [Biard et al.](http://dx.doi.org/10.1038/nature17652) has estimated ≈0.2 Gt C of Rhizaria above 600 µm in diameter.
# 
# We assume that this biomass represents the biomass of Rhizaria in mesozooplankton. As we calculated in the marine arthropod section, Rhizaria represent ≈40% of the total mesoplankton biomass:

# In[5]:


# Load 18S sequecing data of mesozooplankton
seq_data = pd.read_excel('../animals/arthropods/marine_arthropods/marine_arthropods_data.xlsx',sheet_name='de Vargas',skiprows=1)

print('The average fraction of Rhizaria in 18S rDNA sequencing data in surface waters is ' + '{:,.0f}%'.format(seq_data['Rhizaria surface'].mean()*100))
print('The average fraction of Rhizaria in 18S rDNA sequencing data in the deep chlorophyll maximum is ' + '{:,.0f}%'.format(seq_data['Rhizaria DCM'].mean()*100))


# The remaining 60% are made up mainly of arthropods. This would put the total mesozooplankton arthropods biomass at ≈0.3 Gt C. Our estimate for the total biomass of arthropods in the nano, micro and mesozooplankton size fraction is ≈0.56 Gt C (see the marine arthropod section for details). Subtracting the fraction of As which leaves ≈0.2 Gt C of nano and microzooplankton arthropod biomass.

# In[6]:


# The estimate of the biomass of rhizaria based on Biard et al.
rhizaria_biomass = 0.2e15

# Calculate the average fraction of rhizaria out of the biomass
# of mesozooplankton
rhizaria_fraction = np.mean([seq_data['Rhizaria surface'].mean(),seq_data['Rhizaria DCM'].mean()])

# Calculate the biomass of mesozooplankton arthropods
meso_arth = rhizaria_biomass/(1-rhizaria_fraction)

# Our estimate for the total biomass of arthropods in nano
# micro and mezozooplankton size fractions
nano_micro_mezo_arthropod = 0.56e15

# Subtract the mesozooplankton arthropod biomass to estimate
# The nanozooplankton and microzooplankton arthropod biomass
nano_micro_arth = nano_micro_mezo_arthropod - meso_arth


# Based on the Tara Oceans data, the nano and microzooplankton arthropod biomass accounts for ≈40-75% of the total nano and microplankton biomass:

# In[7]:


print('The fraction of arthropods out of the total number of reads in nanoplankton and microplankton')
metazoa_frac = read_data[data['Group'] == 'Metazoa']/tot_reads[['Nano reads','Micro reads']]

print('The mean fraction of arthropods out of the total number of reads in nanoplankton and microplankton is ≈' + '{:,.0f}%'.format(float(metazoa_frac.mean(axis=1)*100)))


# We use the estimate we just calculated of ≈0.2 Gt C of arthropods in the nano and microplankton size fractions, and combine it with the estimate of the biomass fraction of arthropods in the nano and microplankton size fractions from the Tara Oceans dataset. This yields an estimate for the total nano and microplankton biomass which is about ≈0.4 Gt C:

# In[8]:


tot_nano_micro_biomass = nano_micro_arth/metazoa_frac.mean(axis=1)

print('The toal biomass of nano and microplankton we estimate is ≈%.1f Gt C' %(tot_nano_micro_biomass/1e15))


# As we stated in the section regarding the biomass of diatoms, the biomass of nano and microplankton is estimated at ≈1 Gt C based on the MAREDAT database, which is about 2-fold larger than the estimate we got based on combination of information from Biard et al. the Tara Oceans dataset and the MAREDAT database.


# coding: utf-8

# In[1]:

# Load dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean
import sys
sys.path.insert(0, '../../statistics_helper/')
from fraction_helper import *
from excel_utils import *


# # Estimating the biomass of marine protists
# Our estimate of the total biomass of marine protists relies on estimates of global biomass for many plankton groups. We included estimates of all plankton groups that are dominated by protists. The main groups with a significant biomass contribution were picoeukaryotes, microzooplankton (defined not to include copepod biomass), diatoms, *Phaeocystis* and Rhizaria. The estimates for all plankton groups except Rhizaria are based on [Buitenhuis et al.](http://search.proquest.com/openview/0e8e5672fa28111df473268e13f2f757/1?pq-origsite=gscholar&cbl=105729), which used data from the MAREDAT database. The protist group Rhizaria is under represented in the MAREDAT database, and thus our estimate for the total biomass of Rhizaria is based on *in situ* imaging work by [Biard et al.](http://dx.doi.org/10.1038/nature17652).
# 
# For the etimates based on MAREDAT data, Buitenhuis et al. estimates the total biomass of a specific plankton group by using a characteristic biomass concentration for each depth (either a median or average of the values in the database) and applying across the entire volume of ocean at that depth. Buitenhuis et al. generates two types of estimates are supplied for the global biomass of each plankton group: a “minimum” estimate which uses the median concentration of biomass from the database, and a “maximum” estimate which uses the average biomass concentration. Because the distributions of values in the database are usually highly skewed by asymmetrically high values the median and mean are loosely associated by the authors of the MAREDAT study with a minimum and maximum estimate. The estimate based on the average value is more susceptible to biases in oversampling singular locations such as blooms of plankton species, or of coastal areas in which biomass concentrations are especially high, which might lead to an overestimate. On the other hand, the estimate based on the median biomass concentration might underestimate global biomass as it will reduce the effect of biologically relevant high biomass concentrations. Therefore, here and in all estimates based on MAREDAT data, we take the geometric mean of the “minimum” and “maximum” estimates (actually median and mean values of the distribution) as our best estimate, which will increase our robustness to the effects discussed above. 
# 
# We now discuss the estimates for each of the groups of protists.
# 
# ## Picoeukaryotes
# We estimate the total biomass of picoeukaryotes by first estimating the total biomass of picophytoplankton, and then calculating the fraction of eukaryotes out of the total biomass of picophytoplankton. Buitenhuis et al. reports a "minimum" estimate of 0.28 Gt C and a "maximum" estimate of 0.64 Gt C for the biomass of picophytoplankton. We calculate the geometric mean of those estimates:

# In[2]:

# Calculate the geometric mean of the "minimum" and "maximum" estimates from Buitenhuis et al.
# for picophytoplankton
picophyto_biomsss = gmean([0.28e15,0.64e15])


# To estimate the fraction of eukaryotes out of the total biomass of picophytoplankton, we rely on [Buitenhuis et al.](https://ueaeprints.uea.ac.uk/40778/) which estimates that they represent 49-69% of the global biomass of picophytoplankton. We use the geometric mean of this range as our best estimate of the fraction eukaryotes out of the total biomass of picophytoplankton.

# In[3]:

euk_frac = frac_mean(np.array([0.49,0.69]))
auto_picoeuk_biomass = picophyto_biomsss*euk_frac


# Picoeukaryotes contain both protists and plant species (like chlorophytes). It seems that, from the available literature, the biomass distribution between them is not strongly favored towards one class ([Li et al.](http://dx.doi.org/10.1016/0198-0149(92)90085-8)). We thus estimate the protist fraction at about 50% of the biomass of picoeukaryotes:

# In[4]:

auto_pico_protists_fraction = 0.5
auto_pico_protists_biomass = auto_picoeuk_biomass*auto_pico_protists_fraction


# Protists in the picoplankton to nanoplankton size range (0.8-5 µm in diameter) include not only autotrophic, but also heterotrophic organisms. As we could not find a reliable resource for estimating the biomass of heterotrophic pico-nanoplankton we use a recent global 18S ribosomal DNA sequencing effort that was part of the Tara Oceans campaign ([de Vargas et al.](http://dx.doi.org/10.1126/science.1261605)). 
# 
# We extracted data from Fig. 5A in de Vargas et al., which quantifies the ratio between autotropic and heterotrophic picoplankton and nanoplankton:

# In[5]:

pd.options.display.float_format = '{:,.1f}'.format
# Load data from de Vargas on the ratio between autotrophic and heterotrophic protists
pico_nano_data = pd.read_excel('marine_protists_data.xlsx',skiprows=1)
pico_nano_data.head()


# We calculate the geometric mean of the fraction of phototrophic and heterotrophic protists out of the total amount of 18S rDNA sequences. We use the ratio between these geometric means as our best estimate for the ratio between photosynthetic and heterotrophic protists.

# In[6]:

hetero_photo_ratio = gmean(pico_nano_data['Heterotrophic protist'])/gmean(pico_nano_data['Phototrophic protists'])
print('Our best estimate of the ratio between heterotrophic and phototrophic protists in pico-nanoplankton is ≈%.f-fold' %hetero_photo_ratio)


# We add the contribution of heterotrophic pico-nanoprotists to our estimate:

# In[7]:

pico_protists_biomass = (1+hetero_photo_ratio)*auto_pico_protists_biomass


# Relying on 18S sequence abundance as a proxy for biomass is not a well established practice, and has various biases, but for lack of any other alternative we could find to perform the estimate, we chose to use it. Yet, we note that this plays a minor role in our analysis that in any case will not affect any of the major conclusions of our study.
# 
# ## Microzooplankton
# The estimate of microzooplankton in Buitenhuis et al. does not include copepod biomass by definition, and thus is suitable in order to estimate the total biomass of microzooplankton protists. Buitenhuis et al. reports a "minimum" estimate of 0.48 Gt C and a "maximum" estimate of 0.73 Gt C for the biomass of picophytoplankton. We calculate the geometric mean of those estimates:

# In[8]:

# Calculate the geometric mean of the "minimum" and "maximum" estimates from Buitenhuis et al.
# for microzooplankton
microzoo_biomsss = gmean([0.48e15,0.73e15])


# ## Diatoms
# For diatoms, Buitenhuis et al. reports a "minimum" estimate of 0.1 Gt C and a "maximum" estimate of 0.94 Gt C for the biomass of picophytoplankton. We calculate the geometric mean of those estimates:

# In[9]:

# Calculate the geometric mean of the "minimum" and "maximum" estimates from Buitenhuis et al.
# for diatoms
diatom_biomsss = gmean([0.1e15,0.94e15])


# ## Phaeocystis
# For Phaeocystis, reports a "minimum" estimate of 0.11 Gt C and a "maximum" estimate of 0.71 Gt C for the biomass of picophytoplankton. We calculate the geometric mean of those estimates:

# In[10]:

# Calculate the geometric mean of the "minimum" and "maximum" estimates from Buitenhuis et al.
# for Phaeocystis
phaeocystis_biomsss = gmean([0.11e15,0.71e15])


# As stated in Buitenhuis et al., the data from the MAREDAT initiative doesn’t contain the biomass of nanophytoplankton (phytoplankton between 2 and 20 µm) and autotrophic dinoflagellates. Nevertheless, this omission might be compensated by overestimation of Phaeocystis biomass because of sampling bias, so overall the sum of all the different phytoplankton fits well with total chlorophyll measurements from the WOA 2005.
# 
# ## Rhizaria
# For rhizaria, our estimate relies on data from Biard et al. Biard et al. divided the data into three depth layers (0-100 m, 100-200 m, and 200-500 m), and multiplied median biomass concentrations at each depth layer across the entire volume of water at that layer to generate global estimate. The biomass of Rhizaria in the top 500 meters of the ocean is estimated at ≈0.2 Gt C. 

# In[11]:

rhizaria_biomass = 0.2e15


# The estimates based on the MAREDAT database include measurements only for the top 200 meters of the water column. For rhizaria, our estimate includes the top 500 meters of the water column. For more details on possible contributions from deeper ocean laters, see the marine protists section in the Supplementary information.
# 
# ## Particle-atttached protists
# To estimate the total biomass of particle-attached protists, we estimate the ratio between the biomass of particle-attached protists and prokaryotes. We rely on three studies which have measured this ratio at both the epipelagic, mesopelagic and bathypelagic layers ([Bochdansky et al.](http://dx.doi.org/10.1038/ismej.2016.113), [Turley & Mackie](http://www.jstor.org/stable/24849742), [Herndl](http://www.jstor.org/stable/24827742)). We fist calculate the mean ratio between protists and prokaryotes in each study. 
# 
# ### Bochdansky et al.
# Bochdansky et al. provide a mean number of particle-attached eukaryotes normalized by the amount of particle-attached prokaryotes in the bathypelagic realm. They also measure the amount of fungi out of the toal population of eukaryotes. We remove the amount of fungal cells from the total number of eukaryotes:

# In[12]:

# Load the data from Bochdansky et al.
bochdansky_data = pd.read_excel('marine_protists_data.xlsx','Bochdansky ratio',skiprows=1,index_col=0)
protists = bochdansky_data.loc['All Eukaryotes'] - bochdansky_data.loc['Fungi']
print('The mean ratio between the number of particle-attached protists and prokaryotes reported in Bochdansky et al. is ≈%.3f' %protists)


# Our of the total number of eukaryotes, we exclude the group of *Labyrinthulomycetes*, as their biomass was estimated seperatly by Bochdansky et al., as we will see later. This leaves us with protists which are not *Labyrinthulomycetes*, mainly flagellates. To estimate the ratio of the biomass of these remaining protists, we rely on a study which has measured the carbon content of free-living protists in the deep sea ([Pernice et al.](https://dx.doi.org/10.1038%2Fismej.2014.168)). We use the carbon content of free-living protists in the deep sea as our best estimate of the carbon content of particle-attached protists in the deep-sea. For the carbon content of particle-attached prokaryotes, we use our best estimate from the particle-attached prokaryotes section.

# In[13]:

# Calculate the non-Labyrinthulomycetes protists
flagellates = protists-bochdansky_data.loc['Labyrinthulomycetes']

# Load data on the carbon content of flagellates from the deep-sea
flagellates_cc_data = pd.read_excel('marine_protists_data.xlsx','Pernice',skiprows=1,index_col=0)
deep_flagellates_cc = flagellates_cc_data.loc['1401-4000','Protist carbon content [pg C cell^-1]']

# Load our estimate of the carbon content of particle-attached prokaryotes
prok_cc = pd.read_excel('marine_protists_data.xlsx', 'POC prokaryotes').iloc[0,1]

# Calculate the ratio of biomass of non-Labyrinthulomycetes protists to prokaryotes
biomass_ratio_flagellates = flagellates*(deep_flagellates_cc*1000/prok_cc)


# Bochdansky et al. also provide estimates for the biomass ratio between particle-attached *Labyrinthulomycetes* and prokaryotes in the bathypelagic layer. They provide several estimates for the biomass ratio. We use the geometric mean of those estimates as our best estimate of the biomass ratio between particle-attached *Labyrinthulomycetes* and prokaryotes.

# In[14]:

# Load the data on the biomass ratio of Labyrinthulomycetes
lab_biomass_data = pd.read_excel('marine_protists_data.xlsx','Bochdansky biomass',skiprows=1)

# Calculate the geometric mean of the different estimates for the biomass ratio of
# Labyrinthulomycetes and prokaryotes
lab_biomass_ratio = gmean(gmean(lab_biomass_data.iloc[:,1:],axis=1))


# We sum our estimate for the biomass ratio of non-*Labyrinthulomycetes* and *Labyrinthulomycetes* particle-attached protists and prokaryotes as our best estimate from Bochdansky et al. of the biomass ratio between particle-attached protists and bacteria in the deep ocean:

# In[15]:

best_bochdansky = biomass_ratio_flagellates + lab_biomass_ratio

print('Our best estimate for the biomass ratio between particle-attached protists and prokaryotes in the bathypelagic layer is ≈%.1f ' %best_bochdansky)


# ### Herndl
# 
# For Turley & Mackie and Herndl, we have data on the concentrations of prokaryotes and protists on particles. For each study, we fist calculate the mean concentration of prokaryotes and protists, and divide the two mean concentrations to generate an estimate for the ratio between the number of cells of protists and prokaryotes. To estimate the mean concentrations of prokaryotes and protists, we generate two types of estimates: an estimate which uses the arithmetic mean of the different measurements, and an estimate which uses the geometric mean of the different measuremetns. The estimate based on the arithmetic mean is more susceptible to sampling bias, as even a single measurement which is not characteristic of the global population (such as samples which have some technical biases associated with them) might shift the average concentration significantly. On the other hand, the estimate based on the geometric mean might underestimate global biomass as it will reduce the effect of biologically relevant high population densities. As a compromise between these two caveats, we chose to use as our best estimate the geometric mean of the estimates from the two methodologies.

# In[16]:

# Load data from Turley & Mackie and Herndl
poc_ratio = pd.read_excel('marine_protists_data.xlsx','POC')

#  Calculate the arithmetic mean of the measurements in each study
arith_poc_mean_conc = poc_ratio.iloc[:,[1,2,3]].groupby('Reference').mean()

#  Calculate the geometric mean of the measurements in each study
geo_poc_mean_conc =poc_ratio.dropna().groupby('Reference').apply(lambda x: pd.Series(gmean(x.iloc[:,[1,2]])))
geo_poc_mean_conc.columns = poc_ratio.columns[1:3]

# Calculate the geometric mean between the mean estimate based on arithmetic and
# geometric means
best_mean_conc = np.sqrt(arith_poc_mean_conc*geo_poc_mean_conc)

# Calculate the ratio between the number of cells of protists and prokaryotes
best_ratio_conc = best_mean_conc['Concentration of Flagellates [cells mL^-1]']/best_mean_conc['Concentration of Bacteria [cells mL^-1]']
best_ratio_conc


# Herndl has measured the biovolume of protists and prokaryotes on particles, so we can generate an estimate for the carbon content ratio between protists and prokaryotes. For flagellates, Herndl has measured a mean volume of ≈11 $µm^3$, and he uses a conversion ratio between biovolume and carbon content of 220 fg C $µm^3$. He thus estimates flagellates will have a carbon content of 2.4 pg C cell$^{-1}$. 

# In[17]:

herndl_flagellates_vol = 11
herndl_flagellates_cc = herndl_flagellates_vol*0.22


# For prokaryotes, he measures a biovolume of ≈0.25 $µm^3$ for rod cells and 0.067 $µm^3$ for coccoid cells. We convert these volume to carbon content using the following coversion euqation from [Gundersen et al.](onlinelibrary.wiley.com/doi/10.4319/lo.2002.47.5.1525/abstract): $$ carbon\ content = 108.8×V^{0.898}$$

# In[18]:

rod_vol = 0.25
coccoid_vol = 0.067
conversion_eq = lambda x: 108.8*x**0.898
rod_cc = conversion_eq(rod_vol)
coccoid_cc = conversion_eq(coccoid_vol)


# From his experiments, it seems as if the relative fraction of rod and coccoid cells is similar, so we use the average of the carbon contents of rod cells and coccoid cells

# In[19]:

herndl_prok_cc = np.mean([rod_cc,coccoid_cc])


# We calculate the ratio in carbon contents between protists and prokaryotes as reported by Herndl, and multiply it by the ratio of the number of cells of protists and prokaryotes. This gives us an estimate for the ratio of the biomass of particle-attached protists and prokaryotes.

# In[20]:

herndl_cc_ratio = herndl_flagellates_cc*1000/herndl_prok_cc
herndl_biomass_ratio = best_ratio_conc.loc['Herndl']*herndl_cc_ratio
print('Our estimate for the ratio between the biomass of particle-attached protists and prokaryotes based on Herndl is ≈%.1f' %herndl_biomass_ratio)


# ### Turley & Mackie
# For Turley & Mackie, we only have measurements of the ratio between the number of cells of particle-attached protists and prokaryotes. Turkey & Mackie report measurements both in the epipelagic layer and in the mesopelagic layer. We calculate the mean concentrations of protists and prokaryotes in each layer. As we noted above we first calculate the arithmetic and geometric means of the measurements in each layer, and then use the geometric mean between the two values generate by using the arithmetric mean and geometric mean as our best estimate.

# In[21]:

# Take the data in Turley & Mackie
tm_data = poc_ratio[poc_ratio['Reference'] =='Turley & Mackie']

# Divide the data to data in the epipelagic and mesopelagic layers
tm_data['Epipelagic'] = tm_data['Depth [m]'] < 200

# Calculate the arithmetic mean of the measurements in each layer
arith_tm_mean_conc = tm_data.iloc[:,[1,2,6]].groupby('Epipelagic').mean()

# Calculate the geometric mean of the measurements in each layer
geo_tm_mean_conc =tm_data.dropna().groupby('Epipelagic').apply(lambda x: pd.Series(gmean(x.iloc[:,[1,2]])))
geo_tm_mean_conc.columns = tm_data.columns[1:3]

# Calculate the geometric mean between the mean estimate based on arithmetic and
# geometric means
best_tm_mean_conc = np.sqrt(arith_tm_mean_conc*geo_tm_mean_conc)

# Calculate the ratio between the number of cells of protists and prokaryotes
best_tm_ratio_conc = best_tm_mean_conc['Concentration of Flagellates [cells mL^-1]']/best_tm_mean_conc['Concentration of Bacteria [cells mL^-1]']
pd.options.display.float_format = '{:,.3f}'.format
best_tm_ratio_conc


# To estimate the ratio between the biomass of particle-attached protists and prokaryotes based on the ratios of cell concentrations in Turley & Mackie, we need to estimate the ratios in the carbon contents of particle-attached protists and prokaryotes. For the sampled collected in the epipelagic layer, we use the data measured in Herndl, which was also measured in the epipelagic layer. For the mesopelagic layer, we use data from Pernice et al. measured in the mesopelagic layer.

# In[22]:

pd.options.display.float_format = '{:,.1f}'.format
# For the epipelagic layer multiply cell concentration ratios by the carbon
# content ratios measured by Herndl
epi_tm_biomass = best_tm_ratio_conc.loc[True]*herndl_cc_ratio

# For the mesopelagic layer, calculate the mean carbon content of protists
# From data in Pernice et al.
meso_protist_cc = np.average(flagellates_cc_data['Protist carbon content [pg C cell^-1]'],weights=[250,250,700,0])

# Calculate the ratio of carbon content in the mesopelagic layer using
# our best estiamte for the carbon content of particle-attached prokaryotes 
meso_cc_ratio = meso_protist_cc*1000/prok_cc

# Calculate the biomass ratio between particle-attached protists and
# prokaryotes in the mesopelagic layer
meso_biomass_ratio = best_tm_ratio_conc.loc[False]*meso_cc_ratio


# ## Estimating the biomass ratio of particle-attached protists and prokaryotes
# We integrate the estimates from the three different studies in the following manner: We estimate a biomass ratio between particle-attached protists and bacteria in each layer of the ocean - the epipelagic, mesopelagic and bathypelagic layers. For the epipelagic layer, we use the geometric mean of the estimates based on Herndl and Turley & Mackie. For the mesopelagic layer we use the estimates by Turley & Mackie, and for the bathypelagic layer we use the estimates by Bochdansky et al.

# In[23]:

best_biomass_ratio = np.average([gmean([herndl_biomass_ratio,epi_tm_biomass]),meso_biomass_ratio,best_bochdansky], weights=[200,800,3000])
print('Our best estimate for the biomass ratio between particle-attached protists and prokaryotes is ≈%.1f' %best_biomass_ratio)


# We use our best estimate for the total biomass of particle attached prokaryotes and multiply it by our estimate of the biomass ratio between particle-attached protists and prokaryotes to estimate the total biomass of particle-attached protists.

# In[24]:

poc_prok = pd.read_excel('../../bacteria_archaea/marine/marine_prok_biomass_estimate.xlsx').loc[[0,1,4],'Value'].prod()*1e-15

best_poc_protists = poc_prok*best_biomass_ratio

print('Our best estimate for the total biomass of particle-attached protists is ≈%.1f Gt C' %(best_poc_protists/1e15))


# ## Estimating the total biomass of protists
# To estimate the total biomass of marine protists, we sum up all of our estimates of the biomass of the different groups of protists:

# In[25]:

best_estimate = rhizaria_biomass + phaeocystis_biomsss + diatom_biomsss + microzoo_biomsss + pico_protists_biomass + best_poc_protists

print('Our best estimate for the total biomass of marine protists is ≈%.1f Gt C' %(best_estimate/1e15))


# 
# 
# # Uncertanity analysis
# We discuss the uncertainty of estimates based on the MAREDAT database in a dedicated section in the Supplementary Information. We crudly project an uncertainty of about an order of magnitude. We project the same uncertainty for the biomass of particle-attached protists.

# In[26]:

# We crudely estimate and uncertainty of an order of magnitude
mul_CI = 10


# Our final parameters are:

# In[27]:


print('Biomass of marine protists: %.1f Gt C' %(best_estimate/1e15))
print('Uncertainty associated with the estimate of the total biomass of marine protists: ≈%.0f-fold' % mul_CI)


old_results = pd.read_excel('../protists_biomass_estimate.xlsx')
result = old_results.copy()


if (result.shape[0]==0):
    result = pd.DataFrame(index= range(1), columns=['Parameter','Value','Units','Uncertainty'])

result.loc[1] = pd.Series({
                'Parameter': 'Biomass of marine protists',
                'Value': float(best_estimate)/1e15,
                'Units': 'Gt C',
                'Uncertainty': mul_CI
                })

result.loc[2] = pd.Series({
                'Parameter': 'Biomass of pico-nanoprotists',
                'Value': float(pico_protists_biomass)/1e15,
                'Units': 'Gt C',
                'Uncertainty': None
                })

result.to_excel('../protists_biomass_estimate.xlsx',index=False)


# Feed results to Fig. 2C

# Feed green algae picophytoplankton biomass
update_fig2c(row=23,col=1,values=auto_picoeuk_biomass*(1-auto_pico_protists_fraction)/1e15, path='../../results.xlsx')


# Feed bacterial picophytoplankton biomass
update_fig2c(row=24,col=1,values=picophyto_biomsss*(1-euk_frac)/1e15, path='../../results.xlsx')


# Feed protist picophytoplankton biomass
update_fig2c(row=25,col=1,values=auto_picoeuk_biomass*auto_pico_protists_fraction/1e15, path='../../results.xlsx')

# Feed diatom biomass
update_fig2c(row=26,col=1,values=diatom_biomsss/1e15, path='../../results.xlsx')

# Feed Phaeocystis biomass
update_fig2c(row=27,col=1,values=phaeocystis_biomsss/1e15, path='../../results.xlsx')


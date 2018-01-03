
# coding: utf-8

# # Estimating the biomass of livestock
# To estimate the biomass of livestock, we rely on data on global stocks of cattle, sheep goats, and pigs fro the Food and Agriculture Organization database FAOStat. We downloaded data from the domain Production/Live animals.
# We combined data on the total stocks of each animal with estimates of the mean mass of each type of animal species from [Dong et al.](http://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_10_Ch10_Livestock.pdf), Annex 10A.2, Tables 10A-4 to 10A-9.
# 
# Here are samples of the data:

# In[8]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load global stocks data
stocks = pd.read_excel('livestock_stocks.xlsx')
stocks.head()


# In[9]:


# Load species body mass data
body_mass = pd.read_excel('livestock_body_mass.xlsx',skiprows=1) 
body_mass.head()


# The body weight of each aminal is dependent on the continent from which it arrives and the use type (Cattle - dairy and non-dairy. We therefore calculate the total number of animals in each category and multiply the total number of animals in each caterogy by the body mass.
# 
# We first standardize the data in terms of units, region definitions and animal categories:

# In[10]:


# Define transformation between the regions reported in FAOStat and IPCC
region_mappings_subcat =  {'Africa': 'Africa + (Total)',
                    'Eastern Europe':' --Eastern Europe + (Total)',
                    'Western Europe': ' --Western Europe + (Total)',
                    'Oceania':'Oceania + (Total)',
                    'Northern America': ' --Northern America + (Total)',
                    'Latin America': 'Americas + (Total)',
                    'Indian Subcontinent': ' --Southern Asia + (Total)',
                    'Asia': 'Asia + (Total)',
                    #'Middle east': ''
                    }

region_mappings_numbers =  {'Africa': 'Africa',
                    'Eastern Europe':'Eastern Europe',
                    'Western Europe': 'Western Europe',
                    'Oceania':'Oceania',
                    'Northern America': 'Northern America',
                    'Latin America': 'Americas',
                    'Indian Subcontinent': 'Southern Asia',
                    'Asia': 'Asia',
                    #'Middle east': ''
                    }
region_mappings_numbers_reverse = dict ( (v,k) for k, v in region_mappings_numbers.items() )
region_mappings_subcat_reverse= dict ( (v,k) for k, v in region_mappings_subcat.items() )

# Define the animal categories in the body mass data and in the final data
animal_categories_mass = ['Asses','Buffaloes','Camelids, other','Camels','Cattle - dairy','Cattle - non-dairy','Chickens - Broilers','Chickens - Layers','Ducks','Goats','Horses','Mules','Swine - market','Swine - breeding','Sheep','Turkeys']
animal_categories_final = ['Asses','Buffaloes','Camelids, other','Camels','Cattle','Chickens','Ducks','Goats','Horses','Mules','Pigs','Sheep','Turkeys']

# Standardize units - change places in which units are reported in 1000s to standard units.
stocks.loc[stocks['Unit'] == '1000 Head', 'Value'] *=1000



# To calculate the number of laying and non-laying poulry and number of dairy and non-dairy cattle, we load data from the FAOStat. We preprocess it so we could merge it with the stocks data.

# In[13]:


# Load data on the number of egg laying poultry and dairy producing cattle
subcategories = pd.read_excel('dairy_egg_global_data.xlsx',index_col=0)

subcategories.loc[region_mappings_subcat.values()] 
# Filter only the countries which are continents (region mappings subcat)
filtered_subcat = subcategories.loc[region_mappings_subcat.values()] 

# Calculte the total number of egg laying and non-laying poultry
# Filter only egg layers, remove 5 first colomns and reset index
chicken_cat = 1000*filtered_subcat[filtered_subcat['element'] == 'Laying (1000 Head)'][filtered_subcat.columns[5:]].reset_index()

# Melt the pivot by country
chicken_melt = pd.melt(chicken_cat,id_vars=['countries'],value_vars=[x for x in chicken_cat.columns[1:]])

# Remove a row called Unnamed: 58
chicken_melt = chicken_melt.loc[chicken_melt['variable']!='Unnamed: 58']

# Change variable type to int
chicken_melt['variable'] = chicken_melt['variable'].astype('int') 

# Change the names of the regions to standard regions
chicken_melt = chicken_melt.replace({'countries':region_mappings_subcat_reverse}) 

# Change the name of the columns
chicken_melt.columns = ['Country','Year','Chickens - Layers'] 


# Cattle 
# Filter only dairy producers, remove 5 first colomns and reset index
dairy_cat = filtered_subcat[filtered_subcat['element'] == 'Milk Animals (Head)'][filtered_subcat.columns[5:]].reset_index() 

# Melt the pivot by country
dairy_melt = pd.melt(dairy_cat,id_vars=['countries'],value_vars=[x for x in dairy_cat.columns[1:]])

# Remove a row called Unnamed: 58
dairy_melt = dairy_melt.loc[dairy_melt['variable']!='Unnamed: 58'] 

# Change variable type to int
dairy_melt['variable'] = dairy_melt['variable'].astype('int') 

# Change the names of the regions to standard regions
dairy_melt = dairy_melt.replace({'countries':region_mappings_subcat_reverse}) 

# Change the name of the columns
dairy_melt.columns = ['Country','Year','Cattle - dairy'] 

world_data = stocks[stocks['Country'] == 'World']


# We preprocess the stocks DataFrame and merge it with the dairy data:

# In[15]:


# Preprocessing the stocks DataFrame

# Only use the region data, and only the columns country, item, year and value
region_data = stocks[stocks['Country'].isin(region_mappings_numbers.values())][['Country','Item','Year','Value']] 

# Only use the animal types we consider here 
region_data = region_data[region_data['Item'].isin(animal_categories_final)] 

# Pivot table by animal type
region_data_piv = pd.pivot_table(region_data,values='Value',index=['Country','Year'],columns='Item') 

# Reset the index of the DataFrame
region_data_piv = region_data_piv.reset_index() 

# Replace Southern Asia region to Indian Subcontinent 
region_data_piv = region_data_piv.replace({'Country':{'Southern Asia':'Indian Subcontinent'}}) 
# Replace Americas region to Latin America
region_data_piv = region_data_piv.replace({'Country':{'Americas':'Latin America'}}) 

# Merge total abundance and egg and dairy data
# Merge egg-layers data
merged_data = pd.merge(region_data_piv,chicken_melt,how='left',on=['Country','Year']) 
# Merge dairy data
merged_data = pd.merge(merged_data,dairy_melt,how='left',on=['Country','Year'])

## Replace the data for Asia with the data from Asia minus Southern Asia
# Extract the data for Total Asia
asia = merged_data.loc[merged_data.Country == 'Asia'].reset_index() 

# Extract the data for only India
india = merged_data.loc[merged_data.Country == 'Indian Subcontinent'].reset_index() 

# Replace the data for Asia with the data for Asia minus India
merged_data.loc[merged_data.Country == 'Asia',asia.columns[3:]] = np.nan_to_num(asia[asia.columns[3:]].values)-np.nan_to_num(india[india.columns[3:]].values) 

## Replace the data for Americas with the data from Americas minus Northern America
# Extract the data for total Americas
americas = merged_data.loc[merged_data.Country == 'Latin America'].reset_index() 

# Extract the data for only Northen America
north_america = merged_data.loc[merged_data.Country == 'Northern America'].reset_index() #extract north america

# Replace the data in Americas with the data for Americas minus Northern America
merged_data.loc[merged_data.Country == 'Latin America',americas.columns[3:]] = np.nan_to_num(americas[americas.columns[3:]].values)-np.nan_to_num(north_america[north_america.columns[3:]].values) 

## Replace the data for Cattle with the data for Cattle minus the data for "Cattle - non-dairy"
cattle = merged_data['Cattle']
merged_data['Cattle'] = cattle.values- merged_data['Cattle - dairy'].values

## Replace the data for Chickens with the data for Chickens minus the data for "Chickens - Broilers"
merged_data['Chickens'] = merged_data['Chickens'].values- merged_data['Chickens - Layers'].values


# We now multiply the stocks of each animal type and for each region:

# In[25]:


# Copy the stocks data to the new mass DataFrame
mass_data = merged_data[merged_data.columns[:-2]].copy()

# For each animal type and for each region, multiply the stocks data by the characteristic body mass of the animal
for animal in animal_categories_final:
    for region in body_mass.index:
        if animal == 'Cattle':
            mass_data.loc[mass_data.Country == region,animal] = merged_data.loc[merged_data.Country == region]['Cattle']*body_mass.loc[region]['Cattle - non-dairy'] + merged_data.loc[merged_data.Country == region]['Cattle - dairy']*body_mass.loc[region]['Cattle - dairy']
        elif animal == 'Chickens':
            mass_data.loc[mass_data.Country == region,animal] = merged_data.loc[merged_data.Country == region]['Chickens']*body_mass.loc[region]['Chicken - Broilers'] + merged_data.loc[merged_data.Country == region]['Chickens - Layers']*body_mass.loc[region]['Chicken - Layers']
        elif animal == 'Pigs':
            # Assuming 10% of the pig population are for breeding
            mass_data.loc[mass_data.Country == region,animal] = merged_data.loc[merged_data.Country == region]['Pigs']*(0.9*body_mass.loc[region]['Swine - market'] + 0.1*body_mass.loc[region]['Swine - breeding'])
        elif animal == 'Camelids, other':
            mass_data.loc[mass_data.Country == region,animal] = merged_data.loc[merged_data.Country == region][animal]*body_mass.loc[region]['Llamas']
        else:
            mass_data.loc[mass_data.Country == region,animal] = merged_data.loc[merged_data.Country == region][animal]*body_mass.loc[region][animal]

# Sum over all regions to get total mass of each animals at each year
total_mass = mass_data.groupby(['Year']).sum()

#Remove year after 2012 as no all data is available for them
total_mass = total_mass.loc[total_mass.index<2012]

# Generate summaries for each animal category
mass_sum = total_mass[['Cattle','Chickens']].copy()
mass_sum['Cattle'] = total_mass['Cattle'] + total_mass['Buffaloes']
mass_sum['Chickens'] = total_mass.sum(axis=1) - mass_sum['Cattle']
mass_sum.columns = ['Cattle','Other Livestock']

carbon_content = 0.15
print(mass_sum*carbon_content*1000)


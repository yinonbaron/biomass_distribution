
# Estimating the fraction of marine archaea out of the total marine prokaryote population

In order to estimate the fraction of archaea out of the total population of marine bacteria and archaea, we rely of two independent methods: fluorescent in-situ hybridization (FISH) and 16S rDNA sequencing. For each one of the methods, we calculate the fraction of archaea out of the total population of marine bacteria and archaea in the three depth layers of the ocean - the epieplagic (< 200 meters depth), the mesopelagic (200-1000 meters depth) and bathypelagic (1000-4000 meters depth).

### FISH based estimate
For our FISH based estimate we rely on data from [Lloyd et al.](http://dx.doi.org/10.1128/AEM.02090-13). Here is a sample of the data:


```python
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '../../../statistics_helper')
from fraction_helper import *
pd.options.display.float_format = '{:,.1e}'.format
# Genaral parameters used in the estimate
ocean_area = 3.6e14
liters_in_m3 = 1e3
ml_in_m3 = 1e6

# Load the dataset
lloyd = pd.read_excel('marine_arch_frac_data.xlsx','Lloyd')
lloyd.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>paper</th>
      <th>Sample</th>
      <th>Water Depth (m)</th>
      <th>Cells per cc</th>
      <th>CARDFISH Bac per cc</th>
      <th>CARDFISH Arc per cc</th>
      <th>CARDFISH Total per cc</th>
      <th>FISH yield</th>
      <th>Fraction Arc CARDFISH</th>
      <th>Fish or cardFish</th>
      <th>...</th>
      <th>Fixative</th>
      <th>Bac permeabilization</th>
      <th>Arc permeabilization</th>
      <th>Bac probe</th>
      <th>Arc probe</th>
      <th>Counting method</th>
      <th>qPCR-Bacteria (copies/mL water)</th>
      <th>qPCR-Archaea (copies/mL water)</th>
      <th>qPCR-MCG (copies/mL water)</th>
      <th>Total qPCR(copies/mL water)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Al Ali 2009</td>
      <td>La Seyne-sur-Mer, French Mediterranean coast</td>
      <td>2.5e+01</td>
      <td>1.0e+06</td>
      <td>7.5e+05</td>
      <td>9.2e+04</td>
      <td>8.4e+05</td>
      <td>8.3e-01</td>
      <td>1.1e-01</td>
      <td>CARDFISH</td>
      <td>...</td>
      <td>formaldehyde</td>
      <td>lysozyme/achromopeptidase</td>
      <td>proteinase K</td>
      <td>EUB338</td>
      <td>ARCH915</td>
      <td>Microscope-eye</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Al Ali 2009</td>
      <td>La Seyne-sur-Mer, French Mediterranean coast</td>
      <td>1.0e+02</td>
      <td>7.1e+05</td>
      <td>4.3e+05</td>
      <td>1.1e+05</td>
      <td>5.5e+05</td>
      <td>7.8e-01</td>
      <td>2.1e-01</td>
      <td>CARDFISH</td>
      <td>...</td>
      <td>formaldehyde</td>
      <td>lysozyme/achromopeptidase</td>
      <td>proteinase K</td>
      <td>EUB338</td>
      <td>ARCH915</td>
      <td>Microscope-eye</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Al Ali 2009</td>
      <td>La Seyne-sur-Mer, French Mediterranean coast</td>
      <td>5.0e+02</td>
      <td>1.0e+05</td>
      <td>5.3e+04</td>
      <td>2.8e+04</td>
      <td>8.1e+04</td>
      <td>7.9e-01</td>
      <td>3.4e-01</td>
      <td>CARDFISH</td>
      <td>...</td>
      <td>formaldehyde</td>
      <td>lysozyme/achromopeptidase</td>
      <td>proteinase K</td>
      <td>EUB338</td>
      <td>ARCH915</td>
      <td>Microscope-eye</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Al Ali 2009</td>
      <td>La Seyne-sur-Mer, French Mediterranean coast</td>
      <td>1.0e+03</td>
      <td>6.9e+04</td>
      <td>3.3e+04</td>
      <td>2.1e+04</td>
      <td>5.4e+04</td>
      <td>7.8e-01</td>
      <td>3.9e-01</td>
      <td>CARDFISH</td>
      <td>...</td>
      <td>formaldehyde</td>
      <td>lysozyme/achromopeptidase</td>
      <td>proteinase K</td>
      <td>EUB338</td>
      <td>ARCH915</td>
      <td>Microscope-eye</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Al Ali 2009</td>
      <td>La Seyne-sur-Mer, French Mediterranean coast</td>
      <td>1.8e+03</td>
      <td>6.4e+04</td>
      <td>2.6e+04</td>
      <td>2.0e+04</td>
      <td>4.7e+04</td>
      <td>7.3e-01</td>
      <td>4.4e-01</td>
      <td>CARDFISH</td>
      <td>...</td>
      <td>formaldehyde</td>
      <td>lysozyme/achromopeptidase</td>
      <td>proteinase K</td>
      <td>EUB338</td>
      <td>ARCH915</td>
      <td>Microscope-eye</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 21 columns</p>
</div>



The data in Lloyd et al. contains estimates for the number of bacteria and archaea. Lloyd et al. generated regression equations for the concentration of bacteria and archaea as a function of depth. We use these equations to estimate the total number of archaea and bacteria at each of the three depth layers.


```python
# Define the regression equation for the number of bacteria in the top 64 m:
def bac_surf(depth):
    result = np.zeros_like(depth)
    for i,x in enumerate(depth):
        if x==0 :
            result[i] = 5.54
            
        else:
            result[i] = np.log10(x)*0.08+5.54
    return 10**result

# Define the regression equation for the number of bacteria in water deeper than 64 m:
bac_deep = lambda x: 10**(np.log10(x)*-1.09+7.66)

# Define the regression equation for the number of archaea in the top 389 m:
def arch_surf(depth):
    result = np.zeros_like(depth)
    for i,x in enumerate(depth):
        if x==0 :
            result[i] = 4.1
            
        else:
            result[i] = np.log10(x)*0.1+4.1
    return 10**result

# Define the regression equation for the number of bacteria in water below 389 m:
arch_deep = lambda x: 10**(np.log10(x)*-0.8+6.43)

# Estimate the total number of bacteria and archaea in the epipelagic layer by first estimating the concentration using the 
# regression equation, multiplying by the volume at each depth, which is 1 m^3 times the surface
# Area of the ocean, and finally summing across different depths
total_bac_epi = (bac_surf(np.linspace(0,64,65))*ml_in_m3*ocean_area).sum() + (bac_deep(np.linspace(65,200,200-65+1))*ml_in_m3*ocean_area).sum()
total_arch_epi = (arch_surf(np.linspace(0,200,201))*ml_in_m3*ocean_area).sum()

# Calculate the fraction of archaea in the epipelagic layer
FISH_arch_frac_epi = total_arch_epi/(total_arch_epi+total_bac_epi)


# We repeat the same procedure for the total number of bacteria and archaea in the mesopelagic layer
# Number of archaea
total_bac_meso = (bac_deep(np.linspace(201,1000,1000-200+1))*ml_in_m3*ocean_area).sum()
total_arch_meso = (arch_surf(np.linspace(201,389,390-201+1))*ml_in_m3*ocean_area).sum() + (arch_deep(np.linspace(390,1000,1000-390+1))*ml_in_m3*ocean_area).sum()

# Calculate the fraction of archaea in the mesopelagic layer
FISH_arch_frac_meso = total_arch_meso/(total_arch_meso+total_bac_meso)

# We repeat the same procedure for the total number of bacteria and archaea in the mesopelagic layer
# Number of archaea
total_bac_bathy = (bac_deep(np.linspace(1001,4000,4000-1001+1))*ml_in_m3*ocean_area).sum()
total_arch_bathy = (arch_deep(np.linspace(1001,4000,4000-1001+1))*ml_in_m3*ocean_area).sum()

# Calculate the fraction of archaea in the bathypelagic layer
FISH_arch_frac_bathy = total_arch_bathy/(total_arch_bathy+total_bac_bathy)

print('The fraction of archaea in the epipelagic layer based on FISH is %.1f percent' % (FISH_arch_frac_epi*100))
print('The fraction of archaea in the mesopelagic layer based on FISH is %.1f percent' % (FISH_arch_frac_meso*100))
print('The fraction of archaea in the bathypelagic layer based on FISH is %.1f percent' % (FISH_arch_frac_bathy*100))
```

    The fraction of archaea in the epipelagic layer based on FISH is 5.8 percent
    The fraction of archaea in the mesopelagic layer based on FISH is 24.0 percent
    The fraction of archaea in the bathypelagic layer based on FISH is 34.9 percent


### 16S rDNA sequencing

To estimate the fraction of archaea out of the total population of marine bacteria and archaea, we rely on data from [Sunagawa et al.](http://science.sciencemag.org/content/348/6237/1261359) for the epipelagic and mesopelagic layers, and data from [Salazar et al.](http://dx.doi.org/10.1038/ismej.2015.137) for the bathypelagic layer.


```python
sunagawa = pd.read_excel('marine_arch_frac_data.xlsx','Sunagawa')
salazar = pd.read_excel('marine_arch_frac_data.xlsx','Salazar')
```

Here are samples from the data in Sunagawa et al.:


```python
sunagawa.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Thaumarcheota</th>
      <th>Euryarchaeota</th>
      <th>Remarks</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>SRF</th>
      <td>6.2e-01</td>
      <td>2.7e+00</td>
      <td>Data extracted from figure 2 of Sunagawa et al.</td>
    </tr>
    <tr>
      <th>DCM</th>
      <td>1.4e+00</td>
      <td>4.1e+00</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>MESO</th>
      <td>1.1e+01</td>
      <td>2.9e+00</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



Here are samples from the data in Salazar et al.:


```python
salazar.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sample</th>
      <th>station</th>
      <th>filtersize</th>
      <th>Date</th>
      <th>Ocean</th>
      <th>code</th>
      <th>Depth</th>
      <th>Longitude</th>
      <th>Latitude</th>
      <th>Unnamed: 9</th>
      <th>Unnamed: 10</th>
      <th>Archaea</th>
      <th>Bacteria</th>
      <th>No blast hit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>MP0145</td>
      <td>10</td>
      <td>2.0e-01</td>
      <td>2010-12-26</td>
      <td>North Atlantic</td>
      <td>MP0145</td>
      <td>-4002</td>
      <td>-2.6e+01</td>
      <td>1.5e+01</td>
      <td>nan</td>
      <td>MP0145</td>
      <td>3.1e-01</td>
      <td>6.9e-01</td>
      <td>9.4e-05</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MP0262</td>
      <td>17</td>
      <td>2.0e-01</td>
      <td>2011-01-02</td>
      <td>South Atlantic</td>
      <td>MP0262</td>
      <td>-4002</td>
      <td>-2.7e+01</td>
      <td>-3.0e+00</td>
      <td>nan</td>
      <td>MP0262</td>
      <td>1.9e-01</td>
      <td>8.1e-01</td>
      <td>0.0e+00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MP0327</td>
      <td>20</td>
      <td>2.0e-01</td>
      <td>2011-01-05</td>
      <td>South Atlantic</td>
      <td>MP0327</td>
      <td>-4001</td>
      <td>-3.0e+01</td>
      <td>-9.1e+00</td>
      <td>nan</td>
      <td>MP0327</td>
      <td>1.7e-01</td>
      <td>8.3e-01</td>
      <td>0.0e+00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MP0372</td>
      <td>23</td>
      <td>2.0e-01</td>
      <td>2011-01-08</td>
      <td>South Atlantic</td>
      <td>MP0372</td>
      <td>-4003</td>
      <td>-3.3e+01</td>
      <td>-1.6e+01</td>
      <td>nan</td>
      <td>MP0372</td>
      <td>1.4e-01</td>
      <td>8.6e-01</td>
      <td>9.4e-05</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MP0441</td>
      <td>26</td>
      <td>2.0e-01</td>
      <td>2011-01-11</td>
      <td>South Atlantic</td>
      <td>MP0441</td>
      <td>-3907</td>
      <td>-3.7e+01</td>
      <td>-2.3e+01</td>
      <td>nan</td>
      <td>MP0441</td>
      <td>1.2e-01</td>
      <td>8.8e-01</td>
      <td>0.0e+00</td>
    </tr>
  </tbody>
</table>
</div>



As we are working with fractions here, we shall use a utility that will calculate mean and uncertainty of fractions. For details regarding the procedure look at the documentation of the relevant functions.
For the epipelagic layer, we will use the sum of the fractions of Thaumarcheota and Euryarchaeota, two main archaeal phyla. We will use the geometric mean of the fractions in surface waters and the deep chlorophyll maximum.


```python
sunagawa_sum = (sunagawa['Thaumarcheota'] + sunagawa['Euryarchaeota'])/100
seq_arch_frac_epi = frac_mean(sunagawa_sum.loc[['DCM','SRF']])
seq_arch_frac_meso = frac_mean(sunagawa_sum.loc['MESO'])
print('The fraction of archaea in the epipelagic layer based on 16S rDNA sequencing is %.1f percent' % (seq_arch_frac_epi*100))
print('The fraction of archaea in the mesopelagic layer based on 16S rDNA sequencing is %.1f percent' % (seq_arch_frac_meso*100))
```

    The fraction of archaea in the epipelagic layer based on 16S rDNA sequencing is 4.3 percent
    The fraction of archaea in the mesopelagic layer based on 16S rDNA sequencing is 14.4 percent


For the bathypelagic layer, we estimate the fraction of archaea based on 16S rDNA sequencing by using the geometric mean of the data in Salazar et al.


```python
seq_arch_frac_bathy = frac_mean(salazar['Archaea'])
print('The fraction of archaea in the bathypelagic layer based on 16S rDNA sequencing is %.1f percent' % (seq_arch_frac_bathy*100))
```

    The fraction of archaea in the bathypelagic layer based on 16S rDNA sequencing is 15.0 percent


Our best estimate for the fraction of archaea out of the total population of marine bacteria and archaea at each layer is the geometric mean of the estimates of the fraction of archaea based on FISH and on 16S rDNA sequencing, corrected for the lower rDNA operon copy number


```python
best_arch_frac_epi = frac_mean(np.array([FISH_arch_frac_epi,seq_arch_frac_epi*2]))
best_arch_frac_meso = frac_mean(np.array([FISH_arch_frac_meso,seq_arch_frac_meso*2]))
best_arch_frac_bathy = frac_mean(np.array([FISH_arch_frac_bathy,seq_arch_frac_bathy*2]))
print('The best estimate for the fraction of archaea in the epipelagic layer is %.1f percent' % (best_arch_frac_epi*100))
print('The best estimate for the fraction of archaea in the mesopelagic layer is %.1f percent' % (best_arch_frac_meso*100))
print('The best estimate for the fraction of archaea in the bathypelagic layer is %.1f percent' % (best_arch_frac_bathy*100))
```

    The best estimate for the fraction of archaea in the epipelagic layer is 7.1 percent
    The best estimate for the fraction of archaea in the mesopelagic layer is 26.3 percent
    The best estimate for the fraction of archaea in the bathypelagic layer is 32.4 percent


### Estimating the fraction of the population in each depth layer
In order to calculate the fraction of archaea out of the total population of marine bacteria and archaea, we need to estimate the fraction of cells in epipelagic, mesopelagic and bathypelagic layers. To do so we use the same sources used for estimating the total number of marine bacteria and archaea, namely, Aristegui et. al, Buitenhuis et al. and Lloyd et al. 


```python
# Load the datasets
buitenhuis = pd.read_excel('../cell_num/marine_prok_cell_num_data.xlsx','Buitenhuis')
aristegui = pd.read_excel('../cell_num/marine_prok_cell_num_data.xlsx','Aristegui')
```

For Lloyd et al., we already calculated the total number of bacteria and archaea at each layer, so we can estimate what is the relative fraction of cells in each layer


```python
# For lloyd et al. we calculate fraction of the sum of bacteria and archaea in each layer out of the 
# total number of bacteria and archaea

lloyd_total_bac_arch_epi = total_arch_epi + total_bac_epi
lloyd_total_bac_arch_meso = total_arch_meso + total_bac_meso
lloyd_total_bac_arch_bathy = total_arch_bathy + total_bac_bathy
lloyd_total_bac_arch = lloyd_total_bac_arch_epi+lloyd_total_bac_arch_meso+lloyd_total_bac_arch_bathy

lloyd_epi_frac = lloyd_total_bac_arch_epi/lloyd_total_bac_arch
lloyd_meso_frac = lloyd_total_bac_arch_meso/lloyd_total_bac_arch
lloyd_bathy_frac = lloyd_total_bac_arch_bathy/lloyd_total_bac_arch

print('The fraction of cells in the epipelagic layer according to Lloyd et al. is %.1f  percent' % (lloyd_epi_frac*100))
print('The fraction of cells in the mesopelagic layer according to Lloyd et al. is %.1f  percent' % (lloyd_meso_frac*100))
print('The fraction of cells in the bathypelagic layer according to Lloyd et al. is %.1f  percent' % (lloyd_bathy_frac*100))
```

    The fraction of cells in the epipelagic layer according to Lloyd et al. is 38.9  percent
    The fraction of cells in the mesopelagic layer according to Lloyd et al. is 32.5  percent
    The fraction of cells in the bathypelagic layer according to Lloyd et al. is 28.6  percent

For Buitenhuis et al., we bin the data along the depth of each sample in 100 m bins. We calculate the average concentration of cells at each bin. For each bin, we calculate the total number of cells in the bin by multiplying the average concentration by the total volume of water in the bin. We calculate the total number of cells in each layer by dividing the bins to each of the layers and summing across all the bins that belong to the same layer.

```python
# Define depth range every 100 m from 0 to 4000 meters
depth_range = np.linspace(0,4000,41)

# Bin data along depth bins
buitenhuis['Depth_bin'] = pd.cut(buitenhuis['Depth'], depth_range)

# For each bin, calculate the average number of cells per liter
buitenhuis_bins = buitenhuis.groupby(['Depth_bin']).mean()['Bact/L']

# Multiply each average concentration by the total volume at each bin: 100 meters depth time the surface area of the oceac

buitenhuis_bins *= 100*ocean_area*liters_in_m3

# For the epipelagic layer, sum across the first three bins
buitenhuis_total_epi = buitenhuis_bins.iloc[0:3].sum()

# For the mesopelagic layer, sum across the relevant bins
buitenhuis_total_meso = buitenhuis_bins.iloc[3:11].sum()

# For the bathypelagic layer, sum across the remaining bins
buitenhuis_total_bathy = buitenhuis_bins.iloc[12:].sum()

#Calculate the total number of cells
buitenhuis_total = buitenhuis_bins.sum()

# Calculate relative fractions
buitenhuis_frac_epi = buitenhuis_total_epi/buitenhuis_total
buitenhuis_frac_meso = buitenhuis_total_meso/buitenhuis_total
buitenhuis_frac_bathy = buitenhuis_total_bathy/buitenhuis_total
print('Total fraction of cells in the epipelagic layer based on Buitenhuis et al.: %.1f percent' % (buitenhuis_frac_epi*100))
print('Total fraction of cells in the mesopelagic layer based on Buitenhuis et al.: %.1f percent' % (buitenhuis_frac_meso*100))
print('Total fraction of cells in the bathypelagic layer based on Buitenhuis et al.: %.1f percent' % (buitenhuis_frac_bathy*100))
```

    Total fraction of cells in the epipelagic layer based on Buitenhuis et al.: 30.7 percent
    Total fraction of cells in the mesopelagic layer based on Buitenhuis et al.: 27.8 percent
    Total fraction of cells in the bathypelagic layer based on Buitenhuis et al.: 39.5 percent


For Aristegui et al. the data is already binned along each layer, so we just calculate the relative fraction of each layer


```python
aristegui_total = aristegui['Cell abundance (cells m-2)'].sum()
aristegui_frac_epi = aristegui.iloc[0]['Cell abundance (cells m-2)']/aristegui_total
aristegui_frac_meso = aristegui.iloc[1]['Cell abundance (cells m-2)']/aristegui_total
aristegui_frac_bathy = aristegui.iloc[2]['Cell abundance (cells m-2)']/aristegui_total
print('Total fraction of cells in the epipelagic layer based on Aristegui et al.: %.1f percent' % (aristegui_frac_epi*100))
print('Total fraction of cells in the mesopelagic layer based on Aristegui et al.: %.1f percent' % (aristegui_frac_meso*100))
print('Total fraction of cells in the bathypelagic layer based on Aristegui et al.: %.1f percent' % (aristegui_frac_bathy*100))
```

    Total fraction of cells in the epipelagic layer based on Aristegui et al.: 23.2 percent
    Total fraction of cells in the mesopelagic layer based on Aristegui et al.: 36.0 percent
    Total fraction of cells in the bathypelagic layer based on Aristegui et al.: 40.8 percent


Our best estimate for the fraction of bacterial and archaeal cells located at each layer is the geometric mean of estiamtes for our three resources - Lloyd et al., Buitenhuis et al., and Aristegui et al.


```python

best_frac_epi = frac_mean(np.array([lloyd_epi_frac,buitenhuis_frac_epi,aristegui_frac_epi]))
best_frac_meso = frac_mean(np.array([lloyd_meso_frac,buitenhuis_frac_meso,aristegui_frac_meso]))
best_frac_bathy = frac_mean(np.array([lloyd_bathy_frac,buitenhuis_frac_bathy,aristegui_frac_bathy]))

print('The best estimate for the fraction of cells in the epipelagic layer is %.1f percent' % (best_frac_epi*100))
print('The best estimate for the fraction of cells in the mesopelagic layer is %.1f percent' % (best_frac_meso*100))
print('The best estimate for the fraction of cells in the bathypelagic layer is %.1f percent' % (best_frac_bathy*100))
```

    The best estimate for the fraction of cells in the epipelagic layer is 30.6 percent
    The best estimate for the fraction of cells in the mesopelagic layer is 32.0 percent
    The best estimate for the fraction of cells in the bathypelagic layer is 36.1 percent


Our best estimate for the fraction of archaea out of the total population of marine bacteria and archaea is the weighted sum of the fraction of archaea in each layer and the fraction of total cells in each layer


```python
best_arch_frac = best_arch_frac_epi*best_frac_epi + best_arch_frac_meso*best_frac_meso+best_arch_frac_bathy*best_frac_bathy
print('Our best estimate for the fraction of archaea out of the total population of marine bacteria and archaea is %.1f percent' %(best_arch_frac*100))
```

    Our best estimate for the fraction of archaea out of the total population of marine bacteria and archaea is 22.3 percent


# Uncertainty analysis

In order to assess the uncertainty associated with our estimate for the fraction of marine archaea out of the total population of marine bacteria and archaea, we gather all possible indices of uncertainty. We compare the uncertainty of values within each one of the methods and the uncertainty stemming from the variability of the values provided by the two methods. 

## Intra-study uncertainty
We first look at the uncertainty of values within the FISH method and the 16S sequencing method.

### FISH method
For the FISH method, as we use regression lines to extrapolate the number of archaea and bacteria across the depth profile. We do not have a good handle of the uncertainty of this procedure. We thus use an alternative measure for the uncertainty of the fraction of archaea. Lloyd et al. reports in each site the fraction of archaea out of the total population of bacteria and archaea. We use the variation of the values between sites as a measure of the uncertainty of the values for the fraction of archaea and bacteria using FISH.


```python
# Set zero values to a small number for numerical stability of the fraction
lloyd_arc_frac = lloyd['Fraction Arc CARDFISH'].dropna()
lloyd_arc_frac[lloyd_arc_frac == 0] = 0.001

print('The intra-study uncertainty of measurements using FISH for the fraction of archaea is %.1f-fold' % frac_CI(lloyd_arc_frac))
print('The intra-study uncertainty of measurements using FISH for the fraction of bacteria is %.2f-fold' % frac_CI(1.-lloyd_arc_frac))
```

    The intra-study uncertainty of measurements using FISH for the fraction of archaea is 1.1-fold
    The intra-study uncertainty of measurements using FISH for the fraction of bacteria is 1.01-fold


    ../../../statistics_helper/fraction_helper.py:54: RuntimeWarning: invalid value encountered in log
      log_alpha = np.log(alpha)
    ../../../statistics_helper/fraction_helper.py:25: RuntimeWarning: invalid value encountered in log10
      log_alpha = np.log10(alpha)


### 16S rDNA sequencing

For the 16S rDNA sequencing method, we rely of two main resources - Sunagawa et al. for the epipelagic and mesopelagic layers, and Salazar et al. for the bathypelagic layer. No uncertainties are reported by Sunagawa et al., and thus we rely on the variability of values in Salazar et al. as a measure of the uncertainty of the values for the fraction of archaea using 16S rDNA sequencing


```python
print('The intra-study uncertainty of measurements using 16S rDNA sequencing for the fraction of archaea is %.1f-fold' % frac_CI(salazar['Archaea']))
print('The intra-study uncertainty of measurements using 16S rDNA sequencing for the fraction of bacteria is %.2f-fold' % frac_CI(1.-salazar['Archaea']))
```

    The intra-study uncertainty of measurements using 16S rDNA sequencing for the fraction of archaea is 1.2-fold
    The intra-study uncertainty of measurements using 16S rDNA sequencing for the fraction of bacteria is 1.04-fold


## Interstudy uncertainty

We calculate the uncertainty (95% multiplicative confidence interval) between the estimates using the two methods - FISH and 16S rDNA sequencing.


```python
# For each layer, calculate the uncertainty between methods
from fractions import *
epi_mul_CI_arch = frac_CI(np.array([FISH_arch_frac_epi,seq_arch_frac_epi]))
meso_mul_CI_arch = frac_CI(np.array([FISH_arch_frac_meso,seq_arch_frac_meso]))
bathy_mul_CI_arch = frac_CI(np.array([FISH_arch_frac_bathy,seq_arch_frac_bathy]))
print('The uncertainty of the fraction of archaea out of the total population of bacteria and archaea in the epipelagic layer is %.1f-fold' %epi_mul_CI_arch)
print('The uncertainty of the fraction of archaea out of the total population of bacteria and archaea in the mesopelagic layer is %.1f-fold' %meso_mul_CI_arch)
print('The uncertainty of the fraction of archaea out of the total population of bacteria and archaea in the bathypelagic layer is %.1f-fold' %bathy_mul_CI_arch)

epi_mul_CI_bac = frac_CI(np.array([1.-FISH_arch_frac_epi,1.-seq_arch_frac_epi]))
meso_mul_CI_bac = frac_CI(np.array([1.-FISH_arch_frac_meso,1.-seq_arch_frac_meso]))
bathy_mul_CI_bac = frac_CI(np.array([1.-FISH_arch_frac_bathy,1.-seq_arch_frac_bathy]))
print('The uncertainty of the fraction of bacteria out of the total population of bacteria and archaea in the epipelagic layer is %.1f-fold' %epi_mul_CI_bac)
print('The uncertainty of the fraction of bacteria out of the total population of bacteria and archaea in the mesopelagic layer is %.1f-fold' %meso_mul_CI_bac)
print('The uncertainty of the fraction of bacteria out of the total population of bacteria and archaea in the bathypelagic layer is %.1f-fold' %bathy_mul_CI_bac)
```

    The uncertainty of the fraction of archaea out of the total population of bacteria and archaea in the epipelagic layer is 1.3-fold
    The uncertainty of the fraction of archaea out of the total population of bacteria and archaea in the mesopelagic layer is 1.6-fold
    The uncertainty of the fraction of archaea out of the total population of bacteria and archaea in the bathypelagic layer is 2.2-fold
    The uncertainty of the fraction of bacteria out of the total population of bacteria and archaea in the epipelagic layer is 1.0-fold
    The uncertainty of the fraction of bacteria out of the total population of bacteria and archaea in the mesopelagic layer is 1.1-fold
    The uncertainty of the fraction of bacteria out of the total population of bacteria and archaea in the bathypelagic layer is 1.3-fold


As our best estimates for the uncertainty associated with the fraction of archaea and bacteria out of the total population of marine bacteria and archaea, we use the highest uncertainty out of the uncertainties of the three depth layers.

The highest interstudy uncertainty for the fraction of archaea is ≈1.8-fold, which is higher than the highest intra-study uncertainty of ≈1.2-fold, so we use ≈1.8-fold as our best projection of the uncertainty associated with the fraction of archaea out of the total population of marine bacteria and archaea. 
Similarly, the highest interstudy uncertainty for the fraction of bacteria is ≈1.2-fold, which is higher than the highest intra-study uncertainty of ≈1.03-fold, so we use ≈1.2-fold as our best projection of the uncertainty associated with the fraction of bacteria out of the total population of marine bacteria and archaea. 

Our final parameters are:


```python
print('Fraction of marine archaea out of the total population of marine bacteria and archaea: %.1f percent' %(best_arch_frac*100))
print('Fraction of marine bacteria out of the total population of marine bacteria and archaea: %.1f percent' %(100.-best_arch_frac*100))
print('Uncertainty associated with the fraction of marine archaea: %.1f-fold' % np.max([epi_mul_CI_arch,meso_mul_CI_arch,bathy_mul_CI_arch]))
print('Uncertainty associated with the fraction of marine bacteria: %.1f-fold' % np.max([epi_mul_CI_bac,meso_mul_CI_bac,bathy_mul_CI_bac]))

old_results = pd.read_excel('../marine_prok_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[2] = pd.Series({
                'Parameter': 'Fraction of archaea',
                'Value': "{0:.1f}".format(best_arch_frac),
                'Units': 'Unitless',
                'Uncertainty': "{0:.1f}".format(np.max([epi_mul_CI_arch,meso_mul_CI_arch,bathy_mul_CI_arch]))
                })

result.loc[3] = pd.Series({
                'Parameter': 'Fraction of bacteria',
                'Value': "{0:.1f}".format(1.0 - best_arch_frac),
                'Units': 'Unitless',
                'Uncertainty': "{0:.1f}".format(np.max([epi_mul_CI_bac,meso_mul_CI_bac,bathy_mul_CI_bac]))
                })


result.to_excel('../marine_prok_biomass_estimate.xlsx',index=False)
```

    Fraction of marine archaea out of the total population of marine bacteria and archaea: 22.3 percent
    Fraction of marine bacteria out of the total population of marine bacteria and archaea: 77.7 percent
    Uncertainty associated with the fraction of marine archaea: 2.2-fold
    Uncertainty associated with the fraction of marine bacteria: 1.3-fold



# Estimating the total number of marine bacteria and archaea

This notebook details the procedure for estimating the total number of marine bacteria and archaea.
The estimate is based on three data sources:
[Aristegui et al.](http://dx.doi.org/10.4319/lo.2009.54.5.1501),
[Buitenhuis et al.](http://dx.doi.org/10.5194/essd-4-101-2012), and
[Lloyd et al.](http://dx.doi.org/10.1128/AEM.02090-13)



```python
import pandas as pd
import numpy as np
from scipy.stats import gmean
pd.options.display.float_format = '{:,.1e}'.format
import sys
sys.path.insert(0, '../../../statistics_helper')
from CI_helper import *
# Genaral parameters used in the estimate
ocean_area = 3.6e14
liters_in_m3 = 1e3
ml_in_m3 = 1e6
```


```python
# Load the datasets
buitenhuis = pd.read_excel('marine_prok_cell_num_data.xlsx','Buitenhuis')
aristegui = pd.read_excel('marine_prok_cell_num_data.xlsx','Aristegui')
aristegui[['Cell abundance (cells m-2)','SE']] = aristegui[['Cell abundance (cells m-2)','SE']].astype(float)
lloyd = pd.read_excel('marine_prok_cell_num_data.xlsx','Lloyd')
```

Here are samples from the data in Aristegui et al.:


```python
aristegui.head()
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
      <th>Zone</th>
      <th>Cell abundance (cells m-2)</th>
      <th>SE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Epipelagic (0-200 m)</td>
      <td>1.1e+14</td>
      <td>8.0e+12</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Mesopelagic (200-1000 m)</td>
      <td>1.7e+14</td>
      <td>1.0e+13</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Bathypelagic (1000-4000 m)</td>
      <td>1.9e+14</td>
      <td>1.4e+13</td>
    </tr>
  </tbody>
</table>
</div>



From the data in Buitenhuis et al.:


```python
buitenhuis.head()
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
      <th>Investigators</th>
      <th>Reference</th>
      <th>Cruise/sample id</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Year</th>
      <th>day</th>
      <th>Depth</th>
      <th>month</th>
      <th>Bact/L</th>
      <th>ug C/L</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Arabian_Sea/bottle</td>
      <td>NaN</td>
      <td>28001</td>
      <td>1.9e+01</td>
      <td>5.8e+01</td>
      <td>1995</td>
      <td>1.2e+01</td>
      <td>1.1e+01</td>
      <td>9</td>
      <td>4.9e+09</td>
      <td>4.5e+01</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Arabian_Sea/bottle</td>
      <td>NaN</td>
      <td>29001</td>
      <td>1.9e+01</td>
      <td>5.9e+01</td>
      <td>1995</td>
      <td>1.3e+01</td>
      <td>1.6e+00</td>
      <td>9</td>
      <td>3.9e+09</td>
      <td>3.5e+01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Arabian_Sea/bottle</td>
      <td>NaN</td>
      <td>3002</td>
      <td>2.2e+01</td>
      <td>6.2e+01</td>
      <td>1995</td>
      <td>2.0e+01</td>
      <td>8.3e+00</td>
      <td>8</td>
      <td>3.2e+09</td>
      <td>2.9e+01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Arabian_Sea/bottle</td>
      <td>NaN</td>
      <td>3002</td>
      <td>2.2e+01</td>
      <td>6.2e+01</td>
      <td>1995</td>
      <td>2.0e+01</td>
      <td>2.3e+00</td>
      <td>8</td>
      <td>3.2e+09</td>
      <td>2.9e+01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Arabian_Sea/bottle</td>
      <td>NaN</td>
      <td>3002</td>
      <td>2.2e+01</td>
      <td>6.2e+01</td>
      <td>1995</td>
      <td>2.0e+01</td>
      <td>5.7e+00</td>
      <td>8</td>
      <td>3.2e+09</td>
      <td>2.9e+01</td>
    </tr>
  </tbody>
</table>
</div>



And from Llyod et al.:


```python
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



For Aristegui et al. we estimate the total number of cells by multiplying each layer by the surface area of the ocean


```python
aristegui_total = (aristegui['Cell abundance (cells m-2)']*ocean_area).sum()
print('Total number of cells based on Aristegui et al.: %.1e' % aristegui_total)
```

    Total number of cells based on Aristegui et al.: 1.7e+29


For Buitenhuis et al. we bin the data along 100 meter depth bins, and estimate the average cell abundance in each bin. We then multiply the total number of cells per liter by the volume at each depth and sum across layers.


```python
# Define depth range every 100 m from 0 to 4000 meters
depth_range = np.linspace(0,4000,41)

#Bin data along depth bins
buitenhuis['Depth_bin'] = pd.cut(buitenhuis['Depth'], depth_range)

#For each bin, calculate the average number of cells per liter
buitenhuis_bins = buitenhuis.groupby(['Depth_bin']).mean()['Bact/L']

#Multiply each average concentration by the total volume at each bin: 100 meters depth time the surface area of the oceac

buitenhuis_bins *= 100*ocean_area*liters_in_m3

#Sum across all bins to get the total estimate for the number of cells of marine prokaryotes
buitenhuis_total = buitenhuis_bins.sum()
print('Total number of cells based on Buitenhuis et al.: %.1e' % buitenhuis_total)
```

    Total number of cells based on Buitenhuis et al.: 1.3e+29


For Lloyd et al., we rely on the sum of the total number of bacteria and archaea. The estimate for the number of bacteria and archaea is based on the regression of the concentration of bacteria and archaea with depth. We use the equations reported in Lloyd et al. to extrapolate the number of cells of bacteria and archaea across the average ocean depth of 4000 km.


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

# Define the regression equation for the number of bacteria in the top 389 m:
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

# Estimate the total number of bacteria in the top 64 m by first estimating the concentration using the 
# regression equation, multiplying by the volume at each depth, which is 1 m^3 times the surface
# Area of the ocean, and finally summing across different depths
total_bac_surf = (bac_surf(np.linspace(0,64,65))*ml_in_m3*ocean_area).sum()

# We repeat the same procedure for the total number of bacteria in waters deeper than 64 m, and for the total
# Number of archaea
total_bac_deep = (bac_deep(np.linspace(65,4000,4000-65+1))*ml_in_m3*ocean_area).sum()
total_arch_surf = (arch_surf(np.linspace(0,389,390))*ml_in_m3*ocean_area).sum()
total_arch_deep = (arch_deep(np.linspace(390,4000,4000-390+1))*ml_in_m3*ocean_area).sum()

# Sum across bacteria and archaea to get the estimate for the total number of bacteria and archaea in the ocean
lloyd_total = total_bac_surf+total_bac_deep+total_arch_surf+total_arch_deep
print('Total number of cells based on Lloyd et al.: %.1e' % lloyd_total)
```

    Total number of cells based on Lloyd et al.: 6.2e+28


The estimate of the total number of cells in Lloyd et al. is based on FISH measurements, but in general not all cells which are DAPI positive are also stained with FISH. To correct for this effect, we estimate the average FISH yield across samples, and divide our estimate from the FISH measurements by the average FISH yield.


```python
fish_yield = lloyd['FISH yield'].dropna()

# Values which are not feasible are turned to the maximal value. We do not use 1 because of numerical reasons
fish_yield[fish_yield >=1] = 0.999

# calculate the statistics on the fish_visible/fish_invisible value and not the 
# fish_visible/(fish_visible+fish_invisible) value because the first is not bound by 0 and 1
# We transform the values to log space to calculate the geometric mean
alpha_fish_yield = np.log10(1./(1./fish_yield[fish_yield<1]-1.))
mean_alpha_yield = np.average(-alpha_fish_yield.dropna())
mean_yield = 1./(1.+10**mean_alpha_yield)

print('The mean yield of FISH is %.1f' % mean_yield)
lloyd_total /= mean_yield
print('After correcting for FISH yield, the estimate for the total number of bacteria and archaea based on Lloyd et al is %.1e' % lloyd_total)


```

    The mean yield of FISH is 0.8
    After correcting for FISH yield, the estimate for the total number of bacteria and archaea based on Lloyd et al is 8.1e+28


Our best estimate for the total number of marine bacteria and archaea is the geometric mean of the estimates from Aristegui et al., Buitenhuis et al. and Lloyd et al.


```python
estimates = [aristegui_total,buitenhuis_total,lloyd_total]
best_estimate = 10**(np.log10(estimates).mean())

print('Our best estimate for the total number of marine bacteria and archaea is %.1e' %best_estimate)
```

    Our best estimate for the total number of marine bacteria and archaea is 1.2e+29


# Uncertainty analysis

To calculate the uncertainty associated with the estimate for the total number of of bacteria and archaea, we first collect all available uncertainties and then take the largest value as our best projection for the uncertainty. 

## Intra-study uncertainties 
We first survey the uncertainties reported in each of the studies. Aristegui et al. report a sandard error of ≈10% for the average cell concentration per unit area. Buitenhuis et al. and Lloyd et al. do not report uncertainties.

## Interstudy uncertainties

We estimate the 95% multiplicative error of the geometric mean of the values from the three studies.


```python
mul_CI = geo_CI_calc(estimates)

print('The interstudy uncertainty is about %.1f' % mul_CI)
```

    The interstudy uncertainty is about 1.5


We thus take the highest uncertainty from our collection which is ≈1.4-fold.
Our final parameters are:


```python
print('Total number of marine bacteria and archaea: %.1e' % best_estimate)
print('Uncertainty associated with the total number of marine bacteria and archaea: %.1f-fold' % mul_CI)

old_results = pd.read_excel('../marine_prok_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[0] = pd.Series({
                'Parameter': 'Total number of marine bacteria and archaea',
                'Value': int(best_estimate),
                'Units': 'Cells',
                'Uncertainty': "{0:.1f}".format(mul_CI)
                })

result.to_excel('../marine_prok_biomass_estimate.xlsx',index=False)

```

    Total number of marine bacteria and archaea: 1.2e+29
    Uncertainty associated with the total number of marine bacteria and archaea: 1.5-fold


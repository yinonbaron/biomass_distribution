
# Estimateing the biomass contribution of particle-attached bacteria and archaea in the ocean
In order to estimate the total biomass of bacteria and archaea attached to particulate organic matter (POM), we assemble studies which report the local contribution of particle-attached bacteria and archaea to the total number of cells. We focus here on the two main categories of POM - macroaggregates (>0.5 mm in diameter) and microaggregates (smaller then 0.5 mm in diameter ). We estimate the biomass contribution of bacteria and archaea attached to each size category, and then sum up the contributions to estimate the total biomass of particle-attached bacteria and archaea in the ocean. We first survey data on the fraction of the total number of cells which is attached to either macro- or microaggregates. We then estimate the carbon content of particle-attached cells relative to free-living cells.

## Fraction of number of cells which is particle-attached
### Macroaggregates
In order to estimate the total biomass of bacteria and archaea attached to macroaggregates, we collected data from several studies which report the fraction of the total number of bacteria and archaea which is attached to macroaggregates. Here is a sample of the data:


```python
# Import dependencies
import pandas as pd
import numpy as np
from scipy.stats import gmean
import sys
sys.path.insert(0, '../../../statistics_helper')
from CI_helper import *
from fraction_helper import *
pd.options.display.float_format = '{:,.2f}'.format

# Load data
macro = pd.read_excel('poc_data.xlsx','Macroaggregates')
macro.head()
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
      <th>Location</th>
      <th>Fraction of cells in aggregates</th>
      <th>Size of cells relative to free-living cells</th>
      <th>Volume of cells [µm^3]</th>
      <th>Carbon content [fg C]</th>
      <th>Cells on aggregates concentration [cells mL^-1]</th>
      <th>Reference</th>
      <th>Link</th>
      <th>Remarks</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Southern California Bight</td>
      <td>0.01</td>
      <td>1.90</td>
      <td>0.20</td>
      <td>nan</td>
      <td>1,045.00</td>
      <td>Alldredge &amp; Gotschalk</td>
      <td>http://dx.doi.org/10.1016/0278-4343(90)90034-J</td>
      <td>Based on tables 1,2 and 3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Southern California Bight</td>
      <td>0.00</td>
      <td>1.40</td>
      <td>0.15</td>
      <td>nan</td>
      <td>1,997.50</td>
      <td>Alldredge &amp; Gotschalk</td>
      <td>http://dx.doi.org/10.1016/0278-4343(90)90034-J</td>
      <td>Based on tables 1,2 and 3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Southern California Bight</td>
      <td>0.00</td>
      <td>1.10</td>
      <td>0.12</td>
      <td>nan</td>
      <td>1,100.00</td>
      <td>Alldredge &amp; Gotschalk</td>
      <td>http://dx.doi.org/10.1016/0278-4343(90)90034-J</td>
      <td>Based on tables 1,2 and 3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Southern California Bight</td>
      <td>0.01</td>
      <td>1.30</td>
      <td>0.16</td>
      <td>nan</td>
      <td>6,612.00</td>
      <td>Alldredge &amp; Gotschalk</td>
      <td>http://dx.doi.org/10.1016/0278-4343(90)90034-J</td>
      <td>Based on tables 1,2 and 3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Mediterranean</td>
      <td>0.03</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>10,600.00</td>
      <td>Turley &amp; Stutt</td>
      <td>http://dx.doi.org/10.4319/lo.2000.45.2.0419</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



To generate our best estimate for the fraction of cells attached to macroaggregates, we first calculate the average fraction of particle-attached cells within each study. We calculate both the arithmetic mean fraction as well as the geometric mean fraction of cells.


```python
# Calculate the mean fraction of particle-attached cells whitin each study
macro_study_mean = macro.groupby('Reference')['Fraction of cells in aggregates'].apply(np.nanmean)
macro_study_gmean = macro.groupby('Reference')['Fraction of cells in aggregates'].apply(frac_mean)
```

    /usr/local/lib/python3.5/dist-packages/pandas/core/groupby.py:1880: RuntimeWarning: Mean of empty slice
      res = f(group)


We then calculate the mean fraction of particle-attached cells between different studies. We calculate both the arithmetic mean fraction as well as the geometric mean fraction of cells. We thus generate two estimates for the fraction of particle-attached cells out of the total population of marine bacteria and archaea- one based on arithmetic means and one based on geometric means. The estimate based on the arithmetic mean is more susceptible to sampling bias, as even a single measurement which is not characteristic of the global population (such as samples which are contaminated with organic carbon sources, or samples which have some technical biases associated with them) might shift the average concentration significantly. On the other hand, the estimate based on the geometric mean might underestimate global biomass as it will reduce the effect of biologically relevant high biomass concentrations. As a compromise between these two caveats, we chose to use as our best estimate the geometric mean of the estimates from the two methodologies.


```python
# Calculate the mean fraction of particle-attached cells between different studies
macro_mean = np.nanmean(macro_study_mean)
macro_gmean = frac_mean(macro_study_gmean)

# Use the geometric mean of the arithmetic and geometric mean based estimates as our best estimate
best_macro_frac = frac_mean(np.array([macro_mean,macro_gmean]))

print('Our best estimate for the fraction of the toal number of marine bacteria and archaea which is attached to macroaggregates is ≈%.0f percent' %(best_macro_frac*100))

```

    Our best estimate for the fraction of the toal number of marine bacteria and archaea which is attached to macroaggregates is ≈3 percent


### Microaggregates
In order to estimate the total biomass of bacteria and archaea attached to microaggregates, we collected data from several studies which report the fraction of the total number of bacteria and archaea which  is attached to macroaggregates. Here is a sample of the data:


```python
# Load the data on microaggregates
micro = pd.read_excel('poc_data.xlsx','Microaggregates')
micro.head()
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
      <th>Site</th>
      <th>Depth [m]</th>
      <th>Station</th>
      <th>Fraction of attached cells</th>
      <th>Reference</th>
      <th>Link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Arctic Fram Strait</td>
      <td>5</td>
      <td>S3</td>
      <td>0.02</td>
      <td>Busch et al.</td>
      <td>http://dx.doi.org/10.3389/fmars.2017.00166</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Arctic Fram Strait</td>
      <td>15</td>
      <td>S3</td>
      <td>0.02</td>
      <td>Busch et al.</td>
      <td>http://dx.doi.org/10.3389/fmars.2017.00166</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Arctic Fram Strait</td>
      <td>30</td>
      <td>S3</td>
      <td>0.02</td>
      <td>Busch et al.</td>
      <td>http://dx.doi.org/10.3389/fmars.2017.00166</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Arctic Fram Strait</td>
      <td>45</td>
      <td>S3</td>
      <td>0.01</td>
      <td>Busch et al.</td>
      <td>http://dx.doi.org/10.3389/fmars.2017.00166</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Arctic Fram Strait</td>
      <td>75</td>
      <td>S3</td>
      <td>0.02</td>
      <td>Busch et al.</td>
      <td>http://dx.doi.org/10.3389/fmars.2017.00166</td>
    </tr>
  </tbody>
</table>
</div>



In a similar manner to our procedure regarding macroaggregates, we calculate the arithmetic and geometric means of the fraction of particle-attached cells within each study:


```python
# Calculate the mean fraction of particle-attached cells whitin each study
micro_study_mean = micro.groupby('Reference')['Fraction of attached cells'].apply(np.nanmean)
micro_study_gmean = micro.groupby('Reference')['Fraction of attached cells'].apply(frac_mean)
```

We then calculate the mean fraction of particle-attached cells between different studies. We calculate both the arithmetic mean fraction as well as the geometric mean fraction of cells. We thus generate two estimates for the fraction of particle-attached cells out of the total population of marine bacteria and archaea- one based on arithmetic means and one based on geometric means. We use as our best estimate the geometric mean of the estimates from the two methodologies.


```python
# Calculate the mean fraction of particle-attached cells between different studies
micro_mean = micro_study_mean.mean()
micro_gmean = frac_mean(micro_study_gmean)

# Use the geometric mean of the arithmetic and geometric mean based estimates as our best estimate
best_micro_frac = frac_mean(np.array([micro_mean,micro_gmean]))

print('Our best estimate for the fraction of the toal number of marine bacteria and archaea which is attached to microaggregates is ≈%.0f percent' %(best_micro_frac*100))
```

    Our best estimate for the fraction of the toal number of marine bacteria and archaea which is attached to microaggregates is ≈4 percent


## Carbon content of particle-attached cells
Several studies have indicated that particle-attached cells are more bigger in volume, and thus more carbon rich. To estimate the carbon content of particle-attached cells we use two strategies. The first is based on studies  which report the carbon content of particle-attached cells relative to free-living cells. We assume the carbon content of bacteria and archaea which are attached to microaggregates and macroaggregates is similar. 

### Relative carbon content
We first calculate the geometric mean of the size of particle-attached cells relative to free-living cells within each study. Then we calculate the geometric mean of the values reported by different studies as our best estimate for the size of particle-attached cells relative to free-living cells.


```python
# Calculate the geometric mean of the relative size of particle attached cells within each study
rel_size_study = macro.groupby(['Location','Reference'])['Size of cells relative to free-living cells'].apply(gmean)

# Calculate the geometric mean of the values reported in different studies as our best estimate
best_rel_size = gmean(rel_size_study.dropna())

print('Our best estimate for the size of particle-attached cells relative to free-living cells is ≈%1.f-fold' % best_rel_size)
```

    Our best estimate for the size of particle-attached cells relative to free-living cells is ≈3-fold


### Volume of particle-attached cells
We assembled studies estimating the volume of particle-attached cells. We convert this volume to carbon content using the allometric relation reported by [Simon & Azam](http://dx.doi.org/10.3354/meps051201). The allometric model is:
$$C = 88.1 \times V^{0.59}$$
We first calculate the geometric mean of volumes within each study:


```python
# Calculate the geometric mean of the volume of particle-attached cells reported within each study
vol_study = macro.groupby('Reference')['Volume of cells [µm^3]'].apply(gmean)
```

We then calculate the geometric mean of volumes reported in different studies. We convert our best estimate to the volume of particle-attached cells to carbon content based on the formula reported in Simon & Azam. We calculate the carbon content of particle-attached cells relative to free-living cells based on our estimate for the carbon content of free-living bacteria and archaea in the ocean of ≈11 fg C (see the relevant section in the Supplementary Information for more details).


```python
# Calculate the geometric mean of volumes reported in different studies
best_vol = gmean(vol_study.dropna())

# The allometric model reported by Simon & Azam
sa_model = lambda x: 88.1*x**0.59

# Convert our best estimate for the volume of particle-attached cells to carbon content
best_cc = sa_model(best_vol)

# Our best estimate for the carbon content of free-living marine bacteria and archaea 
free_living_cc = 11

# Calculate the relative carbon content of particle-attached cells.
vol_rel_size = best_cc/free_living_cc

print('Our best estimate for the carbon content of particle-attached cells relative to free-living cells based on volume is ≈%1.f-fold' % vol_rel_size)
```

    Our best estimate for the carbon content of particle-attached cells relative to free-living cells based on volume is ≈4-fold


We use the geometric mean of the two estimates of the carbon content of particle-attached cells relative to free-living cells as our best estimate:


```python
best_rel_cc= gmean([best_rel_size,vol_rel_size])
print('Our best estimate for the carbon content of particle-attached cells relative to free-living cells is ≈%1.f-fold' % best_rel_cc)
```

    Our best estimate for the carbon content of particle-attached cells relative to free-living cells is ≈3-fold


To estimate the fraction of the total biomass of marine bacteria and archaea which is particle-attached, we sum up the fraction of the total number of cells contributed by cells attached to micro- and macroaggregates, and multiply it by the relative carbon content of particle-attached cells:


```python
best_estimate = (best_macro_frac+best_micro_frac)*best_rel_cc

print('Our best estimate for the fraction of the total biomass of marine bacteria and archaea which is particle-attached is ≈%.0f percent' %(best_estimate*100))
```

    Our best estimate for the fraction of the total biomass of marine bacteria and archaea which is particle-attached is ≈23 percent


# Uncertainty analysis
To project the uncertainty associated with our estimate of the fraction of the total biomass of marine bacteria and archaea which is particle-attached, we first project the uncertainty associated with the two factors of our estimate - the fraction of the total number of cells which is particle-attached and the relative carbon content of particle-attached cells

## Fraction of cells
We first assess the uncertainty associated with the estimate of the fraction of the total number of cells which is attached to microaggregates and macroaggregates. We then propagate the uncertainty from each fraction to our estimate of the total fraction of cells. We begin with the uncertainty associated with our estimate of the total number of cells which are attached to microaggregates.

### Microaggregates
We collect both the intra-study uncertainty and the interstudy uncertainty associated with our estimate of the fraction of the total number of marine bacteria and archaea which are attached to microaggregates. We use the maximum of this collection of uncertainties as our best projection of the uncertainty associated with our estimate of the fraction of the total number of marine bacteria and archaea whcih are attached to microaggregates.
#### Intra-study uncertainty
We calculate the 95% confidence interval around the mean fraction of microaggregate-attached cells within each study:


```python
# Calculate the 95% confidence interval around the mean fraction of cells attached to microaggregates 
# within each study
micro_study_CI = micro.groupby('Reference')['Fraction of attached cells'].apply(frac_CI)
```

#### Interstudy uncertainty
We calculate the 95% confidence interval around the mean fraction of microaggregate-attached cells between differnt studies:


```python
# Calculate the 95% confidence interval around the mean fraction of cells attached to microaggregates 
# between different studies
micro_CI = frac_CI(micro_study_gmean)
```

#### Inter-method uncertainty
We calculate the 95% confidence interval around the geometric mean between the estimate based on arithmetic means and geometric means of the fraction of cells attached to microaggregates:


```python
# Calculate the 95% confidence interval around the geometric mean of the estimates based on arithmetic means
# and geometric means
micro_inter_method_CI = frac_CI(np.array([micro_mean,micro_gmean]))
```

We use the maximum of the collection of uncertainties as our best projection for the uncertainty associated with our estimate of the fraction of the total number of bacteria and archaea which is attached to microaggregates:


```python
micro_frac_CI = np.max([micro_inter_method_CI,micro_study_CI.max(),micro_CI])
print('Our best projection for the uncertainty associated with our estimate of the total number of bacteria and archaea which is attached to microaggregates is ≈%.1f-fold' %micro_frac_CI)
```

    Our best projection for the uncertainty associated with our estimate of the total number of bacteria and archaea which is attached to microaggregates is ≈2.3-fold


### Macroaggregates
We collect both the intra-study uncertainty and the interstudy uncertainty associated with our estimate of the fraction of the total number of marine bacteria and archaea which are attached to macroaggregates. We use the maximum of this collection of uncertainties as our best projection of the uncertainty associated with our estimate of the fraction of the total number of marine bacteria and archaea whcih are attached to macroaggregates.
#### Intra-study uncertainty
We calculate the 95% confidence interval around the mean fraction of macroaggregate-attached cells within each study:


```python
# Calculate the 95% confidence interval around the mean fraction of cells attached to macroaggregates 
# within each study
macro_study_CI = macro.groupby('Reference')['Fraction of cells in aggregates'].apply(frac_CI)
```

    /usr/local/lib/python3.5/dist-packages/numpy/lib/function_base.py:4116: RuntimeWarning: Invalid value encountered in percentile
      interpolation=interpolation)


#### Interstudy uncertainty
We calculate the 95% confidence interval around the mean fraction of macroaggregate-attached cells between differnt studies:


```python
# Calculate the 95% confidence interval around the mean fraction of cells attached to microaggregates 
# between different studies
macro_CI = frac_CI(macro_study_gmean)
```

#### Inter-method uncertainty
We calculate the 95% confidence interval around the geometric mean between the estimate based on arithmetic means and geometric means of the fraction of cells attached to microaggregates:


```python
# Calculate the 95% confidence interval around the geometric mean of the estimates based on arithmetic means
# and geometric means
macro_inter_method_CI = frac_CI(np.array([macro_mean,macro_gmean]))
```

We use the maximum of the collection of uncertainties as our best projection for the uncertainty associated with our estimate of the fraction of the total number of bacteria and archaea which is attached to macroaggregates:


```python
macro_frac_CI = np.max([macro_inter_method_CI,macro_study_CI.max(),macro_CI])
print('Our best projection for the uncertainty associated with our estimate of the total number of bacteria and archaea which is attached to macroaggregates is ≈%.1f-fold' %macro_frac_CI)
```

    Our best projection for the uncertainty associated with our estimate of the total number of bacteria and archaea which is attached to macroaggregates is ≈7.3-fold


We propagate the uncertainties associated with the estimates of the fraction of the total number of marine bacteria and archaea attached to micro- and macroaggregates to the final estimate of the fraction of marine bacteria and archaea which is particle-attached:


```python
# Propagate the uncertainties of the fraction of cells attached to micro- and macroaggregates
# to the estiamte of the fraction of cells which is particle-attached
num_frac_CI = CI_sum_prop(estimates=np.array([best_micro_frac,best_macro_frac]),mul_CIs=np.array([micro_frac_CI,macro_frac_CI]))
print('Our best projection for the uncertainty associated with our estimate of the total number of bacteria and archaea which is particle-attached is ≈%.1f-fold' %num_frac_CI)
```

    Our best projection for the uncertainty associated with our estimate of the total number of bacteria and archaea which is particle-attached is ≈2.8-fold


## Relative carbon content
We assess the uncertainty associated with the estimate of the relative carbon content of particle-attached cells. We used two independent methods to estimate the relative carbon content. We assess the unertainty associate with each one of them.
### Relative size-based
We collect both the intra-study uncertainty and the interstudy uncertainty associated with our estimate of the size of particle-attached cells relative to free-livign cells. 
#### Intra-study
We calculate the 95% confidence interval around the mean size of particle-attached cells reltive to free-living cells within each study:


```python
size_intra_CI = macro.groupby(['Location','Reference'])['Size of cells relative to free-living cells'].apply(geo_CI_calc)
```

#### Inter-study
We calculate the 95% confidence interval around the mean size of particle-attached cells reltive to free-living cells between different studies:


```python
size_inter_CI = geo_CI_calc(rel_size_study.dropna())
```

### Volume-based
We collect both the intra-study uncertainty and the interstudy uncertainty associated with our estimate of the volume of particle-attached cells. 
#### Intra-study
We calculate the 95% confidence interval around the mean volume of particle-attached cells within each study:


```python
vol_intra_CI = macro.groupby('Reference')['Volume of cells [µm^3]'].apply(geo_CI_calc)
```

#### Inter-study
We calculate the 95% confidence interval around the mean volume of particle-attached cells between different studies:


```python
vol_inter_CI = geo_CI_calc(vol_study.dropna())
```

### Inter-method uncertainty
We calculate the 95% confidence interval around the geometric mean between the size-based estimate and the volume based estimate:


```python
cc_inter_method_CI = geo_CI_calc(np.array([vol_rel_size,best_rel_size]))
```

We use the maximum of the collection of uncertainties for both the volume-based methoda and the size based method as our best projection of the uncertainty associated with our estimate of the relative carbon content of particle-attached bacteria and archaea:


```python
cc_CI = np.max([cc_inter_method_CI,vol_inter_CI,vol_intra_CI.max(),size_inter_CI,size_intra_CI.max()])
print('Our best projection for the uncertainty associated with our estimate of the relative carbon content of particles-attached bacteria and archaea is ≈%.1f-fold' %cc_CI)
```

    Our best projection for the uncertainty associated with our estimate of the relative carbon content of particles-attached bacteria and archaea is ≈2.8-fold


We combine our projections for the uncertainty associated with our estimate of the fraction of the total number of cells which is particle-attached and our estimate of the relative carbon content of particle-attached cells.


```python
mul_CI = CI_prod_prop(np.array([cc_CI,num_frac_CI]))
print('Our best projection for the uncertainty associated with our estimate of the fraction of the total biomass of marine bactetia and archaea which is particle-attached is ≈%.1f-fold' %mul_CI)
```

    Our best projection for the uncertainty associated with our estimate of the fraction of the total biomass of marine bactetia and archaea which is particle-attached is ≈4.3-fold


Our final parameters are:


```python
print('Fraction of the total biomass of marine bacteria and archaea which is particle-attahced: %.1e' % best_estimate)
print('Uncertainty associated with the fraction of the biomass of marine bacteria and archaea which is particle-attached: %.1f-fold' % mul_CI)

old_results = pd.read_excel('../marine_prok_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[4] = pd.Series({
                'Parameter': 'Fraction of the total biomass of marine bacteria and archaea which is particle-attached',
                'Value': best_estimate,
                'Units': 'Unitless',
                'Uncertainty': "{0:.1f}".format(mul_CI)
                })

result.to_excel('../marine_prok_biomass_estimate.xlsx',index=False)
```

    Fraction of the total biomass of marine bacteria and archaea which is particle-attahced: 2.3e-01
    Uncertainty associated with the fraction of the biomass of marine bacteria and archaea which is particle-attached: 4.3-fold


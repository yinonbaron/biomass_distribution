
# Estimating the total number of terrestrial deep subsurface phages
Estimating the total number of phages in the terrestrial deep subsurface is challenging as data on the abundance of phages in this environment is scarce. To generate an estimate for the total number of phages present in the terrestrial deep subsurface, we combined five different types of estimates for the ratio between the concentration of prokaryotes and phage-like particles. Below we detail these five different estimates. 

## Phage-like particle to prokaryotes concentration ratios
### Naive ratio of phage-live particles and prokaryotes
A common claim regarding the ratio between the concentration of phage-like particles and prokaryotes is that phage-like particles are about 10 times more abundant than the number of prokaryotes. We use this ratio as our first estimate for the ratio between the concentration of phage-like particles and prokaryotes.


```python
naive_ratio = 10
```

### Engelhardt et al. based ratio
For our second estimate of the ratio of the concentration of phage-like particles and prokaryotes, we use the relation measured in subseafloor sediments by [Engelhardt et al.](http://dx.doi.org/10.1038/ismej.2013.245). The ratio Engelhardt et al. measured is: $$V = 271.8\times P ^{0.768}$$
Where V is the concentrations of phage-like particles and P is the concentration of prokaryotes.



```python
engelhardt_ratio = lambda x: 271.8*x**0.768
```

### Kyle et al. based ratio
For our fourth estimate of the ratio of the concentration of phage-like particles and prokaryotes, we use the relation measured in the terrestrial deep subsurface by [Kyle et al.](http://dx.doi.org/10.1038/ismej.2008.18). The ratio Kyle et al. measured is: $$V = 10^{1.3\times log_{10}(P)-0.62}$$
Where V is the concentrations of phage-like particles and P is the concentration of prokaryotes.


```python
kyle_ratio = lambda x: 10**(1.3*np.log10(x)-0.62)
```

### Pan et al. based ratio
For our third estimate of the ratio of the concentration of phage-like particles and prokaryotes, we use the relation measured in the terrestrial deep subsurface by [Pan et al.](http://dx.doi.org/10.3389/fmicb.2017.01199). Pan et al. measured the concentration of phage-like particles and prokaryotes in alluvial aquifer which is situated near a U.S. Department of Energy uranium ore-processing site. The measurement were done in aquifers that are inside or outside a uranium plume from the nearby site. We use the data from samples outside the plume and calculate a geometric mean of the ratio between the concentration of phage-like particles and prokaryotes.



```python
import pandas as pd
pd.options.display.float_format = '{:,.1e}'.format
import numpy as np
import sys
sys.path.insert(0, '../../../statistics_helper/')
from CI_helper import *

from scipy.stats import gmean
pan_data = pd.read_excel('terrestrial_deep_subsurface_phage_num_data.xlsx','Pan',skiprows=1)
pan_ratio = gmean(pan_data['Virus-to-cell ratio (VCR)'])
print('Our estimate for the ratio between the concentration of phage-like particles and prokaryotes based on Pan et al. is ≈%.0f.' % pan_ratio)

```

    Our estimate for the ratio between the concentration of phage-like particles and prokaryotes based on Pan et al. is ≈3.


### Roundnew et al. based ratio
For our fifth estimate of the ratio of the concentration of phage-like particles and prokaryotes, we use the relation measured in the terrestrial deep subsurface by [Roundnew et al.](http://onlinelibrary.wiley.com/doi/10.1111/j.1745-6592.2011.01393.x/full). Roundnew et al. measured the concentration of phage-like particles and prokaryotes in groundwater along a depth profile. We use the data from samples outside the plume and calculate a geometric mean of the ratio between the concentration of phage-like particles and prokaryotes.



```python
roundnew_data = pd.read_excel('terrestrial_deep_subsurface_phage_num_data.xlsx','Roundnew',skiprows=1)
roundnew_ratio = gmean(roundnew_data['Virus:Bacteria ratio'])
print('Our estimate for the ratio between the concentration of phage-like particles and prokaryotes based on Roundnew et al. is ≈%.0f.' % roundnew_ratio)
```

    Our estimate for the ratio between the concentration of phage-like particles and prokaryotes based on Roundnew et al. is ≈2.


## Generating estimates for the total number of phages in the terrestrial deep subsurface
These estimates of the ratio of the concentration of phage-like particles and prokaryotes can be used to estimate the total number of phages by plugging into them an estimate for the total number of prokaryotes in the terrestrial deep subsurface. After detailing the five estimates of the ratio between the number of phage-like particles and prokaryotes, we discuss the estimate of the total number of prokaryotes in the terrestrial deep subsurface that we plug into the ratios to generate estimates of the total number of phages in the terrestrial deep subsurface.

In general, it is not clear whether the measured ratios between the concentrations of phage-like particles and prokaryotes refer to attached or unattached cells. We take this factor into consideration in our estimate as a scaling factor that converts the estimated number of phages in groundwater to an estimate for the total number of phages. Our best estimate for this factor is a geometric mean of three estimates. The first takes into account only groundwater, and the other two assume an that attached cells (and thus also phages) are ≈$10^2-10^3$ more abundant than cell in groundwater (as estimated in [McMahon & Parnell](http://dx.doi.org/10.1111/1574-6941.12196)).

The estimates of the ratio between the concentration of phage-like particles and prokaryotes can be divided to two categories: estimates that are invariant to the local concentration of prokaryotes and ratios that are dependent on the local concentration of prokaryotes.

The first category of estimates includes the naive estimate and the estimates by Pan et al. and Roundnew et al. For those estimates, we can just plug in an estimate for the total number of prokaryotes in the terrestrial deep subsurface and get an estimate for the total number of phages. The second category includes the estimates by Engelhardt et al. and Kyle et al. For those estimates, we need to use the local concentrations of prokaryotes to generate local concentrations of phage-like particles, and then sum all the local concentrations.

We start with generating the estimates for the first category of estimates of the ratio between the concentration of phage-like particles and prokaryotes. The total number of prokaryotes we use is based on our analysis of the biomass of terrestrial bacteria and archaea (see relevant section in the Supplementary Information). As we note in the section on the biomass of terrestrial deep subsurface prokaryotes, we generate two estimates for the total number of cells in groundwater - one based on arithmetic means of cell concentrations at several depth bins, and the other based on geometric means of cell concentraions at the same depth bins. Here is a view of the data:


```python
# Load data on the concentrations of prokaryotes in each depth bin from our analysis of the biomass
# of terrestrial deep subsurface prokaryotes
prok_concentration = pd.read_excel('terrestrial_deep_subsurface_prok_num.xlsx','Cell concentration')
prok_concentration = prok_concentration.reset_index().set_index('Depth bin [m]')
prok_concentration
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
      <th>index</th>
      <th>Mean cell concentration [cells mL-1]</th>
      <th>Geometric mean cell concentration [cells mL-1]</th>
    </tr>
    <tr>
      <th>Depth bin [m]</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>(0.0, 250.0]</th>
      <td>0</td>
      <td>1.0e+06</td>
      <td>4.2e+05</td>
    </tr>
    <tr>
      <th>(250.0, 500.0]</th>
      <td>1</td>
      <td>6.4e+05</td>
      <td>2.2e+05</td>
    </tr>
    <tr>
      <th>(500.0, 750.0]</th>
      <td>2</td>
      <td>7.3e+05</td>
      <td>4.1e+05</td>
    </tr>
    <tr>
      <th>(750.0, 1000.0]</th>
      <td>3</td>
      <td>1.6e+05</td>
      <td>6.7e+04</td>
    </tr>
    <tr>
      <th>(1000.0, 1250.0]</th>
      <td>4</td>
      <td>1.6e+05</td>
      <td>1.2e+05</td>
    </tr>
    <tr>
      <th>(1250.0, 1500.0]</th>
      <td>5</td>
      <td>1.4e+05</td>
      <td>1.2e+04</td>
    </tr>
    <tr>
      <th>(1500.0, 1750.0]</th>
      <td>6</td>
      <td>2.9e+04</td>
      <td>3.4e+03</td>
    </tr>
    <tr>
      <th>(1750.0, 2000.0]</th>
      <td>7</td>
      <td>2.1e+04</td>
      <td>3.5e+03</td>
    </tr>
  </tbody>
</table>
</div>



We multiply the concentraion by data on the total volume of groundwater at each depth bin. The data on the total volume at each depth bin is generated in our analysis of the biomass of terrestrial deep subsurface prokaryotes. Here is a view of the water volume data:


```python
# Load data on the total volume of groundwater in each depth bin from our analysis of the biomass
# of terrestrial deep subsurface prokaryotes
water_vol = pd.read_excel('terrestrial_deep_subsurface_prok_num.xlsx','Water volume')
water_vol = water_vol.reset_index().set_index('Depth bin [m]')
water_vol
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
      <th>index</th>
      <th>Water volume [mL]</th>
    </tr>
    <tr>
      <th>Depth bin [m]</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>(0.0, 250.0]</th>
      <td>0</td>
      <td>5.4e+21</td>
    </tr>
    <tr>
      <th>(250.0, 500.0]</th>
      <td>1</td>
      <td>4.1e+21</td>
    </tr>
    <tr>
      <th>(500.0, 750.0]</th>
      <td>2</td>
      <td>3.2e+21</td>
    </tr>
    <tr>
      <th>(750.0, 1000.0]</th>
      <td>3</td>
      <td>2.6e+21</td>
    </tr>
    <tr>
      <th>(1000.0, 1250.0]</th>
      <td>4</td>
      <td>2.2e+21</td>
    </tr>
    <tr>
      <th>(1250.0, 1500.0]</th>
      <td>5</td>
      <td>1.9e+21</td>
    </tr>
    <tr>
      <th>(1500.0, 1750.0]</th>
      <td>6</td>
      <td>1.7e+21</td>
    </tr>
    <tr>
      <th>(1750.0, 2000.0]</th>
      <td>7</td>
      <td>1.6e+21</td>
    </tr>
  </tbody>
</table>
</div>



To calculate the total number of phages based on the naive method and based on the data in Pan et al. and Roundnew et al., we calculate the total number of prokaryotes by multiplying the cell concentration at each depth bin by the total volume of water at that depth bin, and sum over depth bins:


```python
tot_prok = pd.DataFrame()

# Multiply the arithmetic of geometric mean concentrations of prokaryotes at each depth bin 
# by the total volume of groundwater at each depth bin
tot_prok['Geometric mean estimate'] = prok_concentration['Geometric mean cell concentration [cells mL-1]'] * water_vol['Water volume [mL]']
tot_prok['Arithmetic mean estimate'] = prok_concentration['Mean cell concentration [cells mL-1]'] * water_vol['Water volume [mL]']
tot_prok.sum()
```




    Geometric mean estimate    4.9e+27
    Arithmetic mean estimate   1.2e+28
    dtype: float64



Our best estimate for the total number of prokaryotes in groundwater is the geometric mean of the total number of prokaryotes based on geometric and arithmetic mean concentrations (see the biomass of terrestrial deep subsurface prokaryotes section for details). 


```python
# Estimate the total number of prokaryotes in groundwater as the geometric mean of the estimates based on 
# arithmetic and geometric mean cell concentrations
tot_prok_num_gw = gmean(tot_prok.sum())

print('Our best estimate for the total number of prokaryotes in groundwater for the calculation of the total number of phages in the terrestrial deep subsurface is %.0e.' %tot_prok_num_gw)

```

    Our best estimate for the total number of prokaryotes in groundwater for the calculation of the total number of phages in the terrestrial deep subsurface is 8e+27.


Now that we have an estimate for the total number of prokaryotes, we can plug them into the ratios estimated based on the data in Pan et. al, Roundnew et al., or to use our naive estimate of ten times more phages than prokaryotes.

As stated above, to go from the total number of phages in groundwater to our estimate for the total number of phages in the terrestrial deep subsurface, we multiply our estimate of the total number of phages by a scaling factor. As our best estimate for this scaling factor we use geometric mean of three estimates. The first takes into account only groundwater (and thus the scaling factor is 1), and the other two assume an attached to unattached ratios of $10^2-10^3$ as in [McMahon & Parnell](http://dx.doi.org/10.1111/1574-6941.12196).


```python
# Define the scaling factor from number of cells in groundwater to cells relevant for calculating the total
# Number of phages
scaling_factor = gmean([1,100,1000])


# Estimate the total number of phages based on the naive ratio of 10:1
tot_phage_naive = tot_prok_num_gw*naive_ratio*scaling_factor
print('Our estimate for the total number of phages in the terrestrial deep subsurface based on the naive ratio of 10:1 is %.0e' %tot_phage_naive)

# Estimate the total number of phages based on Pan et al.
tot_phage_pan = tot_prok_num_gw*pan_ratio*scaling_factor
print('Our estimate for the total number of phages in the terrestrial deep subsurface based on Pan et al. is %.0e' %tot_phage_pan)

# Estimate the total number of phages based on Roundnew et al.
tot_phage_roundnew = tot_prok_num_gw*roundnew_ratio*scaling_factor
print('Our estimate for the total number of phages in the terrestrial deep subsurface based on Pan et al. is %.0e' %tot_phage_roundnew)

```

    Our estimate for the total number of phages in the terrestrial deep subsurface based on the naive ratio of 10:1 is 3e+30
    Our estimate for the total number of phages in the terrestrial deep subsurface based on Pan et al. is 9e+29
    Our estimate for the total number of phages in the terrestrial deep subsurface based on Pan et al. is 6e+29


For the two estimates of the ratio between the concentration of phage-like particles and prokaryotes which are dependent on the local concentraions of prokaryotes, we the data on the arithmetic and geometric mean cell concentrations at each depth bin total number of cells at each depth bin, and plug it into the relations described by either Engelhardt et al. or Kyle et al.:


```python
engelhardt_phage_conc_geo_mean = engelhardt_ratio(prok_concentration['Geometric mean cell concentration [cells mL-1]'])
engelhardt_phage_conc_mean = engelhardt_ratio(prok_concentration['Mean cell concentration [cells mL-1]'])

kyle_phage_conc_mean = kyle_ratio(prok_concentration['Mean cell concentration [cells mL-1]'])
kyle_phage_conc_geo_mean = kyle_ratio(prok_concentration['Geometric mean cell concentration [cells mL-1]'])
```

We calculate the total number of phages based on the arithmetic and geometric mean concentration in each depth bin by multiplying by the total volume of groundwater at each depth bin and by the scaling factor we used for the previous method to convert from number of phages in groundwater to total number of phages in the terrestrial deep subsurface.


```python
engelhardt_tot_phage_mean = (engelhardt_phage_conc_mean*water_vol['Water volume [mL]']).sum()*scaling_factor
engelhardt_tot_phage_geo_mean = (engelhardt_phage_conc_geo_mean*water_vol['Water volume [mL]']).sum()*scaling_factor

kyle_tot_phage_mean = (kyle_phage_conc_mean*water_vol['Water volume [mL]']).sum()*scaling_factor
kyle_tot_phage_geo_mean = (kyle_phage_conc_geo_mean*water_vol['Water volume [mL]']).sum()*scaling_factor
```

Our best estimate for the total number of phages is the geometric mean of the estimates based on the arithmetic and geometric means.


```python
engelhardt_tot_phage = gmean([engelhardt_tot_phage_geo_mean,engelhardt_tot_phage_mean])
kyle_tot_phage = gmean([kyle_tot_phage_geo_mean,kyle_tot_phage_mean])

print('Our best estimate for the total number of phages in the terrestrial deep subsurface based on the data from Engelhardt et al. on the relation between the number of phage-like particles and prokaryotes is %.0e' %engelhardt_tot_phage)
print('Our best estimate for the total number of phages in the terrestrial deep subsurface based on the data from Kyle et al. on the relation between the number of phage-like particles and prokaryotes is %.0e' %kyle_tot_phage)
```

    Our best estimate for the total number of phages in the terrestrial deep subsurface based on the data from Engelhardt et al. on the relation between the number of phage-like particles and prokaryotes is 5e+30
    Our best estimate for the total number of phages in the terrestrial deep subsurface based on the data from Kyle et al. on the relation between the number of phage-like particles and prokaryotes is 4e+30


In summary, the results from our five different approaches are:


```python
estimates = pd.Series([tot_phage_naive,tot_phage_pan,tot_phage_roundnew,engelhardt_tot_phage,kyle_tot_phage],
                     index = ['Naive estimate','Pan et al.','Roundnew et al.','Engelhardt et al.','Kyle et al.'])
estimates
```




    Naive estimate      3.5e+30
    Pan et al.          9.3e+29
    Roundnew et al.     5.8e+29
    Engelhardt et al.   4.6e+30
    Kyle et al.         4.3e+30
    dtype: float64



To generate our best estimate for the total number of phages in the terrestrial deep subsurface, we calculate the geometric mean of the estimates from our five different methods:


```python
best_estimate = gmean(estimates)
print('Our best estimate for the total number of phages in the the terrestrial deep subsurface is %.0e' % best_estimate)
```

    Our best estimate for the total number of phages in the the terrestrial deep subsurface is 2e+30


# Uncertainty estimate
To assess the uncertainty of our estimate of the total number of phages in the terrestrial deep subsurface, we calculate the uncertainty associated with each of the components of the estimate: The ratios between the concentration of phage-like particles and prokaryotes, the number of prokaryotes we use to derive the number phages and the scaling factor between the number of prokaryotes in groundwater and the total number of prokaryotes.

## Uncertainty of the ratio between the number of phage-like particles and prokaryotes
As a measure of the uncertainty associated with our estimate of the ratio between the concentration of phage-like particles and prokaryotes, we calculate both the intra-study uncertainty of this ratio and the interstudy uncertainty.

### Intra-study uncertainty
The only cases in which we could calculate the intra-study uncertainty of the ratio between the concentration of phage-like particles and prokaryotes are in Pan et al. and Roundnew et al. We calculate the 95% confidence interval of the geometric mean of the measurements in each of the studies as a measure of the intra-study uncertainty:


```python
pan_CI = geo_CI_calc(pan_data['Virus-to-cell ratio (VCR)'])
roundnew_CI = geo_CI_calc(roundnew_data['Virus:Bacteria ratio'])
print('The 95 percent confidence interval of the geometric mean of the values in Pan et al. is ≈%.1f-fold' % pan_CI)
print('The 95 percent confidence interval of the geometric mean of the values in Roundnew et al. is ≈%.1f-fold' % roundnew_CI)
```

    The 95 percent confidence interval of the geometric mean of the values in Pan et al. is ≈1.5-fold
    The 95 percent confidence interval of the geometric mean of the values in Roundnew et al. is ≈1.7-fold


### Interstudy uncertainty
We calculate the 95% confidence interval of the geometric mean of the estimates from our five different methodologies for measuring the ratio between the concentration of phage-like particles and prokaryotes. We use this range as a measure of the interstudy uncertainty associated with the estimate of the ratio:


```python
ratio_inter_CI = geo_CI_calc(estimates)
print('The interstudy uncertainty associated with our estimate of the ratio between the concentration of phage-like particles and prokaryotes is ≈%.1f-fold' % ratio_inter_CI)

ratio_CI = np.max([ratio_inter_CI,pan_CI,roundnew_CI])
```

    The interstudy uncertainty associated with our estimate of the ratio between the concentration of phage-like particles and prokaryotes is ≈2.3-fold


As our best projection for the uncertainty associated with the ratio between the concentration of phage-like particles and prokaryotes, we use the highest uncertainty of the intra-study and interstudy uncetainties. Thus, we project an uncertainty of ≈2.3-fold.

## Uncertainty of the number of prokaryotes we use to derive the total number of phages
In order to use the ratios between the concentration of phage-like particles and prokaryotes to estimate the total number of phages, we need to use estimates for the total number of prokaryotes in groundwater. We use two different types of estimates - one based on the arithmetic mean cell concentration at each depth bin and one based on the geometric mean cell concentration at each depth bin. We plug either estimate into the five different ratios between the concentration of phages and prokaryotes and produce an estimate for the total number of phages in groundwater. As we have five estiamtes for the ratios, and two estimates for the number of prokaryotes, we generate ten different estimates for the total number of phages in groundwater. We then use the geometric mean of the two estimates for each ratio as our best estimate for that ratio. We now assess the uncertainty of the total number of phages associated with the uncertaitny of the number of prokaryotes we use.

We calculate the 95% confidence interval of the geometric mean of the estimates of the total number of phages using arithmetic and geometric mean concentrations of prokaryotes. This yields an uncertainty for each one of the five methods to estimate the ratio between the concentration of phage-like particles and prokaryotes. We use the maximal uncertainty of those five uncertainties as our best projection for the uncertainty associated with the total number of prokaryotes.


```python
# For the naive estimate, the Pan et al. based ratio and the Roundnew et al. based ratio
# The uncertainty is the 95% confidence interval of the total number of prokaryotes in
# groundwater
tot_prok_CI = geo_CI_calc(tot_prok.sum())

# For the estimates based on the relation in Engelhardt et al. and Kyle et al., we use 
# calculate the 95% confidence interval betwee the estimates based on arithmetic and 
# geometric mean concentrations of prokaryotes
engelhardt_CI = geo_CI_calc(np.array([engelhardt_tot_phage_mean,engelhardt_tot_phage_geo_mean]))
kyle_CI = geo_CI_calc(np.array([kyle_tot_phage_mean,kyle_tot_phage_geo_mean]))

#
prok_num_CI = np.max([tot_prok_CI,engelhardt_CI,kyle_CI])
print('Our best projection for uncertainty in the total number of phages in the terrestrial deep subsurface associated with the estimate of the total number of prokaryotes in the terrestrial deep subsurface is ≈%.1f-fold' %tot_prok_CI)
```

    Our best projection for uncertainty in the total number of phages in the terrestrial deep subsurface associated with the estimate of the total number of prokaryotes in the terrestrial deep subsurface is ≈2.3-fold


## Uncertainty of the total number of prokaryotes
As we discussed above, it is not clear whether the measured ratios between the concentrations of phage-like particles and prokaryotes refer to attached or unattached cells. We take this factor into consideration in our estimate as a scaling factor that converts the measured number of phages in groundwater to an estimate for the total number of phages. Our best estimate for this factor is a geometric mean of three estimate - one which includes only phages in groundwater (and thus a scaling factor of 1), and the other two assume an attached to unattached ratios of $10^2-10^3$ as in [McMahon & Parnell](http://dx.doi.org/10.1111/1574-6941.12196). To assess the uncertainty associated with this scaling factor, we calculate the 95% confidence interval of the geometric mean of the three estimates:


```python
scaling_factor_CI = geo_CI_calc(np.array([1,100,1000]))
print('The uncertainty associated with the scaling factor from number of phages in groundwater to the total number of phages is ≈%.1f-fold' %scaling_factor_CI)
```

    The uncertainty associated with the scaling factor from number of phages in groundwater to the total number of phages is ≈53.5-fold


As our best projection of the uncertainty associated with our estimate of the total number of phages in the terrestrial deep subsurface, we combine the uncertainty projections for the three factors discussed above: the ratio between the concentration of phage-like particles and prokaryotes; the total number of prokaryotes we plug into the ratio between phages and prokaryotes; and the scaling factor between the number of phages in groundwater and the total number of phages:


```python
mul_CI = CI_prod_prop(np.array([ratio_CI,tot_prok_CI,scaling_factor_CI]))
print('Our best projection for the uncertainty associated with the total number of phages in the terrestrial deep subsurface is ≈%.0f-fold' %mul_CI)
```

    Our best projection for the uncertainty associated with the total number of phages in the terrestrial deep subsurface is ≈64-fold


Our final parameters are:


```python

print('Our best estimate for the total number of phages in the terrestrial deep subsurface: %.0e' % best_estimate)
print('Uncertainty associated with the estiamte of the total number of phages in the terrestrial deep subsurface: %.0f-fold' % mul_CI)

old_results = pd.read_excel('../phage_num_estimate.xlsx')
result = old_results.copy()
result.loc[2] = pd.Series({
                'Parameter': 'Total number of phages in the terrestrial deep subsurface',
                'Value': best_estimate,
                'Units': 'Number of individuals',
                'Uncertainty': mul_CI
                })

result.to_excel('../phage_num_estimate.xlsx',index=False)

```

    Our best estimate for the total number of phages in the terrestrial deep subsurface: 2e+30
    Uncertainty associated with the estiamte of the total number of phages in the terrestrial deep subsurface: 64-fold


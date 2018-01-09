
# Estimating the fraction of archaea out of the total marine deep subsurface prokaryote population

In order to estimate the fraction of archaea out of the total population of marine deep subsurface bacteria and archaea, we rely of three sources of data. Two of those sources are measurements made in the terrestrial deep subsurface of the fraction of archaea using two independent methods: 16S rDNA sequencing (FISH) and quantitative PCR (qPCR). For each method we collect several studies which used the method to measure the fraction of archaea out of the total population of bacteria and archaea in the terrestrial deep subsurface. We calculate the geometric means of samples within each study. We then calculate the geometric mean of the average estimates from each study using the same method to generate a characteristic estimate for the fraction of archaea out of the total population of bacteria and archaea in the terrestrial deep subsurface for each method. 

## 16S rDNA sequencing-based estimate
For our 16S rDNA sequencing-based estimate we rely on data from [Rempfert et al.](http://dx.doi.org/10.3389/fmicb.2017.00056), [Lau et al.](http://dx.doi.org/10.1073/pnas.1612244113), [Osburn et al.](http://dx.doi.org/10.3389/fmicb.2014.00610), and [Simkus et al.](http://dx.doi.org/10.1016/j.gca.2015.10.003). Here is a sample of the data:


```python
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '../../../statistics_helper')
from fraction_helper import *

pd.options.display.float_format = '{:,.1e}'.format

# Define a function that will calculate the geometric mean of fractions for each bin of a groupby
def frac_geo_mean_groupby(input):
    return frac_mean(input['Archaea fraction'])

# Define a function that will calculate the CI of geometric mean of fractions for each bin of a groupby
def frac_CI_groupby(input):
    return frac_CI(input['Archaea fraction'])


seq_data = pd.read_excel('terrestrial_deep_subsurface_arch_frac_data.xlsx','16S rDNA sequencing')
seq_data.head()
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
      <th>Study</th>
      <th>Link</th>
      <th>Well</th>
      <th>Year</th>
      <th>Archaea fraction</th>
      <th>Depth</th>
      <th>Rock type</th>
      <th>Location</th>
      <th>Remarks</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Rempfert et al.</td>
      <td>http://dx.doi.org/10.3389/fmicb.2017.00056</td>
      <td>NSHQ14</td>
      <td>2014</td>
      <td>4.3e-03</td>
      <td>1.8e+01</td>
      <td>Peridotite</td>
      <td>Oman</td>
      <td>Calculated from Table 3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Rempfert et al.</td>
      <td>http://dx.doi.org/10.3389/fmicb.2017.00056</td>
      <td>NSHQ14</td>
      <td>2015</td>
      <td>7.0e-04</td>
      <td>2.0e+01</td>
      <td>Peridotite</td>
      <td>Oman</td>
      <td>Calculated from Table 3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Rempfert et al.</td>
      <td>http://dx.doi.org/10.3389/fmicb.2017.00056</td>
      <td>NSHQ14</td>
      <td>2016</td>
      <td>2.8e-01</td>
      <td>7.0e+01</td>
      <td>Peridotite</td>
      <td>Oman</td>
      <td>Calculated from Table 3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Rempfert et al.</td>
      <td>http://dx.doi.org/10.3389/fmicb.2017.00056</td>
      <td>WAB56</td>
      <td>2015</td>
      <td>3.8e-02</td>
      <td>1.2e+01</td>
      <td>Peridotite</td>
      <td>Oman</td>
      <td>Calculated from Table 3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Rempfert et al.</td>
      <td>http://dx.doi.org/10.3389/fmicb.2017.00056</td>
      <td>WAB56</td>
      <td>2016</td>
      <td>3.7e-03</td>
      <td>5.0e+01</td>
      <td>Peridotite</td>
      <td>Oman</td>
      <td>Calculated from Table 3</td>
    </tr>
  </tbody>
</table>
</div>



We calculate the geometric mean of the fraction of archaea out of the total population of bacteria and archea for each study:


```python
seq_bin = seq_data.groupby('Study')

seq_study_mean = seq_bin.apply(frac_geo_mean_groupby)
seq_study_mean
```




    Study
    Lau et al.        1.9e-02
    Osburn et al.     6.3e-02
    Rempfert et al.   2.6e-02
    Simkus et al.     1.5e-02
    dtype: float64



We calculate the geometric mean of the average fractions from each study:


```python
seq_mean = frac_mean(seq_study_mean)
print('The characteristic 16S rDNA sequencing-based fraction of archaea out of the total population of bacteria and archaea in the terrestrial deep susurface is ' + '{:,.1f}%'.format(seq_mean*100))
```

    The characteristic 16S rDNA sequencing-based fraction of archaea out of the total population of bacteria and archaea in the terrestrial deep susurface is 2.6%


## qPCR-based estimate
For our qPCR-based estimate we rely on data from [Purkamo et al.](https://helda.helsinki.fi/handle/10138/165462), [Takai et al.](http://dx.doi.org/10.1128/AEM.67.21.5750-5760.2001), and [Bomberg et al.](http://dx.doi.org/10.5194/bg-13-6031-2016). Here is a sample of the data:


```python
qpcr_data = pd.read_excel('terrestrial_deep_subsurface_arch_frac_data.xlsx','qPCR')
qpcr_data.head()
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
      <th>Study</th>
      <th>Link</th>
      <th>Well</th>
      <th>Year</th>
      <th>Archaea fraction</th>
      <th>Depth</th>
      <th>Rock type</th>
      <th>Location</th>
      <th>Remarks</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Purkamo et al.</td>
      <td>https://helda.helsinki.fi/handle/10138/165462</td>
      <td>180</td>
      <td>2009-2011</td>
      <td>1.2e-03</td>
      <td>180</td>
      <td>Mica schist, biotite gneiss</td>
      <td>Outokumpu, Finland</td>
      <td>Calculated from Table 2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Purkamo et al.</td>
      <td>https://helda.helsinki.fi/handle/10138/165462</td>
      <td>500</td>
      <td>2009-2011</td>
      <td>4.6e-05</td>
      <td>500</td>
      <td>Chlorite–sericite schist</td>
      <td>Outokumpu, Finland</td>
      <td>Calculated from Table 2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Purkamo et al.</td>
      <td>https://helda.helsinki.fi/handle/10138/165462</td>
      <td>967</td>
      <td>2009-2011</td>
      <td>3.9e-03</td>
      <td>967</td>
      <td>Mica schist, chlorite–sericite schist</td>
      <td>Outokumpu, Finland</td>
      <td>Calculated from Table 2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Purkamo et al.</td>
      <td>https://helda.helsinki.fi/handle/10138/165462</td>
      <td>2260</td>
      <td>2009-2011</td>
      <td>2.5e-02</td>
      <td>2260</td>
      <td>Biotite gneiss</td>
      <td>Outokumpu, Finland</td>
      <td>Calculated from Table 2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Takai et al.</td>
      <td>http://dx.doi.org/10.1128/AEM.67.21.5750-5760....</td>
      <td>F1</td>
      <td>NaN</td>
      <td>1.8e-01</td>
      <td>2700</td>
      <td>Driefontein</td>
      <td>Witwatersrand Basin, South Africa.</td>
      <td>From first paragraph of Archaeal rDNA abundanc...</td>
    </tr>
  </tbody>
</table>
</div>



We calculate the geometric mean of the fraction of archaea out of the total population of bacteria and archea for each study:


```python
qpcr_bin = qpcr_data.groupby('Study')

qpcr_study_mean = qpcr_bin.apply(frac_geo_mean_groupby)
qpcr_study_mean
```




    Study
    Bomberg et al.   4.3e-02
    Purkamo et al.   1.5e-03
    Takai et al.     4.5e-02
    dtype: float64



We calculate the geometric mean of the average fractions from each study:


```python
qpcr_mean = frac_mean(qpcr_study_mean)
print('The characteristic qPCR-based fraction of archaea out of the total population of bacteria and archaea in the terrestrial deep susurface is ' + '{:,.1f}%'.format(qpcr_mean*100))
```

    The characteristic qPCR-based fraction of archaea out of the total population of bacteria and archaea in the terrestrial deep susurface is 1.5%


Due to the scarcity of data in the terrestrial deep subsurface, we use as a third source of data our estimate for the fraction of archaea out of the total population of bacteria and archea in subseafloor sediments.

Our best estimate for the fraction of archaea out of the total population of bacteria and archaea is the geometric mean of these three sources of data:


```python
# As a third data source we use our estimate for the fraction of archaea out of the total population of bacteria
# and archaea in subseafloor sediments.
subseafloor_sed_arch_frac = 0.35

# Calculate the geometric mean of the three data sources
best_estimate = frac_mean(np.array([qpcr_mean, seq_mean, subseafloor_sed_arch_frac]))

print('Our best estimate for the fraction of archaea out of the total population of bacteria and archaea in the terrestrial deep subsurface is ' + '{:,.0f}%'.format(best_estimate*100))
```

    Our best estimate for the fraction of archaea out of the total population of bacteria and archaea in the terrestrial deep subsurface is 6%


# Uncertainty analysis
In order to assess the uncertainty associated with our estimate for the fraction of marine archaea out of the total population of bacteria and archaea in the terrestrial deep subsurface, we gather all possible indices of uncertainty. We compare the uncertainty of values within each one of the methods and the uncertainty stemming from the variability of the values provided by the two methods. 

## Intra-study uncertainty 
### 16S rDNA sequencing-based method
We calculate the intra-study 95% confidence inteval for the geometric mean of the values for the fraction of archaea out of the total population of bacteria and archaea measured using 16S rDNA seuqencing.


```python
seq_arc_CI = seq_bin.apply(frac_CI_groupby)

seq_data_bac = seq_data.copy()
seq_data_bac['Archaea fraction'] = 1.- seq_data_bac['Archaea fraction']
seq_bin_bac = seq_data_bac.groupby('Study')
seq_bac_CI = seq_bin_bac.apply(frac_CI_groupby)


print('The intra-study uncertainty of the 16S rDNA sequencing-based estimate of the fraction of archaea out of the population of bacteria nad archaea are:')
print(seq_arc_CI)
print('The intra-study uncertainty of the 16S rDNA sequencing-based estimate of the fraction of bacteria out of the population of bacteria nad archaea are:')
print(seq_bac_CI)
```

    The intra-study uncertainty of the 16S rDNA sequencing-based estimate of the fraction of archaea out of the population of bacteria nad archaea are:
    Study
    Lau et al.            nan
    Osburn et al.     2.0e+00
    Rempfert et al.   2.4e+00
    Simkus et al.     3.0e+00
    dtype: float64
    The intra-study uncertainty of the 16S rDNA sequencing-based estimate of the fraction of bacteria out of the population of bacteria nad archaea are:
    Study
    Lau et al.            nan
    Osburn et al.     1.1e+00
    Rempfert et al.   1.0e+00
    Simkus et al.     1.0e+00
    dtype: float64


    /usr/local/lib/python3.5/dist-packages/numpy/lib/function_base.py:4116: RuntimeWarning: Invalid value encountered in percentile
      interpolation=interpolation)


### qPCR-based method
We calculate the intra-study 95% confidence inteval for the geometric mean of the values for the fraction of archaea out of the total population of bacteria and archaea measured using qPCR.


```python
qpcr_arc_CI = qpcr_bin.apply(frac_CI_groupby)

qpcr_data_bac = qpcr_data.copy()
qpcr_data_bac['Archaea fraction'] = 1.- qpcr_data_bac['Archaea fraction']
qpcr_bin_bac = qpcr_data_bac.groupby('Study')
qpcr_bac_CI = qpcr_bin_bac.apply(frac_CI_groupby)


print('The intra-study uncertainty of the qPCR-based estimate of the fraction of archaea out of the population of bacteria nad archaea are:')
print(qpcr_arc_CI)
print('The intra-study uncertainty of the qPCR-based estimate of the fraction of bacteria out of the population of bacteria nad archaea are:')
print(qpcr_bac_CI)
```

    The intra-study uncertainty of the qPCR-based estimate of the fraction of archaea out of the population of bacteria nad archaea are:
    Study
    Bomberg et al.   3.5e+00
    Purkamo et al.   1.2e+01
    Takai et al.     2.0e+01
    dtype: float64
    The intra-study uncertainty of the qPCR-based estimate of the fraction of bacteria out of the population of bacteria nad archaea are:
    Study
    Bomberg et al.   1.1e+00
    Purkamo et al.   1.0e+00
    Takai et al.     1.5e+00
    dtype: float64


## Interstudy uncertainty 
### 16S rDNA sequencing-based method
We calculate the interstudy 95% confidence inteval for the geometric mean of the average values from each study for the fraction of archaea out of the total population of bacteria and archaea measured using 16S rDNA sequencing.


```python
inter_seq_arc_CI = frac_CI(seq_study_mean)
inter_seq_bac_CI = frac_CI(1-seq_study_mean)
print('The interstudy uncertainty of the 16S rDNA sequencing-based estimate of the fraction of archaea out of the population of bacteria nad archaea is ≈%.1f-fold' % inter_seq_arc_CI)
print('The interstudy uncertainty of the 16S rDNA sequencing-based estimate of the fraction of bacteria out of the population of bacteria nad archaea is ≈%.1f-fold' % inter_seq_bac_CI)
```

    The interstudy uncertainty of the 16S rDNA sequencing-based estimate of the fraction of archaea out of the population of bacteria nad archaea is ≈1.9-fold
    The interstudy uncertainty of the 16S rDNA sequencing-based estimate of the fraction of bacteria out of the population of bacteria nad archaea is ≈1.0-fold


### qPCR-based method
We calculate the interstudy 95% confidence inteval for the geometric mean of the average values from each study for the fraction of archaea out of the total population of bacteria and archaea measured using qPCR.


```python
inter_qpcr_arc_CI = frac_CI(qpcr_study_mean)
inter_qpcr_bac_CI = frac_CI(1-qpcr_study_mean)
print('The interstudy uncertainty of the qPCR-based estimate of the fraction of archaea out of the population of bacteria nad archaea is ≈%.1f-fold' % inter_qpcr_arc_CI)
print('The interstudy uncertainty of the qPCR-based estimate of the fraction of bacteria out of the population of bacteria nad archaea is ≈%.1f-fold' % inter_qpcr_bac_CI)
```

    The interstudy uncertainty of the qPCR-based estimate of the fraction of archaea out of the population of bacteria nad archaea is ≈8.1-fold
    The interstudy uncertainty of the qPCR-based estimate of the fraction of bacteria out of the population of bacteria nad archaea is ≈1.1-fold


## Inter-method uncertainty
We calculate the interstudy 95% confidence inteval for the geometric mean of the estimates from the three different sources - the 16S rDNA sequencing-based estimate, the pPCR-based estiamte and the estimate for the fraction of archea out of the total population of bacteria and archaea in subseafloor sediments.


```python
inter_method_arc_CI = frac_CI(np.array([seq_mean,qpcr_mean,subseafloor_sed_arch_frac]))
inter_method_bac_CI = frac_CI(1-np.array([seq_mean,qpcr_mean,subseafloor_sed_arch_frac]))
print('The inter-method uncertainty of the estimate of the fraction of archaea out of the population of bacteria nad archaea is ≈%.1f-fold' % inter_method_arc_CI)
print('The inter-method uncertainty of the estimate of the fraction of bacteria out of the population of bacteria nad archaea is ≈%.1f-fold' % inter_method_bac_CI)
```

    The inter-method uncertainty of the estimate of the fraction of archaea out of the population of bacteria nad archaea is ≈7.3-fold
    The inter-method uncertainty of the estimate of the fraction of bacteria out of the population of bacteria nad archaea is ≈1.2-fold


As our best estimates for the uncertainty associated with the fraction of archaea and bacteria out of the total population of terrestrial deep subsurface bacteria and archaea, we use the highest uncertainty out of the available set pf uncertainties we collected.

The highest uncertainty for the fraction of archaea is the intra-study uncertainty of the Takai et al. study, which is ≈20-fold. Similarly, the highest uncertainty for the fraction of bacteria is intra-study uncertainty of the Takai et al. study, which is ≈1.5-fold.

Our final parameters are:


```python
# Take the maximum uncertainty as our best projection of uncertainty
arc_mul_CI = np.max([seq_arc_CI.max(),qpcr_arc_CI.max(),inter_seq_arc_CI,inter_method_arc_CI])
bac_mul_CI = np.max([seq_bac_CI.max(),qpcr_bac_CI.max(),inter_seq_bac_CI,inter_qpcr_bac_CI,inter_method_bac_CI])

print('Fraction of archaea out of the total population of terrestrial deep subsurface bacteria and archaea: %.0f percent' %(best_estimate*100))
print('Fraction of bacteria out of the total population of terrestrial deep subsurface bacteria and archaea: %.0f percent' %(100.-best_estimate*100))
print('Uncertainty associated with the fraction of marine archaea: %.1f-fold' % arc_mul_CI)
print('Uncertainty associated with the fraction of marine bacteria: %.1f-fold' % bac_mul_CI)

old_results = pd.read_excel('../terrestrial_deep_subsurface_prok_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[1] = pd.Series({
                'Parameter': 'Fraction of archaea',
                'Value': "{0:.2f}".format(best_estimate),
                'Units': 'Unitless',
                'Uncertainty': "{0:.1f}".format(arc_mul_CI)
                })

result.loc[2] = pd.Series({
                'Parameter': 'Fraction of bacteria',
                'Value': "{0:.2f}".format(1.0 - best_estimate),
                'Units': 'Unitless',
                'Uncertainty': "{0:.1f}".format(bac_mul_CI)
                })


result.to_excel('../terrestrial_deep_subsurface_prok_biomass_estimate.xlsx',index=False)
```

    Fraction of archaea out of the total population of terrestrial deep subsurface bacteria and archaea: 6 percent
    Fraction of bacteria out of the total population of terrestrial deep subsurface bacteria and archaea: 94 percent
    Uncertainty associated with the fraction of marine archaea: 19.6-fold
    Uncertainty associated with the fraction of marine bacteria: 1.5-fold


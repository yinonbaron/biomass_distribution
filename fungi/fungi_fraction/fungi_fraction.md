
# Estimating the fraction of fungi out of the biomass of soil microbes
Our estimate for the fraction of fungi out of the biomass of soil microbes is based on a study by [Joergensen & Wichern ](http://dx.doi.org/10.1016/j.soilbio.2008.08.017). Joergensen & Wichern survey the fraction of fungi out of the total microbial biomass using several independent methods. The data in Joergensen & Wichern contains measurements of the fraction of fungi out of the total biomass of soil microbes in four differennt soil types - arable soil, forest soil, grassland soil and litter. We rely on measurement collected in these four soil types using two independent methods - microscopy and measurement of cell wall components.

Here is a sample of the data from Joergensen & Wichern:


```python
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '../../statistics_helper')
from fraction_helper import *
pd.options.display.float_format = '{:,.3f}'.format

data = pd.read_excel('fungi_fraction_data.xlsx')
data.head()
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
      <th>Reference</th>
      <th>Fraction</th>
      <th>N</th>
      <th>Method</th>
      <th>Type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Shields et al. (1973)</td>
      <td>0.860</td>
      <td>15</td>
      <td>Microscopy</td>
      <td>Arable</td>
    </tr>
    <tr>
      <th>1</th>
      <td>West (1986)</td>
      <td>0.750</td>
      <td>5</td>
      <td>Microscopy</td>
      <td>Arable</td>
    </tr>
    <tr>
      <th>2</th>
      <td>West (1986)</td>
      <td>0.580</td>
      <td>10</td>
      <td>Microscopy</td>
      <td>Forest</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Ingham and Horton (1987)</td>
      <td>0.090</td>
      <td>10</td>
      <td>Microscopy</td>
      <td>Arable</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Neely et al. (1991)</td>
      <td>0.640</td>
      <td>72</td>
      <td>Microscopy</td>
      <td>Litter</td>
    </tr>
  </tbody>
</table>
</div>



Our general methodology for calculating the fraction of fungi out of the biomass of soil microbes is the following. We calculate the geometric mean of all values reported from the same soil type using the same method. This gives us estimates for characteric fraction of fungi in each soil type for each method. 


```python
def groupby_geo_frac_mean(input):
    return frac_mean(input['Fraction'],weights=input['N'])

type_method_mean = data.groupby(['Method','Type']).apply(groupby_geo_frac_mean).unstack(level=0)
type_method_mean
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
      <th>Method</th>
      <th>Microscopy</th>
      <th>glucosamine and muramic acid</th>
    </tr>
    <tr>
      <th>Type</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Arable</th>
      <td>0.312</td>
      <td>0.747</td>
    </tr>
    <tr>
      <th>Forest</th>
      <td>0.476</td>
      <td>0.714</td>
    </tr>
    <tr>
      <th>Grassland</th>
      <td>0.251</td>
      <td>0.687</td>
    </tr>
    <tr>
      <th>Litter</th>
      <td>0.643</td>
      <td>0.784</td>
    </tr>
  </tbody>
</table>
</div>



We then calculate the geometric mean of the characteristic fractions from different soil types using the same method. This gives us a characteristic fraction of fungi for each of the two methods.


```python
method_mean = type_method_mean.apply(frac_mean)
method_mean
```




    Method
    Microscopy                     0.414
    glucosamine and muramic acid   0.735
    dtype: float64



In the last stage, we calculate the geometric mean of the characteristic values from the two methods. We use the geometric mean as our best estimate for the fraction of fungi out of the total biomass of soil microbes.


```python
best_estimate = frac_mean(method_mean)
print('Our best estimate for the fraction of fungi out of the total biomass of fungi is ≈' + '{:,.0f}%'.format(best_estimate*100))
```

    Our best estimate for the fraction of fungi out of the total biomass of fungi is ≈58%


# Uncertainty analysis

To calculate the uncertainty associated with the estimate for the fraction of fungi out of the total biomass of number of of bacteria and archaea, we first collect all available uncertainties and then take the largest value as our best projection for the uncertainty.

**Variability of studies using the same method and done in the same soil type** <br>
We calculate the 95% confidence confidence interval of the values reported by studies performed in the same soil type and using the same method.



```python
def groupby_frac_CI(input):
    return frac_CI(input['Fraction'])

type_method_CI = data.groupby(['Method','Type']).apply(groupby_frac_CI).unstack(level=0)
type_method_CI
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
      <th>Method</th>
      <th>Microscopy</th>
      <th>glucosamine and muramic acid</th>
    </tr>
    <tr>
      <th>Type</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Arable</th>
      <td>2.893</td>
      <td>1.051</td>
    </tr>
    <tr>
      <th>Forest</th>
      <td>1.255</td>
      <td>1.189</td>
    </tr>
    <tr>
      <th>Grassland</th>
      <td>2.506</td>
      <td>1.097</td>
    </tr>
    <tr>
      <th>Litter</th>
      <td>1.210</td>
      <td>1.145</td>
    </tr>
  </tbody>
</table>
</div>



**Variability of fractions from different soil types measured using the same method** <br>
We calculate the 95% confidence interval of the characteristic values from each soil type measured in the same method.


```python
intra_method_CI = type_method_mean.apply(frac_CI)
intra_method_CI
```




    Method
    Microscopy                     1.554
    glucosamine and muramic acid   1.057
    dtype: float64



**Variability of fraction measured using different methods** <br>
We calculate the 95% confidence interval of the characteristic values from each method.


```python
inter_method_CI = frac_CI(method_mean)
print('The 95' + '%'+' confidence interval of the characteristic values from each method is ≈%.1f-fold' % inter_method_CI)

```

    The 95% confidence interval of the characteristic values from each method is ≈1.8-fold


We choose the highest uncertainty among the uncertianties we collected which is ≈3-fold, as our projection for the uncertainty of the fraction of fungi out of the total biomass of soil microbes.
Our final parameters are:


```python
mul_CI = np.max([type_method_CI.values.flatten().max(),intra_method_CI.max(),inter_method_CI])
print('Fraction of fungi out of the total biomass of microbes:' +'{:.1f}%'.format(best_estimate*100))
print('Uncertainty associated with the estimate of the total biomass of soil microbes ≈%.1f-fold' % mul_CI)

old_results = pd.read_excel('../fungi_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[1] = pd.Series({
                'Parameter': 'Fraction of fungi ou out the total biomass of soil microbes',
                'Value': '{0:.1f}'.format(best_estimate),
                'Units': 'Unitless',
                'Uncertainty': "{0:.1f}".format(mul_CI)
                })

result.to_excel('../fungi_biomass_estimate.xlsx',index=False)
```

    Fraction of fungi out of the total biomass of microbes:58.3%
    Uncertainty associated with the estimate of the total biomass of soil microbes ≈2.9-fold



# Estimating the carbon content of marine bacteria and archaea

In order to estimate the characteristic carbon content of marine bacteria and archaea, we collected data on the carbon content of marine prokaryotes from 5 studies. Here is a summary of the data collected


```python
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '../../../statistics_helper')
from CI_helper import *
pd.options.display.float_format = '{:,.1f}'.format
summary = pd.read_excel('marine_prok_carbon_content_data.xlsx','Summary')
summary.head()
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
      <th>Link to paper</th>
      <th>fg C cell-1</th>
      <th>Location</th>
      <th>Intra-study uncertainty</th>
      <th>remarks</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Lee and Fuhrman (1987)</td>
      <td>https://www.ncbi.nlm.nih.gov/pubmed/16347362</td>
      <td>20.0</td>
      <td>NW-atlantic</td>
      <td>1.1</td>
      <td>standard error of 0.8. We use two standard err...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Ducklow and Carlson (1992)</td>
      <td>http://dx.doi.org/10.1007/978-1-4684-7609-5_3</td>
      <td>12.2</td>
      <td>Oceans</td>
      <td>1.1</td>
      <td>mean and standard error calculated in sheet2 b...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Gundersen et al. (2002)</td>
      <td>http://onlinelibrary.wiley.com/doi/10.4319/lo....</td>
      <td>7.7</td>
      <td>N-Atlantic</td>
      <td>1.1</td>
      <td>mean and standard error calculated in sheet3 b...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Carlson et al. (1999)</td>
      <td>http://dx.doi.org/10.3354/ame019229</td>
      <td>7.7</td>
      <td>Antarctica</td>
      <td>1.3</td>
      <td>range of 5.5-9.8</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Fukuda et al. (1998)</td>
      <td>http://aem.asm.org/cgi/pmidlookup?view=long&amp;pm...</td>
      <td>12.4</td>
      <td>Pacific Ocean</td>
      <td>1.4</td>
      <td>std of 6.3 and sample size of 6 equals standar...</td>
    </tr>
  </tbody>
</table>
</div>



We use the geometric mean of the carbon content from each study as our best estimate for the carbon content of marine bacteria and archaea.


```python
best_estimate = 10**(np.log10(summary['fg C cell-1']).mean())
print('Our best estimate for the carbon content of marine bacteria and arcaea is %0.1f fg C cell^-1' % best_estimate)
```

    Our best estimate for the carbon content of marine bacteria and arcaea is 11.2 fg C cell^-1


# Uncertainty analysis

In order to assess the uncertainty associated with our estimate of the carbon content of marine bacteria and archaea, we survey all availabe measures of uncertainty.

## Intra-study uncertainty
We collected the uncertainties reported in each of the studies. Below is a list of the uncertainties reported in each of the studies. The highest uncertainty reported is lower than 1.5-fold.


```python
print(summary[['Reference','Intra-study uncertainty']])
```

                        Reference  Intra-study uncertainty
    0      Lee and Fuhrman (1987)                      1.1
    1  Ducklow and Carlson (1992)                      1.1
    2     Gundersen et al. (2002)                      1.1
    3       Carlson et al. (1999)                      1.3
    4        Fukuda et al. (1998)                      1.4


## Interstudy uncertainty
We estimate the 95% multiplicative confidence interval around the geometric mean of the values from the different studies. 


```python
mul_CI = geo_CI_calc(summary['fg C cell-1'])
print('The interstudy uncertainty is ≈%.1f-fold' % mul_CI)
```

    The interstudy uncertainty is ≈1.4-fold


We thus take the highest uncertainty from our collection of intra-study and interstudy uncertainties which is ≈1.4-fold.
Our final parameters are:


```python
print('Carbon content of marine bacteria and archaea: %.1f fg C cell^-1' % best_estimate)
print('Uncertainty associated with the carbon content of marine bacteria and archaea: %.1f-fold' % mul_CI)

old_results = pd.read_excel('../marine_prok_biomass_estimate.xlsx')
result = old_results.copy()
result.loc[1] = pd.Series({
                'Parameter': 'Carbon content',
                'Value': "{0:.1f}".format(best_estimate),
                'Units': 'fg C cell^-1',
                'Uncertainty': "{0:.1f}".format(mul_CI)
                })

result.to_excel('../marine_prok_biomass_estimate.xlsx',index=False)

```

    Carbon content of marine bacteria and archaea: 11.2 fg C cell^-1
    Uncertainty associated with the carbon content of marine bacteria and archaea: 1.4-fold


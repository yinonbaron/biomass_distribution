
# Estimating the total biomass of marine archaea and bacteria

We use our best estimates for the total number of marine prokaryotes, the carbon content of marine prokaryotes and the fraction of marine archaea and bacteria out of the total population of marine prokaryotes to estimate the total biomass of marine bacteria and archaea


```python
import numpy as np
import pandas as pd
pd.options.display.float_format = '{:,.1e}'.format
import sys
sys.path.insert(0, '../../statistics_helper')
from CI_helper import *
results = pd.read_excel('marine_prok_biomass_estimate.xlsx')

```

These are our best estimates for the different parameters required for the estimate, along with the associated uncertainties


```python
results.head()
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
      <th>Parameter</th>
      <th>Value</th>
      <th>Units</th>
      <th>Uncertainty</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Total number of marine bacteria and archaea</td>
      <td>1.2e+29</td>
      <td>Cells</td>
      <td>1.5e+00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Carbon content</td>
      <td>1.1e+01</td>
      <td>fg C cell^-1</td>
      <td>1.4e+00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Fraction of archaea</td>
      <td>2.0e-01</td>
      <td>Unitless</td>
      <td>2.2e+00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Fraction of bacteria</td>
      <td>8.0e-01</td>
      <td>Unitless</td>
      <td>1.3e+00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Fraction of the total biomass of marine bacter...</td>
      <td>2.3e-01</td>
      <td>Unitless</td>
      <td>4.3e+00</td>
    </tr>
  </tbody>
</table>
</div>



We multiply all the relevant parameters to arrive at our best estimate for the biomass of marine archaea and bacteria, and propagate the uncertainties associated with each parameter to calculate the uncertainty associated with the estimate for the total biomass


```python
# Calculate the total biomass of marine archaea and bacteria
total_arch_biomass = results['Value'][0]*results['Value'][1]*(1+results['Value'][4])*1e-15*results['Value'][2]
total_bac_biomass = results['Value'][0]*results['Value'][1]*(1+results['Value'][4])*1e-15*results['Value'][3]

print('Our best estimate for the total biomass of marine archaea is %.1f Gt C' %(total_arch_biomass/1e15))
print('Our best estimate for the total biomass of marine bacteria is %.1f Gt C' %(total_bac_biomass/1e15))

# Propagate the uncertainty in the total biomass of bacteria and archaea
prok_biomass_CI = CI_sum_prop(estimates=np.array([results['Value'][0]*results['Value'][1], results['Value'][0]*results['Value'][1]*results['Value'][4]]), mul_CIs=np.array([CI_prod_prop(results['Uncertainty'][:2]),results['Uncertainty'][4]]))

# Propagate the uncertainty associated with each parameter to the final estimate
arch_biomass_uncertainty = CI_prod_prop(np.array([prok_biomass_CI,results['Uncertainty'][2]]))
bac_biomass_uncertainty = CI_prod_prop(np.array([prok_biomass_CI,results['Uncertainty'][3]]))

print('The uncertainty associated with the estimate for the biomass of archaea is %.1f-fold' %arch_biomass_uncertainty)
print('The uncertainty associated with the estimate for the biomass of bacteria is %.1f-fold' %bac_biomass_uncertainty)

```

    Our best estimate for the total biomass of marine archaea is 0.3 Gt C
    Our best estimate for the total biomass of marine bacteria is 1.4 Gt C
    The uncertainty associated with the estimate for the biomass of archaea is 2.6-fold
    The uncertainty associated with the estimate for the biomass of bacteria is 1.8-fold



# Estimating the total biomass of terrestrial deep subsurface archaea and bacteria

We use our best estimates for the total biomass of terrestrial deep subsurface prokaryotes and the fraction of archaea and bacteria out of the total population of terrestrial deep subsurface prokaryotes to estimate the total biomass of terrestrial deep subsurface bacteria and archaea.


```python
import numpy as np
import pandas as pd
pd.options.display.float_format = '{:,.1e}'.format
import sys
sys.path.insert(0, '../../statistics_helper')
from CI_helper import *
results = pd.read_excel('terrestrial_deep_subsurface_prok_biomass_estimate.xlsx')
results
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
      <td>Total biomass of bacteria and archaea in the t...</td>
      <td>6.2e+16</td>
      <td>g C</td>
      <td>2.0e+01</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Fraction of archaea</td>
      <td>6.0e-02</td>
      <td>Unitless</td>
      <td>2.0e+01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Fraction of bacteria</td>
      <td>9.4e-01</td>
      <td>Unitless</td>
      <td>1.5e+00</td>
    </tr>
  </tbody>
</table>
</div>



We multiply all the relevant parameters to arrive at our best estimate for the biomass of terrestrial deep subsurface archaea and bacteria, and propagate the uncertainties associated with each parameter to calculate the uncertainty associated with the estimate for the total biomass.


```python
# Calculate the total biomass of marine archaea and bacteria
total_arch_biomass = results['Value'][0]*results['Value'][1]
total_bac_biomass = results['Value'][0]*results['Value'][2]

print('Our best estimate for the total biomass of terrestrial deep subsurface archaea is %.0f Gt C' %(total_arch_biomass/1e15))
print('Our best estimate for the total biomass of terrestrial deep subsurface bacteria is %.0f Gt C' %(total_bac_biomass/1e15))

# Propagate the uncertainty associated with each parameter to the final estimate

arch_biomass_uncertainty = CI_prod_prop(results['Uncertainty'][:2])
bac_biomass_uncertainty = CI_prod_prop(results.iloc[[0,2]]['Uncertainty'])

print('The uncertainty associated with the estimate for the biomass of archaea is %.1f-fold' %arch_biomass_uncertainty)
print('The uncertainty associated with the estimate for the biomass of bacteria is %.1f-fold' %bac_biomass_uncertainty)



```

    Our best estimate for the total biomass of terrestrial deep subsurface archaea is 4 Gt C
    Our best estimate for the total biomass of terrestrial deep subsurface bacteria is 58 Gt C
    The uncertainty associated with the estimate for the biomass of archaea is 68.2-fold
    The uncertainty associated with the estimate for the biomass of bacteria is 20.6-fold


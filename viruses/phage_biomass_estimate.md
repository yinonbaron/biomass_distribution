
# Estimating the biomass of phages
Our estimate of the total biomass of phages relies upon the estimates for the total number of phages and the carbon content of a single phage which we derived in the relevant sections

These are our best estimates for the different parameters required for the estimate, along with the associated uncertainties:


```python
import pandas as pd
import sys
sys.path.insert(0,'../statistics_helper/')
from CI_helper import *
pd.options.display.float_format = '{:,.0e}'.format

# Load estimates for the total number of phages and for the carbon cont
estimate = pd.read_excel('phage_biomass_estimate.xlsx')
estimate
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
      <td>Total number of phages</td>
      <td>1e+31</td>
      <td>Number of individuals</td>
      <td>1e+01</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Carbon content of a single phage</td>
      <td>2e-17</td>
      <td>g C per individual</td>
      <td>2e+00</td>
    </tr>
  </tbody>
</table>
</div>



In order to estimate the total biomass of phages, we multiply our estimate of the total number of phages by our estimate of the carbon content of a single phage.


```python
best_estimate = estimate['Value'].prod()

print('Our best estimate for the total biomass of phages is %.1f Gt C' %(best_estimate/1e15))
```

    Our best estimate for the total biomass of phages is 0.2 Gt C


We propagate the uncertainties associated with each of the parameters to project the uncertainty of our estimate of the total biomass of phages:


```python
mul_CI = CI_prod_prop(estimate['Uncertainty'])

print('Our best projection for the uncertainty associated with our estiamte of the biomass of phages is %.1f-fold' %mul_CI)
```

    Our best projection for the uncertainty associated with our estiamte of the biomass of phages is 15.4-fold


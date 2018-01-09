
# Estimating the biomass of Annelids
To estimate the total biomass of annelids, we rely on data collected in a recent study by [Fierer et al.](http://dx.doi.org/10.1111/j.1461-0248.2009.01360.x). Fierer et al. collected data on the biomass density of two major groups on annelids (Enchytraeids & Earthworms) in different biomes. Here is a sample from the data:


```python
import pandas as pd
import numpy as np
from scipy.stats import gmean

# Load the data taken from Fierer et al.
data = pd.read_excel('annelid_biomass_data.xlsx','Fierer',skiprows=1)
data
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
      <th>Biome</th>
      <th>Average biomass density [g C m^-2]</th>
      <th>Median biomass density [g C m^-2]</th>
      <th>Taxon</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Boreal forests</td>
      <td>0.32</td>
      <td>0.28</td>
      <td>Enchytraeids</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Desert</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>Enchytraeids</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Temperate coniferous forest</td>
      <td>0.80</td>
      <td>0.56</td>
      <td>Enchytraeids</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Temeprate deciduous forest</td>
      <td>0.64</td>
      <td>0.30</td>
      <td>Enchytraeids</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Temprate grassland</td>
      <td>0.31</td>
      <td>0.26</td>
      <td>Enchytraeids</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Tropical forest</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>Enchytraeids</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Tundra</td>
      <td>0.99</td>
      <td>0.83</td>
      <td>Enchytraeids</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Boreal forests</td>
      <td>0.28</td>
      <td>0.10</td>
      <td>Earthworms</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Desert</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>Earthworms</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Temperate coniferous forest</td>
      <td>1.20</td>
      <td>0.13</td>
      <td>Earthworms</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Temeprate deciduous forest</td>
      <td>2.00</td>
      <td>1.19</td>
      <td>Earthworms</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Temprate grassland</td>
      <td>3.80</td>
      <td>0.79</td>
      <td>Earthworms</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Tropical forest</td>
      <td>4.90</td>
      <td>0.48</td>
      <td>Earthworms</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Tundra</td>
      <td>1.40</td>
      <td>0.09</td>
      <td>Earthworms</td>
    </tr>
  </tbody>
</table>
</div>



For each biome, Fierer et al. provides an estimate of the average biomass density and the median biomass density. We generate two estimates for the total biomass of annelids, one based on average biomass densities and one based on median biomass densities. The estimate based on the average biomass density is more susceptible to sampling bias, as even a single measurement which is not characteristic of the global population (such as samples which are in non-natural conditions, or samples which have some technical biases associated with them) might shift the average biomass density significantly. On the other hand, the estimate based on median biomass densities might underestimate global biomass as it will reduce the effect of biologically relevant high biomass concentrations. As a compromise between these two caveats, we chose to use as our best estimate the geometric mean of the estimates from the two methodologies.

For each biome, we multiply the sum of the biomass density of Enchytraeids and Earthworms by the total area of that biome taken from the book [Biogeochemistry: An analysis of Global Change](https://www.sciencedirect.com/science/book/9780123858740) by Schlesinger & Bernhardt.:


```python
# Load biome area data
area = pd.read_excel('annelid_biomass_data.xlsx','Biome area', skiprows=1, index_col='Biome')

# For each biome sum the total biomass density of annelids
total_biomass_density = data.groupby('Biome').sum()

# Calculate the total biomass of annelids based on average or median biomass densities
total_biomass_mean = (total_biomass_density['Average biomass density [g C m^-2]']*area['Area [m^2]']).sum()
total_biomass_median = (total_biomass_density['Median biomass density [g C m^-2]']*area['Area [m^2]']).sum()

print('The total biomass of annelids based on Fierer et al. based on average biomass densities is %.1f Gt C' %(total_biomass_mean/1e15))
print('The total biomass of annelids based on Fierer et al. based on median biomass densities is %.2f Gt C' %(total_biomass_median/1e15))

```

    The total biomass of annelids based on Fierer et al. based on average biomass densities is 0.2 Gt C
    The total biomass of annelids based on Fierer et al. based on median biomass densities is 0.05 Gt C


The data in Fierer et al. does not account two biomes - croplands and tropical savannas. To estimate the biomass contribution of annelids from those biomes, we collected data from the literature on the biomass density of annelids (mostly earthworms) from these biomes. The data we collected is provided below:


```python
supp_biome_data = pd.read_excel('annelid_biomass_data.xlsx','Supplementary biomes')
supp_biome_data
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
      <th>Original value</th>
      <th>Original units</th>
      <th>Biomass density [g C m^-2]</th>
      <th>Site</th>
      <th>Biome</th>
      <th>Reference</th>
      <th>Link</th>
      <th>Remarks</th>
      <th>Unnamed: 8</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4516.846514</td>
      <td>g DW m-2</td>
      <td>2.258423</td>
      <td>Ivory Coast, Lamto, “mean savanna”</td>
      <td>Native tropical savanna</td>
      <td>Petersen, H., &amp; Luxton, M. (1982). A comparati...</td>
      <td>http://dx.doi.org/10.2307/3544689</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2977.568617</td>
      <td>g DW m-2</td>
      <td>1.488784</td>
      <td>Ivory Coast, Lamto, unburnt savanna/bare soil</td>
      <td>Native tropical savanna</td>
      <td>Block, W. (1970). Micro-arthropods in some Uga...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>48.793261</td>
      <td>g DW m-2</td>
      <td>0.024397</td>
      <td>Uganda, Kabanyolo, elephant grass</td>
      <td>Native tropical savanna</td>
      <td>Block, W. (1970). Micro-arthropods in some Uga...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>58.792141</td>
      <td>g DW m-2</td>
      <td>0.029396</td>
      <td>Uganda, Kabanyolo, natural bush</td>
      <td>Native tropical savanna</td>
      <td>Block, W. (1970). Micro-arthropods in some Uga...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>79.062971</td>
      <td>g DW m-2</td>
      <td>0.039531</td>
      <td>Uganda, Kabanyolo, pasture</td>
      <td>Native tropical savanna</td>
      <td>Block, W. (1970). Micro-arthropods in some Uga...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5</th>
      <td>20.000000</td>
      <td>g FW m-2</td>
      <td>3.000000</td>
      <td>1 Site in Mexico and 6 in Ivory Coast</td>
      <td>Native tropical savanna</td>
      <td>Fragoso, C., Kanyonyo, J., Moreno, A., Senapat...</td>
      <td>http://horizon.documentation.ird.fr/exl-doc/pl...</td>
      <td>total 32.06 and earthworms are 60%</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>6</th>
      <td>67.000000</td>
      <td>g FW m-2</td>
      <td>10.050000</td>
      <td>67 sites in america africa and asia</td>
      <td>Tropical pastures</td>
      <td>Fragoso, C., Kanyonyo, J., Moreno, A., Senapat...</td>
      <td>http://horizon.documentation.ird.fr/exl-doc/pl...</td>
      <td>73.2 g FW m-2 and ≈90% is earthworms</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.700000</td>
      <td>g FW m-2</td>
      <td>0.105000</td>
      <td>40 sites in america africa and asia</td>
      <td>Crops</td>
      <td>Fragoso, C., Kanyonyo, J., Moreno, A., Senapat...</td>
      <td>http://horizon.documentation.ird.fr/exl-doc/pl...</td>
      <td>NaN</td>
      <td>5.12 g FW and 13% of the biomass is earthworms</td>
    </tr>
    <tr>
      <th>8</th>
      <td>4.774000</td>
      <td>g FW m-2</td>
      <td>0.716100</td>
      <td>Carimagua, columbia</td>
      <td>Native tropical savanna</td>
      <td>Decaëns, T., Jiménez, J. J., Barros, E., Chauv...</td>
      <td>http://dx.doi.org/10.1016/j.agee.2003.12.005</td>
      <td>NaN</td>
      <td>15.3 g m-2 and 31% earthworms</td>
    </tr>
    <tr>
      <th>9</th>
      <td>59.600000</td>
      <td>g FW m-2</td>
      <td>8.940000</td>
      <td>Carimagua, columbia</td>
      <td>Tropical pastures</td>
      <td>Decaëns, T., Jiménez, J. J., Barros, E., Chauv...</td>
      <td>http://dx.doi.org/10.1016/j.agee.2003.12.005</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>10</th>
      <td>3.900000</td>
      <td>g FW m-2</td>
      <td>0.585000</td>
      <td>Manaus, Brazil</td>
      <td>Tropical pastures</td>
      <td>Decaëns, T., Jiménez, J. J., Barros, E., Chauv...</td>
      <td>http://dx.doi.org/10.1016/j.agee.2003.12.005</td>
      <td>NaN</td>
      <td>5.6 g FW m-2 and 65% earthworms</td>
    </tr>
    <tr>
      <th>11</th>
      <td>45.100000</td>
      <td>g FW m-2</td>
      <td>6.765000</td>
      <td>Manaus, Brazil</td>
      <td>Tropical pastures</td>
      <td>Decaëns, T., Jiménez, J. J., Barros, E., Chauv...</td>
      <td>http://dx.doi.org/10.1016/j.agee.2003.12.005</td>
      <td>NaN</td>
      <td>60.8 g FW m-2 and 79% earthworms</td>
    </tr>
    <tr>
      <th>12</th>
      <td>39.700000</td>
      <td>g FW m-2</td>
      <td>5.955000</td>
      <td>Manaus, Brazil</td>
      <td>Tropical pastures</td>
      <td>Decaëns, T., Jiménez, J. J., Barros, E., Chauv...</td>
      <td>http://dx.doi.org/10.1016/j.agee.2003.12.005</td>
      <td>NaN</td>
      <td>57 g FW m-2 and 90% earthworms</td>
    </tr>
    <tr>
      <th>13</th>
      <td>5.000000</td>
      <td>g FW m-2</td>
      <td>0.750000</td>
      <td>Carimagua, columbia</td>
      <td>Native tropical savanna</td>
      <td>Jiménez, J. J., Moreno, A. G., Decaëns, T., La...</td>
      <td>http://dx.doi.org/10.1007/s003740050469</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>14</th>
      <td>62.000000</td>
      <td>g FW m-2</td>
      <td>9.300000</td>
      <td>Carimagua, columbia</td>
      <td>Tropical pastures</td>
      <td>Jiménez, J. J., Moreno, A. G., Decaëns, T., La...</td>
      <td>http://dx.doi.org/10.1007/s003740050469</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



For each biome, we calculate the average and median annelid biomass density, and multiply by the total area of the biome:


```python
# Calculate average and median biomass densities for each additional biome
mean_supp_biome_biomass_density = supp_biome_data.groupby('Biome').mean()['Biomass density [g C m^-2]']
median_supp_biome_biomass_density = supp_biome_data.groupby('Biome').median()['Biomass density [g C m^-2]']

# Add the additional biomass to the estimate of the total biomass
total_biomass_mean += (mean_supp_biome_biomass_density*area['Area [m^2]']).sum()
total_biomass_median += (median_supp_biome_biomass_density*area['Area [m^2]']).sum()

print('Our estimate for the biomass of annelids based on average biomass densities is %.1f Gt C' %(total_biomass_mean/1e15))
print('Our estimate for the biomass of annelids based on median biomass densities is %.1f Gt C' %(total_biomass_median/1e15))
```

    Our estimate for the biomass of annelids based on average biomass densities is 0.3 Gt C
    Our estimate for the biomass of annelids based on median biomass densities is 0.2 Gt C


As noted above, for our best estimate we use the geometric mean of the estimates based on the average and median biomass densities at each biome:


```python
# Calculate the geometric mean of the average-based and median-based estimates
best_estimate = gmean([total_biomass_mean,total_biomass_median])

print('Our best estimate for the biomass of annelids is %.1f Gt C' %(best_estimate/1e15))
```

    Our best estimate for the biomass of annelids is 0.2 Gt C


This estimate does not take into account marine annelids, which we estimate do not contribute a major biomass component to the total biomass of annelids, as discussed in the annelids section in the Supplementary Information.


# Estimating the biomass of marine protists
Our estimate of the total biomass of marine protists relies on estimates of global biomass for many plankton groups. We included estimates of all plankton groups that are dominated by protists. The main groups with a significant biomass contribution were picoeukaryotes, microzooplankton (defined not to include copepod biomass), diatoms, *Phaeocystis* and Rhizaria. The estimates for all plankton groups except Rhizaria are based on [Buitenhuis et al.](http://search.proquest.com/openview/0e8e5672fa28111df473268e13f2f757/1?pq-origsite=gscholar&cbl=105729), which used data from the MAREDAT database. The protist group Rhizaria is under represented in the MAREDAT database, and thus our estimate for the total biomass of Rhizaria is based on *in situ* imaging work by [Biard et al.](http://dx.doi.org/10.1038/nature17652).

For the etimates based on MAREDAT data, Buitenhuis et al. estimates the total biomass of a specific plankton group by using a characteristic biomass concentration for each depth (either a median or average of the values in the database) and applying across the entire volume of ocean at that depth. Buitenhuis et al. generates two types of estimates are supplied for the global biomass of each plankton group: a “minimum” estimate which uses the median concentration of biomass from the database, and a “maximum” estimate which uses the average biomass concentration. Because the distributions of values in the database are usually highly skewed by asymmetrically high values the median and mean are loosely associated by the authors of the MAREDAT study with a minimum and maximum estimate. The estimate based on the average value is more susceptible to biases in oversampling singular locations such as blooms of plankton species, or of coastal areas in which biomass concentrations are especially high, which might lead to an overestimate. On the other hand, the estimate based on the median biomass concentration might underestimate global biomass as it will reduce the effect of biologically relevant high biomass concentrations. Therefore, here and in all estimates based on MAREDAT data, we take the geometric mean of the “minimum” and “maximum” estimates (actually median and mean values of the distribution) as our best estimate, which will increase our robustness to the effects discussed above. 

We now discuss the estimates for each of the groups of protists.

## Picoeukaryotes
We estimate the total biomass of picoeukaryotes by first estimating the total biomass of picophytoplankton, and then calculating the fraction of eukaryotes out of the total biomass of picophytoplankton. Buitenhuis et al. reports a "minimum" estimate of 0.28 Gt C and a "maximum" estimate of 0.64 Gt C for the biomass of picophytoplankton. We calculate the geometric mean of those estimates:


```python
import pandas as pd
from scipy.stats import gmean
# Calculate the geometric mean of the "minimum" and "maximum" estimates from Buitenhuis et al.
# for picophytoplankton
picophyto_biomsss = gmean([0.28e15,0.64e15])
```

To estimate the fraction of eukaryotes out of the total biomass of picophytoplankton, we rely on [Buitenhuis et al.](https://ueaeprints.uea.ac.uk/40778/) which estimates that they represent 49-69% of the global biomass of picophytoplankton. We use the geometric mean of this range as our best estimate of the fraction eukaryotes out of the total biomass of picophytoplankton.


```python
euk_frac = gmean([0.49,0.69])
auto_picoeuk_biomass = picophyto_biomsss*euk_frac
```

Picoeukaryotes contain both protists and plant species (like chlorophytes). It seems that, from the available literature, the biomass distribution between them is not strongly favored towards one class ([Li et al.](http://dx.doi.org/10.1016/0198-0149(92)90085-8)). We thus estimate the protist fraction at about 50% of the biomass of picoeukaryotes:


```python
auto_pico_protists_fraction = 0.5
auto_pico_protists_biomass = auto_picoeuk_biomass*auto_pico_protists_fraction
```

Protists in the picoplankton to nanoplankton size range (0.8-5 µm in diameter) include not only autotrophic, but also heterotrophic organisms. As we could not find a reliable resource for estimating the biomass of heterotrophic pico-nanoplankton we use a recent global 18S ribosomal DNA sequencing effort that was part of the Tara Oceans campaign ([de Vargas et al.](http://dx.doi.org/10.1126/science.1261605)). 

We extracted data from Fig. 5A in de Vargas et al., which quantifies the ratio between autotropic and heterotrophic picoplankton and nanoplankton:


```python
pd.options.display.float_format = '{:,.1f}'.format
# Load data from de Vargas on the ratio between autotrophic and heterotrophic protists
pico_nano_data = pd.read_excel('marine_protists_data.xlsx',skiprows=1)
pico_nano_data.head()
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
      <th>Ocean</th>
      <th>Phototrophic protists</th>
      <th>Heterotrophic protist</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4</td>
      <td>NAO</td>
      <td>0.3</td>
      <td>0.4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7</td>
      <td>MS</td>
      <td>0.2</td>
      <td>0.4</td>
    </tr>
    <tr>
      <th>2</th>
      <td>9</td>
      <td>MS</td>
      <td>0.2</td>
      <td>0.4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>11</td>
      <td>MS</td>
      <td>0.1</td>
      <td>0.3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>16</td>
      <td>MS</td>
      <td>0.2</td>
      <td>0.4</td>
    </tr>
  </tbody>
</table>
</div>



We calculate the geometric mean of the fraction of phototrophic and heterotrophic protists out of the total amount of 18S rDNA sequences. We use the ratio between these geometric means as our best estimate for the ratio between photosynthetic and heterotrophic protists.


```python
hetero_photo_ratio = gmean(pico_nano_data['Heterotrophic protist'])/gmean(pico_nano_data['Phototrophic protists'])
print('Our best estimate of the ratio between heterotrophic and phototrophic protists in pico-nanoplankton is ≈%.f-fold' %hetero_photo_ratio)
```

    Our best estimate of the ratio between heterotrophic and phototrophic protists in pico-nanoplankton is ≈2-fold


We add the contribution of heterotrophic pico-nanoprotists to our estimate:


```python
pico_protists_biomass = (1+hetero_photo_ratio)*auto_pico_protists_biomass
```

Relying on 18S sequence abundance as a proxy for biomass is not a well established practice, and has various biases, but for lack of any other alternative we could find to perform the estimate, we chose to use it. Yet, we note that this plays a minor role in our analysis that in any case will not affect any of the major conclusions of our study.

## Microzooplankton
The estimate of microzooplankton in Buitenhuis et al. does not include copepod biomass by definition, and thus is suitable in order to estimate the total biomass of microzooplankton protists. Buitenhuis et al. reports a "minimum" estimate of 0.48 Gt C and a "maximum" estimate of 0.73 Gt C for the biomass of picophytoplankton. We calculate the geometric mean of those estimates:


```python
# Calculate the geometric mean of the "minimum" and "maximum" estimates from Buitenhuis et al.
# for microzooplankton
microzoo_biomsss = gmean([0.48e15,0.73e15])
```

## Diatoms
For diatoms, Buitenhuis et al. reports a "minimum" estimate of 0.1 Gt C and a "maximum" estimate of 0.94 Gt C for the biomass of picophytoplankton. We calculate the geometric mean of those estimates:


```python
# Calculate the geometric mean of the "minimum" and "maximum" estimates from Buitenhuis et al.
# for diatoms
diatom_biomsss = gmean([0.1e15,0.94e15])
```

## Phaeocystis
For Phaeocystis, reports a "minimum" estimate of 0.11 Gt C and a "maximum" estimate of 0.71 Gt C for the biomass of picophytoplankton. We calculate the geometric mean of those estimates:


```python
# Calculate the geometric mean of the "minimum" and "maximum" estimates from Buitenhuis et al.
# for Phaeocystis
phaeocystis_biomsss = gmean([0.11e15,0.71e15])
```

As stated in Buitenhuis et al., the data from the MAREDAT initiative doesn’t contain the biomass of nanophytoplankton (phytoplankton between 2 and 20 µm) and autotrophic dinoflagellates. Nevertheless, this omission might be compensated by overestimation of Phaeocystis biomass because of sampling bias, so overall the sum of all the different phytoplankton fits well with total chlorophyll measurements from the WOA 2005.

## Rhizaria
For rhizaria, our estimate relies on data from Biard et al. Biard et al. divided the data into three depth layers (0-100 m, 100-200 m, and 200-500 m), and multiplied median biomass concentrations at each depth layer across the entire volume of water at that layer to generate global estimate. The biomass of Rhizaria in the top 500 meters of the ocean is estimated at ≈0.2 Gt C. 


```python
rhizaria_biomass = 0.2e15
```

To estimate the total biomass of marine protists, we sum up all of our estimates of the biomass of the different groups of protists:


```python
best_estimate = rhizaria_biomass + phaeocystis_biomsss + diatom_biomsss + microzoo_biomsss + pico_protists_biomass

print('Our best estimate for the total biomass of marine protists is ≈%.1f Gt C' %(best_estimate/1e15))
```

    Our best estimate for the total biomass of marine protists is ≈1.8 Gt C


The estimates based on the MAREDAT database include measurements only for the top 200 meters of the water column. For rhizaria, our estimate includes the top 500 meters of the water column. For more details on possible contributions from deeper ocean laters, see the marine protists section in the Supplementary information.

# Uncertanity analysis
We discuss the uncertainty of estimates based on the MAREDAT database in a dedicated section in the Supplementary Information. We crudly project an uncertainty of about an order of magnitude.

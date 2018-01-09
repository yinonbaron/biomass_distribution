
# Estimating the biomass of livestock
To estimate the biomass of livestock, we rely on data on global stocks of cattle, sheep goats, and pigs fro the Food and Agriculture Organization database FAOStat. We downloaded data from the domain Production/Live animals.
We combined data on the total stocks of each animal with estimates of the mean mass of each type of animal species from [Dong et al.](http://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_10_Ch10_Livestock.pdf), Annex 10A.2, Tables 10A-4 to 10A-9.

Here are samples of the data:


```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.display.float_format = '{:,.1e}'.format
# Load global stocks data
stocks = pd.read_csv('FAOSTAT_stock_data_mammals.csv')
stocks.head()
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
      <th>Domain Code</th>
      <th>Domain</th>
      <th>Area Code</th>
      <th>Area</th>
      <th>Element Code</th>
      <th>Element</th>
      <th>Item Code</th>
      <th>Item</th>
      <th>Year Code</th>
      <th>Year</th>
      <th>Unit</th>
      <th>Value</th>
      <th>Flag</th>
      <th>Flag Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>QA</td>
      <td>Live Animals</td>
      <td>5100</td>
      <td>Africa</td>
      <td>5111</td>
      <td>Stocks</td>
      <td>1107</td>
      <td>Asses</td>
      <td>2014</td>
      <td>2014</td>
      <td>Head</td>
      <td>18946358</td>
      <td>A</td>
      <td>Aggregate, may include official, semi-official...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>QA</td>
      <td>Live Animals</td>
      <td>5100</td>
      <td>Africa</td>
      <td>5111</td>
      <td>Stocks</td>
      <td>946</td>
      <td>Buffaloes</td>
      <td>2014</td>
      <td>2014</td>
      <td>Head</td>
      <td>3949287</td>
      <td>A</td>
      <td>Aggregate, may include official, semi-official...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>QA</td>
      <td>Live Animals</td>
      <td>5100</td>
      <td>Africa</td>
      <td>5111</td>
      <td>Stocks</td>
      <td>1126</td>
      <td>Camels</td>
      <td>2014</td>
      <td>2014</td>
      <td>Head</td>
      <td>23533724</td>
      <td>A</td>
      <td>Aggregate, may include official, semi-official...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>QA</td>
      <td>Live Animals</td>
      <td>5100</td>
      <td>Africa</td>
      <td>5111</td>
      <td>Stocks</td>
      <td>866</td>
      <td>Cattle</td>
      <td>2014</td>
      <td>2014</td>
      <td>Head</td>
      <td>312327289</td>
      <td>A</td>
      <td>Aggregate, may include official, semi-official...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>QA</td>
      <td>Live Animals</td>
      <td>5100</td>
      <td>Africa</td>
      <td>5111</td>
      <td>Stocks</td>
      <td>1016</td>
      <td>Goats</td>
      <td>2014</td>
      <td>2014</td>
      <td>Head</td>
      <td>374380445</td>
      <td>A</td>
      <td>Aggregate, may include official, semi-official...</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Load species body mass data
body_mass = pd.read_excel('livestock_body_mass.xlsx',skiprows=1,index_col=0) 
body_mass.head()
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
      <th>Cattle - dairy</th>
      <th>Cattle - non-dairy</th>
      <th>Buffaloes</th>
      <th>Swine - market</th>
      <th>Swine - breeding</th>
      <th>Sheep</th>
      <th>Goats</th>
      <th>Horses</th>
      <th>Asses</th>
      <th>Mules</th>
      <th>Camels</th>
      <th>Camelids, other</th>
    </tr>
    <tr>
      <th>IPCC Area</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Indian Subcontinent</th>
      <td>275</td>
      <td>110</td>
      <td>295</td>
      <td>28</td>
      <td>28</td>
      <td>2.8e+01</td>
      <td>3.0e+01</td>
      <td>238</td>
      <td>130</td>
      <td>130</td>
      <td>217</td>
      <td>217</td>
    </tr>
    <tr>
      <th>Eastern Europe</th>
      <td>550</td>
      <td>391</td>
      <td>380</td>
      <td>50</td>
      <td>180</td>
      <td>4.8e+01</td>
      <td>3.8e+01</td>
      <td>377</td>
      <td>130</td>
      <td>130</td>
      <td>217</td>
      <td>217</td>
    </tr>
    <tr>
      <th>Africa</th>
      <td>275</td>
      <td>173</td>
      <td>380</td>
      <td>28</td>
      <td>28</td>
      <td>2.8e+01</td>
      <td>3.0e+01</td>
      <td>238</td>
      <td>130</td>
      <td>130</td>
      <td>217</td>
      <td>217</td>
    </tr>
    <tr>
      <th>Oceania</th>
      <td>500</td>
      <td>330</td>
      <td>380</td>
      <td>45</td>
      <td>180</td>
      <td>4.8e+01</td>
      <td>3.8e+01</td>
      <td>377</td>
      <td>130</td>
      <td>130</td>
      <td>217</td>
      <td>217</td>
    </tr>
    <tr>
      <th>Western Europe</th>
      <td>600</td>
      <td>420</td>
      <td>380</td>
      <td>50</td>
      <td>198</td>
      <td>4.8e+01</td>
      <td>3.8e+01</td>
      <td>377</td>
      <td>130</td>
      <td>130</td>
      <td>217</td>
      <td>217</td>
    </tr>
  </tbody>
</table>
</div>



We pivot the stocks DataFrame to have a view of each kind of animal at each region:


```python
# Replace NaN with zeros
stocks.fillna(value=0,inplace=True)
stock_pivot = pd.pivot(stocks.Area,stocks.Item, stocks.Value).astype(float)

# Replace NaN with zeros
stock_pivot.fillna(value=0,inplace=True)

stock_pivot
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
      <th>Item</th>
      <th>Asses</th>
      <th>Buffaloes</th>
      <th>Camelids, other</th>
      <th>Camels</th>
      <th>Cattle</th>
      <th>Goats</th>
      <th>Horses</th>
      <th>Mules</th>
      <th>Pigs</th>
      <th>Sheep</th>
    </tr>
    <tr>
      <th>Area</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Africa</th>
      <td>1.9e+07</td>
      <td>3.9e+06</td>
      <td>0.0e+00</td>
      <td>2.4e+07</td>
      <td>3.1e+08</td>
      <td>3.7e+08</td>
      <td>6.1e+06</td>
      <td>1.0e+06</td>
      <td>3.4e+07</td>
      <td>3.4e+08</td>
    </tr>
    <tr>
      <th>Americas</th>
      <td>6.8e+06</td>
      <td>1.3e+06</td>
      <td>8.9e+06</td>
      <td>0.0e+00</td>
      <td>5.1e+08</td>
      <td>3.6e+07</td>
      <td>3.3e+07</td>
      <td>5.9e+06</td>
      <td>1.7e+08</td>
      <td>8.6e+07</td>
    </tr>
    <tr>
      <th>Asia</th>
      <td>1.6e+07</td>
      <td>1.9e+08</td>
      <td>0.0e+00</td>
      <td>4.2e+06</td>
      <td>4.9e+08</td>
      <td>5.8e+08</td>
      <td>1.4e+07</td>
      <td>3.0e+06</td>
      <td>5.9e+08</td>
      <td>5.4e+08</td>
    </tr>
    <tr>
      <th>Eastern Europe</th>
      <td>1.0e+05</td>
      <td>1.7e+04</td>
      <td>0.0e+00</td>
      <td>7.4e+03</td>
      <td>4.0e+07</td>
      <td>4.6e+06</td>
      <td>2.8e+06</td>
      <td>3.5e+03</td>
      <td>5.3e+07</td>
      <td>3.6e+07</td>
    </tr>
    <tr>
      <th>Northern America</th>
      <td>5.2e+04</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>1.0e+08</td>
      <td>2.6e+06</td>
      <td>1.1e+07</td>
      <td>4.0e+03</td>
      <td>8.1e+07</td>
      <td>6.1e+06</td>
    </tr>
    <tr>
      <th>Oceania</th>
      <td>9.0e+03</td>
      <td>2.4e+02</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>4.0e+07</td>
      <td>4.0e+06</td>
      <td>4.0e+05</td>
      <td>0.0e+00</td>
      <td>5.3e+06</td>
      <td>1.0e+08</td>
    </tr>
    <tr>
      <th>Southern Asia</th>
      <td>8.3e+06</td>
      <td>1.5e+08</td>
      <td>0.0e+00</td>
      <td>1.7e+06</td>
      <td>2.7e+08</td>
      <td>2.9e+08</td>
      <td>1.3e+06</td>
      <td>5.8e+05</td>
      <td>1.1e+07</td>
      <td>1.5e+08</td>
    </tr>
    <tr>
      <th>Western Europe</th>
      <td>3.4e+04</td>
      <td>6.5e+03</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>4.2e+07</td>
      <td>2.1e+06</td>
      <td>1.1e+06</td>
      <td>3.1e+04</td>
      <td>6.5e+07</td>
      <td>1.1e+07</td>
    </tr>
  </tbody>
</table>
</div>



There is a difference between the body mass of a dairy producing cow to a non-dairy producing cow. We thus count seperately the dairy producing cattle from the non-dairy producing cattle. Data about the amount of dairy cattle comes from the FAOStat domain Production - Livestock Primary.
There is also a difference in body mass between breeding and non-breeding pigs. We assume 90% of the population is breeding based on IPCC, 2006, Vol.4, Ch.10,Table.10.19.


```python
# Load data on the number of dairy producing cattle
dairy = pd.read_csv('FAOSTAT_cattle_dairy_data.csv')

# Set the index of the DataFrame to be the region so we can compare with the stocks data
dairy.set_index('Area',inplace=True)

# Add a category of dairy producing cattle
stock_pivot['Cattle - dairy'] = dairy.Value

# Set the amount of non-dairy producing cattle to be the total number minus the dairy producing cattle
stock_pivot['Cattle'] = stock_pivot['Cattle']-stock_pivot['Cattle - dairy']

# Rename the Cattle column name to Cattle - non-dairy
stock_pivot.rename(columns={'Cattle': 'Cattle - non-dairy'}, inplace=True)

# Set the amount of non-breeding (market) pigs (swine) to 10% of the total amount of pigs
stock_pivot['Swine - market'] = 0.1*stock_pivot['Pigs']

# Set the amount of breeding pigs (swine) to 90% of the total amount of pigs
stock_pivot['Pigs'] *= 0.9

# Rename the Pigs column name to Swine - breeding
stock_pivot.rename(columns={'Pigs': 'Swine - breeding'}, inplace=True)

stock_pivot
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
      <th>Item</th>
      <th>Asses</th>
      <th>Buffaloes</th>
      <th>Camelids, other</th>
      <th>Camels</th>
      <th>Cattle - non-dairy</th>
      <th>Goats</th>
      <th>Horses</th>
      <th>Mules</th>
      <th>Swine - breeding</th>
      <th>Sheep</th>
      <th>Cattle - dairy</th>
      <th>Swine - market</th>
    </tr>
    <tr>
      <th>Area</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Africa</th>
      <td>1.9e+07</td>
      <td>3.9e+06</td>
      <td>0.0e+00</td>
      <td>2.4e+07</td>
      <td>2.4e+08</td>
      <td>3.7e+08</td>
      <td>6.1e+06</td>
      <td>1.0e+06</td>
      <td>3.1e+07</td>
      <td>3.4e+08</td>
      <td>67436568</td>
      <td>3.4e+06</td>
    </tr>
    <tr>
      <th>Americas</th>
      <td>6.8e+06</td>
      <td>1.3e+06</td>
      <td>8.9e+06</td>
      <td>0.0e+00</td>
      <td>4.5e+08</td>
      <td>3.6e+07</td>
      <td>3.3e+07</td>
      <td>5.9e+06</td>
      <td>1.5e+08</td>
      <td>8.6e+07</td>
      <td>54930519</td>
      <td>1.7e+07</td>
    </tr>
    <tr>
      <th>Asia</th>
      <td>1.6e+07</td>
      <td>1.9e+08</td>
      <td>0.0e+00</td>
      <td>4.2e+06</td>
      <td>3.8e+08</td>
      <td>5.8e+08</td>
      <td>1.4e+07</td>
      <td>3.0e+06</td>
      <td>5.3e+08</td>
      <td>5.4e+08</td>
      <td>107571193</td>
      <td>5.9e+07</td>
    </tr>
    <tr>
      <th>Eastern Europe</th>
      <td>1.0e+05</td>
      <td>1.7e+04</td>
      <td>0.0e+00</td>
      <td>7.4e+03</td>
      <td>2.3e+07</td>
      <td>4.6e+06</td>
      <td>2.8e+06</td>
      <td>3.5e+03</td>
      <td>4.8e+07</td>
      <td>3.6e+07</td>
      <td>16188776</td>
      <td>5.3e+06</td>
    </tr>
    <tr>
      <th>Northern America</th>
      <td>5.2e+04</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>9.1e+07</td>
      <td>2.6e+06</td>
      <td>1.1e+07</td>
      <td>4.0e+03</td>
      <td>7.3e+07</td>
      <td>6.1e+06</td>
      <td>10161310</td>
      <td>8.1e+06</td>
    </tr>
    <tr>
      <th>Oceania</th>
      <td>9.0e+03</td>
      <td>2.4e+02</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>3.3e+07</td>
      <td>4.0e+06</td>
      <td>4.0e+05</td>
      <td>0.0e+00</td>
      <td>4.8e+06</td>
      <td>1.0e+08</td>
      <td>6874751</td>
      <td>5.3e+05</td>
    </tr>
    <tr>
      <th>Southern Asia</th>
      <td>8.3e+06</td>
      <td>1.5e+08</td>
      <td>0.0e+00</td>
      <td>1.7e+06</td>
      <td>2.0e+08</td>
      <td>2.9e+08</td>
      <td>1.3e+06</td>
      <td>5.8e+05</td>
      <td>1.0e+07</td>
      <td>1.5e+08</td>
      <td>69325063</td>
      <td>1.1e+06</td>
    </tr>
    <tr>
      <th>Western Europe</th>
      <td>3.4e+04</td>
      <td>6.5e+03</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>3.1e+07</td>
      <td>2.1e+06</td>
      <td>1.1e+06</td>
      <td>3.1e+04</td>
      <td>5.8e+07</td>
      <td>1.1e+07</td>
      <td>11289409</td>
      <td>6.5e+06</td>
    </tr>
  </tbody>
</table>
</div>



Data on the mass of animals is divided into different regions than the FAOStat data so we need preprocess the stocks DataFrame and merge it with the body mass data:


```python
# Preprocessing the stocks DataFrame

# Calculate the total number of animals in Latin America by subtracting values for Northern America from the total
# values for the Americas
stock_pivot.loc['Americas'] -= stock_pivot.loc['Northern America']

# Change name of Americas to Latin America
stock_pivot.rename(index={'Americas': 'Latin America'},inplace=True)

# Calculate the total number of animals in Asia without the Indian Subcontinent by subtracting values for the Southern Asia 
# from the total values for the Asia
stock_pivot.loc['Asia'] -= stock_pivot.loc['Southern Asia']

# Change name of Southern Asia to Indian Subcontinent
stock_pivot.rename(index={'Southern Asia': 'Indian Subcontinent'},inplace=True)


stock_pivot

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
      <th>Item</th>
      <th>Asses</th>
      <th>Buffaloes</th>
      <th>Camelids, other</th>
      <th>Camels</th>
      <th>Cattle - non-dairy</th>
      <th>Goats</th>
      <th>Horses</th>
      <th>Mules</th>
      <th>Swine - breeding</th>
      <th>Sheep</th>
      <th>Cattle - dairy</th>
      <th>Swine - market</th>
    </tr>
    <tr>
      <th>Area</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Africa</th>
      <td>1.9e+07</td>
      <td>3.9e+06</td>
      <td>0.0e+00</td>
      <td>2.4e+07</td>
      <td>2.4e+08</td>
      <td>3.7e+08</td>
      <td>6.1e+06</td>
      <td>1.0e+06</td>
      <td>3.1e+07</td>
      <td>3.4e+08</td>
      <td>6.7e+07</td>
      <td>3.4e+06</td>
    </tr>
    <tr>
      <th>Latin America</th>
      <td>6.7e+06</td>
      <td>1.3e+06</td>
      <td>8.9e+06</td>
      <td>0.0e+00</td>
      <td>3.6e+08</td>
      <td>3.3e+07</td>
      <td>2.2e+07</td>
      <td>5.9e+06</td>
      <td>8.0e+07</td>
      <td>8.0e+07</td>
      <td>4.5e+07</td>
      <td>8.9e+06</td>
    </tr>
    <tr>
      <th>Asia</th>
      <td>8.2e+06</td>
      <td>3.7e+07</td>
      <td>0.0e+00</td>
      <td>2.5e+06</td>
      <td>1.8e+08</td>
      <td>2.9e+08</td>
      <td>1.3e+07</td>
      <td>2.4e+06</td>
      <td>5.2e+08</td>
      <td>3.8e+08</td>
      <td>3.8e+07</td>
      <td>5.8e+07</td>
    </tr>
    <tr>
      <th>Eastern Europe</th>
      <td>1.0e+05</td>
      <td>1.7e+04</td>
      <td>0.0e+00</td>
      <td>7.4e+03</td>
      <td>2.3e+07</td>
      <td>4.6e+06</td>
      <td>2.8e+06</td>
      <td>3.5e+03</td>
      <td>4.8e+07</td>
      <td>3.6e+07</td>
      <td>1.6e+07</td>
      <td>5.3e+06</td>
    </tr>
    <tr>
      <th>Northern America</th>
      <td>5.2e+04</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>9.1e+07</td>
      <td>2.6e+06</td>
      <td>1.1e+07</td>
      <td>4.0e+03</td>
      <td>7.3e+07</td>
      <td>6.1e+06</td>
      <td>1.0e+07</td>
      <td>8.1e+06</td>
    </tr>
    <tr>
      <th>Oceania</th>
      <td>9.0e+03</td>
      <td>2.4e+02</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>3.3e+07</td>
      <td>4.0e+06</td>
      <td>4.0e+05</td>
      <td>0.0e+00</td>
      <td>4.8e+06</td>
      <td>1.0e+08</td>
      <td>6.9e+06</td>
      <td>5.3e+05</td>
    </tr>
    <tr>
      <th>Indian Subcontinent</th>
      <td>8.3e+06</td>
      <td>1.5e+08</td>
      <td>0.0e+00</td>
      <td>1.7e+06</td>
      <td>2.0e+08</td>
      <td>2.9e+08</td>
      <td>1.3e+06</td>
      <td>5.8e+05</td>
      <td>1.0e+07</td>
      <td>1.5e+08</td>
      <td>6.9e+07</td>
      <td>1.1e+06</td>
    </tr>
    <tr>
      <th>Western Europe</th>
      <td>3.4e+04</td>
      <td>6.5e+03</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>3.1e+07</td>
      <td>2.1e+06</td>
      <td>1.1e+06</td>
      <td>3.1e+04</td>
      <td>5.8e+07</td>
      <td>1.1e+07</td>
      <td>1.1e+07</td>
      <td>6.5e+06</td>
    </tr>
  </tbody>
</table>
</div>



We now multiply the stocks of each animal type and for each region by the characteristic body weight of each animal:


```python
wet_biomass =(body_mass*stock_pivot)
wet_biomass
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
      <th>Asses</th>
      <th>Buffaloes</th>
      <th>Camelids, other</th>
      <th>Camels</th>
      <th>Cattle - dairy</th>
      <th>Cattle - non-dairy</th>
      <th>Goats</th>
      <th>Horses</th>
      <th>Mules</th>
      <th>Sheep</th>
      <th>Swine - breeding</th>
      <th>Swine - market</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Africa</th>
      <td>2.5e+09</td>
      <td>1.5e+09</td>
      <td>0.0e+00</td>
      <td>5.1e+09</td>
      <td>1.9e+10</td>
      <td>4.2e+10</td>
      <td>1.1e+10</td>
      <td>1.4e+09</td>
      <td>1.3e+08</td>
      <td>9.5e+09</td>
      <td>8.7e+08</td>
      <td>9.6e+07</td>
    </tr>
    <tr>
      <th>Asia</th>
      <td>1.1e+09</td>
      <td>1.4e+10</td>
      <td>0.0e+00</td>
      <td>5.5e+08</td>
      <td>1.3e+10</td>
      <td>7.2e+10</td>
      <td>1.1e+10</td>
      <td>4.9e+09</td>
      <td>3.1e+08</td>
      <td>1.9e+10</td>
      <td>9.4e+10</td>
      <td>2.9e+09</td>
    </tr>
    <tr>
      <th>Eastern Europe</th>
      <td>1.3e+07</td>
      <td>6.3e+06</td>
      <td>0.0e+00</td>
      <td>1.6e+06</td>
      <td>8.9e+09</td>
      <td>9.2e+09</td>
      <td>1.8e+08</td>
      <td>1.0e+09</td>
      <td>4.6e+05</td>
      <td>1.8e+09</td>
      <td>8.6e+09</td>
      <td>2.6e+08</td>
    </tr>
    <tr>
      <th>Indian Subcontinent</th>
      <td>1.1e+09</td>
      <td>4.5e+10</td>
      <td>0.0e+00</td>
      <td>3.7e+08</td>
      <td>1.9e+10</td>
      <td>2.2e+10</td>
      <td>8.8e+09</td>
      <td>3.2e+08</td>
      <td>7.6e+07</td>
      <td>4.3e+09</td>
      <td>2.9e+08</td>
      <td>3.2e+07</td>
    </tr>
    <tr>
      <th>Latin America</th>
      <td>8.8e+08</td>
      <td>5.0e+08</td>
      <td>1.9e+09</td>
      <td>0.0e+00</td>
      <td>1.8e+10</td>
      <td>1.1e+11</td>
      <td>9.9e+08</td>
      <td>5.2e+09</td>
      <td>7.7e+08</td>
      <td>2.2e+09</td>
      <td>2.2e+09</td>
      <td>2.5e+08</td>
    </tr>
    <tr>
      <th>Middle east</th>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
    </tr>
    <tr>
      <th>Northern America</th>
      <td>6.8e+06</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>6.1e+09</td>
      <td>3.5e+10</td>
      <td>1.0e+08</td>
      <td>4.0e+09</td>
      <td>5.2e+05</td>
      <td>3.0e+08</td>
      <td>1.4e+10</td>
      <td>3.7e+08</td>
    </tr>
    <tr>
      <th>Oceania</th>
      <td>1.2e+06</td>
      <td>9.3e+04</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>3.4e+09</td>
      <td>1.1e+10</td>
      <td>1.5e+08</td>
      <td>1.5e+08</td>
      <td>0.0e+00</td>
      <td>5.0e+09</td>
      <td>8.7e+08</td>
      <td>2.4e+07</td>
    </tr>
    <tr>
      <th>Western Europe</th>
      <td>4.4e+06</td>
      <td>2.5e+06</td>
      <td>0.0e+00</td>
      <td>0.0e+00</td>
      <td>6.8e+09</td>
      <td>1.3e+10</td>
      <td>7.9e+07</td>
      <td>4.1e+08</td>
      <td>4.1e+06</td>
      <td>5.2e+08</td>
      <td>1.2e+10</td>
      <td>3.2e+08</td>
    </tr>
  </tbody>
</table>
</div>



We sum over all regions and convert units from kg wet weight to Gt C carbon by assuming carbon is ≈15% of the wet weight (30% dry weight of wet weight and carbon is 50% of dry weight).


```python
# conversion factor from kg wet weight to Gt C
kg_to_gt_c = 1000*0.15/1e15
total_biomass = wet_biomass.sum()*kg_to_gt_c
best_estimate = total_biomass.sum()
print('Our best estimate for the biomass of mammal livestock is %.1f Gt C' % best_estimate)
```

    Our best estimate for the biomass of mammal livestock is 0.1 Gt C


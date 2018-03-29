# The Biomass Distribution on Earth
This repository contains all source data and code for the analysis found in "The Distribution of Biomass on Earth" by Yinon Bar-On, Rob Phillips and Ron Milo.

An index for the structure of this repository is given below:

* **[`plants/`](./plants)|** Data and code for estimating the total biomass of plants

* **[`bacteria_archaea/`](./bacteria_archaea)|** Data and code for estimating the total biomass of bacteria & arechaea

* **[`fungi/`](./fungi)|** Data and code for estimating the total biomass of fungi

* **[`protists/`](./protists)|** Data and code for estimating the total biomass of fungi

* **[`animals/`](./animals)|** Data and code for estimating the total biomass of animals

* **[`viruses/`](./viruses)|** Data and code for estimating the total biomass of viruses

* **[`MAREDAT_consistency_check/`](./MAREDAT_consistency_check)|** Consistency checks for estimates based on the MARine Ecosystem DATa (MEREDAT)

* **[`figures/`](./figures)|** Code for generating the figures in the manuscript and scripts for calculating the probability of plants dominating biomass and for calculating the probability the marine trophic pyramid is inverted

* **[`statistics_helper/`](./statistics_helper)|** Helper functions for generating our best estimates as well as uncertainty projections

* `results.xlsx`| A file summarizing the results of the study

* `run_pipeline.py`| A script for running the entire analysis and regenerating the results

Each directory contain Jupyter notebooks detailing the analysis leading to our estimates. To make our analysis accessible, we provide the notebooks in three file formats: `.ipynb` files, `.html` files and `.py` files.

In order to run the code in this repository, first intall the dependencies of the code. To install the dependencies run the following script:

```sudo pip install -r requirements.txt```

The code was tested on the following software versions:
* python 3.5.2
* ipython 5.5.0
* jupyter 1.0.0
* scipy 0.19.0
* pandas 0.21.0
* numpy 1.14.2
* gdal 1.11.3
* matplotlib 2.2.2
* openpyxl 2.5.0

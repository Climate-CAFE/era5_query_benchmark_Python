# Benchmarking Performance of Dowmloading Hourly ERA5-Land Data
## Project Overview
Using the Python cdsapi package, ERA5-Land hourly measures are downloaded from the Copernicus Climate Data Store (CDS). The API query can be very time-consuming especially when too many and too large API queries are made. This project benchmarks the performance of downloading hourly measures of ERA5-Land data using sequential processing and parallel processing. It did two experiments. The first experiment compares the performance of downloading the monthly data of the year 2000 sequentally month-by-month versus over months in parallel. In the second experiment, the monthly data across two years (2000 and 2001) are downloaded. It compares the performance of downloading the monthly data sequentially year-by-year versus over years in parallel, given that within each year monthly data are downlaoded over months in parallel. Kenya is used as a demonstration area for the Copernicus CDS API query, using administrative boundaries from the Database of Global Administrative Areas. The project shows that downloading data in parallel over both years and months within a year is much faster than downloading data sequentially especially when there are many variables to download, and the implementation of parallel processing in Python is relatively easy. 

## Usage
This repository provides the building blocks for the query of any data from the Copernicus CDS. The following comments describe how to manipulate the ERA5 API language to query additional variables, time frames, or spatial extents. 

1) Users will need to set up an account with the Copernicus CDS for the API query to function effectively. For more information on the cdsapi package and details about how to set up an account and access the necessary user ID and API key inputs for the API query please see: https://cds.climate.copernicus.eu/how-to-api#install-the-cds-api-client. Do these steps to create account, get API key, and agree to the Term of Use:
   - Create an ECMWF account by self-registering. Go to: https://www.ecmwf.int/. Click Log in.
   - Once you log in, go to Climate Data Store webpage: https://cds.climate.copernicus.eu/.
   - Click your log-in icon, then click "Your profile" to get user ID and key. 
   - Visit user profile to accept the terms and conditions in the profile page. 
   - One must agree to the Terms of Use of a dataset before downloading any data out of it. This step must be done manually from the dataset page (at the bottom of the download form). For example, Go to ERA-5 land data Download page https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=download. Go to "Terms of use" block to accept the data licence to use products.
   - Visit user profile page again to double check that Dataset licences to use Copernicus products shows up there and has been accepted.   
You don't need to set key for web API in the program. This is becuase the web API url and your key have been saved to the file C:\Users\YOURUSERNAME\.cdsapirc. When you make a request, the program can automatically find those information from that file. Note: your user ID and API key should never be shared externally.
2) Set a directory. Establishing this at the start of the script is useful in case future adjustments are made to the path. There are subdirectories within this directory for reading in Global Administrative boundaries and for outputting the ERA5 rasters queried in this script.
3) Read in Kenya boundaries geopackage. These data were downloaded from GADM https://gadm.org/download_country.html. The layer specification "ADM_ADM_0" indicates that the level 0 boundaries should be read in, representing the national boundary. We read in the boundaries here to establish the geographic extent that should be queried from ERA5, so ward-level boundaries are not needed. Note: need to first create a subfolder "Kenya_GADM" on your path, and put gadm41_KEN.gpkg file in that subfolder.
4) Assess bounding box. The bounding box represents the coordinates of the extent of the shapefile, and will be used to specify the area we would like to query from Copernicus Climate Data Store. The API will allow any bounding parameters; however, values that deviate from the original model grid scale will be interpolated onto a new grid. Therefore, it’s recommended that for ERA5-Land (which is 0.1˚ resolution) the bounding coordinates be divisible by 0.1 (e.g., 49.5˚N, -66.8˚E, etc.), and that coordinates for ERA5 be divisible by 0.25 (e.g., 49.25˚N, -66.75˚E, etc.). Add a small buffer around the bounding box to ensure the whole region is queried, and round the parameters to a 0.1 resolution. A 0.1 resolution is applied because the resolution of netCDF ERA5 data is .25x.25 https://confluence.ecmwf.int/display/CKB/ERA5%3A+What+is+the+spatial+reference. The ERA5 area query requires the area to be formatted specifically as a list of xmin, ymin, xmax, ymax. 

## Notes on Computation
- The query of data using cdsapi is done in monthly chunks due to restrictions in the CDS API. Two years of data (2000 and 2001) are downloaded for this experiment.
- Each 1-month period of ERA5-Land data across Kenya with 1 to 8 variables are downloaded to benchmark the performance.
- The computation efficiency and size will vary by use case. Aggregating to a smaller administrative boundary, or using a less spatially resolved raw product (such as ERA5, Non-Land with is a 25km grid) will reduce the needed computation resources.
- The use of a computing cluster allows for intensive computation to run more quickly and to run without the limits of conventional storage options on a single computer.

## Data Sources
- [ERA5-Land hourly data from 1950 to present](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land)
- [Database of Global Administrative Areas](https://gadm.org/)

## Workflow
Five scripts are included in the code repository. The plot from the last script is included in the plot repository.     

1) seqY_seqM_singleY.py applies the cdsapi package to query hourly ERA5-Land data from the Copernicus CDS sequentially month-by-month for year 2000. Each 1-month period of ERA5-Land data across Kenya with 1 to 8 variables are downloaded to benchmark the performance.
2) seqY_parM_singleY.py applies the cdsapi package to query hourly ERA5-Land data from the Copernicus CDS over months in parallel for year 2000. Each 1-month period of ERA5-Land data across Kenya with 1 to 8 variables are downloaded to benchmark the performance.   
3) seqY_parM_multY.py applies the cdsapi package to query hourly ERA5-Land data from the Copernicus CDS both sequentially year-by-year and over months in parallel within each year for years 2000 and 2001. Each 1-month period of ERA5-Land data across Kenya with 1 to 8 variables are downloaded to benchmark the performance.
4) parY_parM_multY.py applies the cdsapi package to query hourly ERA5-Land data from the Copernicus CDS both over years in parallel and over months in parallel within each year for years 2000 and 2001. Each 1-month period of ERA5-Land data across Kenya with 1 to 8 variables are downloaded to benchmark the performance.
5) plot.py plots performance comparing downloading time of monthly data within a given year sequentially versus in parallel and comparing downloading time of monthly data across two years sequentally versus in parallel.  

## Dependencies
Packages used in this repository include:

- import cdsapi for era5 data query
- import geopandas for spatial operations on geometric types
- import os for creating/removing a file path
- import pandas for manipulation of structured data 
- from timeit import timeit for measuring execution time of small code
- import matplotlib.pyplot as plt for plotting
- import time for pausing code execution
- from multiprocessing import Pool, current_process for parallel processing


  

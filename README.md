# Air Quality Analysis

## Introduction

This project focuses on the analysis of air quality data collected from 12 air quality monitoring stations. The primary objective is to explore air pollution trends, assess the impact of various environmental factors on pollutant levels, and visualize these trends to gain insights into the quality of air in different regions. 
## Dataset Overview

The dataset consists of air quality data collected over a period of time from 12 different monitoring stations. Each entry in the dataset contains various environmental variables. Below is an overview of the key variables present in the dataset:

- **Year**: The year when the data was collected.
- **Month**: The month when the data was collected.
- **Day**: The day of the month when the data was collected.
- **Hour**: The hour of the day when the data was recorded.
- **PM2.5**: Concentration of particulate matter smaller than 2.5 micrometers (µg/m³).
- **PM10**: Concentration of particulate matter smaller than 10 micrometers (µg/m³).
- **SO2**: Concentration of sulfur dioxide (µg/m³).
- **NO2**: Concentration of nitrogen dioxide (µg/m³).
- **CO**: Concentration of carbon monoxide (µg/m³).
- **O3**: Concentration of ozone (µg/m³).
- **TEMP**: Air temperature in degrees Celsius (°C).
- **PRESSURE**: Atmospheric pressure in hectopascals (hPa).
- **DEWP**: Dew point temperature in degrees Celsius (°C).
- **RAIN**: Amount of rainfall in millimeters (mm).
- **wd**: Wind direction (measured in degrees).
- **WSPM**: Wind speed in meters per second (m/s).
- **Station**: The name of the monitoring station that recorded the data.

## Analysis Task

### 1. Data Wrangling
- **Gathering Data**: Data collected from CSV files from various monitoring stations.
- **Assessing Data**: Checking for missing values, duplicates, and anomalies.
- **Cleaning Data**: Handling missing values, removing duplicates, and converting data types when necessary.

### 2. Exploratory Data Analysis (EDA)
- Analyzing the distribution of pollutants, relationships with environmental factors, and time-based trends (daily, monthly, yearly).

### 3. Visualization
- Creating line plots, heatmaps, and scatter plots to visualize trends and relationships between the data.

## Installation

### 1. Set Up a Virtual Environment - Shell/Terminal

```
pipenv install
pipenv shell
```

### 2. Install Required Libraries
```
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```

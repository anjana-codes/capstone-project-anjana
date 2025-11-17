# capstone-project-anjana

# Title: FEMA Hazard Mitigation Costs and State Trends Analysis
### Name: Anjana Dhakal, Date: 10/26/2025

## Overview
This capstone project analyzes the FEMA Hazard Mitigation Assistance (HMA) Mitigated Properties dataset (v4) to predict project costs and uncover state-level trends in disaster mitigation spending.

The project leverages data cleaning, exploratory data analysis, and predictive modeling to gain insights into mitigation spending patterns across the United States.

## Project Objectives

- Understand trends in hazard mitigation projects across states and structure types.
- Identify factors influencing the actual amount paid for mitigation projects.
- Conduct exploratory data analysis to guide feature engineering and predictive modeling.
- Generate visual insights for reporting and decision support.

## Dataset
- Source: (https://www.fema.gov/openfema-data-page/hazard-mitigation-assistance-mitigated-properties-v4)
- Description: Contains details of projects funded under FEMA mitigation programs, including property attributes, project types, costs, and     approval dates.
- Size: ~ 15MB ( 97,515 rows × 19 columns)
  

##  File structure 
 ```
 
capstone-project-anjana/
│
├── data/ # Raw and cleaned datasets
│ ├── hma_mitigated_properties_v4.csv
│ └── hma_mitigated_properties_cleaned.csv
├── images/ # Figures and visualizations from EDA aand modeling
├── notebooks/ # Jupyter notebooks for EDA and modeling
│ └── fema_mitigation_analysis.ipynb
├── reports/ # Generated reports and summaries
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md

```
## Environment set up

1. Created a new repo in github
2. Cloned git repo to local machine
3. Added gigtignore and requirements. md
4. Created virtual environment and activated it
   
```
   py -m venv .venv
.\.venv\Scripts\activate

```

5. Installed dependencies
 
``` 
.\.venv\Scripts\activate
py -m pip install --upgrade pip setuptools wheel
py -m pip install --upgrade -r requirements.txt

```
   
6. Git add-commit-push to Github

``` 
git add .
git commit -m "initial commit"
git push -u origin main

```

## Data Cleaning
1. Early filter to US states and post-2000.
2. Keep relevant columns (including model predictors).
3. Handle missing values early (for categoricals before standardization).
4. Type conversions and standardize categoricals (with str conversion for safety).
5. Derive date proxy and clip negatives.
6. Remove duplicates and derive total cost.
7. Validation and save cleaned data in csv format.

## Data Description

The dataset contains records of properties mitigated under FEMA’s Hazard Mitigation Assistance (HMA) program. Key fields:

| Field Name             | Description                                                    |
|------------------------|----------------------------------------------------------------|
| state                  | U.S. state where the property is located                      |
| county                 | County name where the property is located                     |
| damageCategory         | Severity of damage (e.g., Substantial, Minor)                 |
| structureType          | Type of property structure (e.g., Single Family)              |
| typeOfResidency        | Residency type (e.g., Owner-Occupied)                         |
| foundationType         | Property foundation type (e.g., Slab-On-Grade)                |
| actualAmountPaid       | Amount paid to property owner (USD; excludes admin costs)     |
| numberOfProperties     | Number of properties mitigated in the project                 |
| propertyAction         | Mitigation action type (e.g., Elevation, Acquisition)         |
| propertyPartOfProject  | Indicates if property is part of a larger project             |
| programFy              | Fiscal year of the mitigation program                          |
| date_approved_proxy    | Approval date proxy derived from fiscal year                   |
| totalMitigationCost    | Total mitigation cost (actualAmountPaid × numberOfProperties) |

## Exploratory Data Analysis (EDA)
- Dataset Overview: Descriptive statistics for actualAmountPaid, numberOfProperties, and totalMitigationCost to understand distributions and outliers.
- Target Variable: Histogram of actualAmountPaid (raw and log-transformed) to assess skewness and normalize distribution.
- Temporal Trends: Projects counted per fiscal year (programFy); line charts show yearly project counts, total funds paid, and average cost per property.
- Reactive Funding Pattern: Aggregated yearly actualAmountPaid and numberOfProperties; dual-axis chart compares total spending vs. properties mitigated.
- Mitigation Strategy: Top property actions (propertyAction) and structure types counted; visualized via pie and bar charts.
- Geographic Analysis: Aggregated by state; identified top 10 states by total funds; horizontal bar chart with national average reference line.

## Modeling Approach


## Key Insights
- The temporal analysis clearly shows funding surges after major disasters, indicating a reactive funding model.
- Funding is highly concentrated in a few states, with Missouri and Washington leading the expenditure, confirming localized hotspots.

## Important links
- GitHub link (https://github.com/anjana-codes/capstone-project-anjana)
- Overleaf link (https://www.overleaf.com/read/qvzgmxrvcscf#589394)
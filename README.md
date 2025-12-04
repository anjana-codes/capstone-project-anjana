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
├── images/ # Figures and visualizations from EDA and modeling
├── notebooks/ 
│ └── fema_mitigation_analysis.ipynb
├── reports
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

- Dataset Overview: Post-2000 U.S. dataset; target is log-transformed `actualAmountPaid` to reduce right-skewness.
- Features: Categorical (`state`, `structureType`, `typeOfResidency`, `foundationType`) and numerical (`numberOfProperties`, `programFy`).
- Preprocessing: One-hot encoding for categorical features; numerical features passed through unchanged; 80/20 train/test split (`random_state=42`).
- Models Evaluated: Linear Regression (baseline) and Random Forest Regressor (100 trees, `max_depth=15`, `min_samples_split=5`).
- Evaluation: Metrics include R² (log and original scales), MAE, RMSE; 5-fold cross-validation for generalizability; train/test metrics to detect overfitting.

Summary table for model evaluation 

| Dataset   | Model                   | R² (Log) | R² (Original) | MAE ($)   | RMSE ($)    |
|-----------|------------------------|----------|---------------|-----------|------------|
| Training  | Linear Regression       | 0.3955   | -0.0006       | 265,200   | 9,092,721  |
| Training  | Random Forest Regressor | 0.6570   | 0.0019        | 253,640   | 9,081,705  |
| Test      | Linear Regression       | 0.3857   | -0.0003       | 222,836   | 9,635,366  |
| Test      | Random Forest Regressor | 0.5847   | -0.0003       | 213,165   | 9,634,923  |

 - Projections: RFR used for FY2030 scenario (+5 years to `programFy`); national costs increase 17.9% ($1.63B → $1.92B) with 90% CI $1.46B–$2.39B.
 - Visualizations: Model comparison bar charts, feature importance plots, and top-5 state projections (current vs. future costs).

| State       | Current Cost ($M) | Projected FY2030 Cost ($M) |
|------------ |----------------- |----------------------------|
| Missouri    | 2,605            | 240                        |
| Washington  | 1,703            | 19                         |
| Florida     | 1,082            | 251                        |
| Alabama     | 1,025            | 107                        |
| Pennsylvania| 1,006            | 62                         |


## Key Insights
- Reactive Funding:Temporal analysis shows funding surges after major disasters, indicating a reactive funding model.  
- Geographic Concentration: Missouri and Washington lead expenditures, confirming localized hotspots.  
- Extreme Cost Concentration: Costs are right-skewed (median ~$50K; outliers >$10M); log-transformation normalizes ~80% of mid-range residential projects.  
- Strategic Priorities: Wind Retrofit (35%) and Acquisition/Demolition (38%) dominate actions; Single-Family structures (~65%) are the primary focus, highlighting gaps in public/commercial asset protection.  
- Reactive Temporal Trends: Spikes in 2005 (Katrina), 2010 (floods/tornadoes), 2017 (hurricanes); ~40% decline post-2020; average cost per property rose ~$40K (2000s) → ~$75K (2010s).  
- Geographic Hotspots: Top 10 states account for ~75% of spending (e.g., Missouri $2.6B); inland flood areas reveal hidden risks; low-funding states (e.g., North Dakota <$10M) face resilience gaps.  
- Predictive Modeling Insights: Random Forest Regressor captures nonlinear patterns (e.g., state × structureType); FY2030 projections show hotspot fade (e.g., Missouri -91%) and spending redistribution, signaling policy risks.  
- Policy Implications: Reactive funding creates inequities; recommendations include 20% preemptive allocation, diversified strategies for public assets, and integration of climate projections for hazard-specific models.


## Important links
- GitHub repo link (https://github.com/anjana-codes/capstone-project-anjana)
- Overleaf link (https://www.overleaf.com/read/qvzgmxrvcscf#589394)
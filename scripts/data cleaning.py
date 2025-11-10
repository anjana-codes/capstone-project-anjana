# ======================================================================
# FEMA HMA Mitigated Properties – Data Cleaning Script 
# ======================================================================


import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Load raw dataset (no filters)
file_path = r"C:\Repos\capstone-project-anjana\data\hma_mitigated_properties_v4.csv"
df_raw = pd.read_csv(file_path)
print("✅ Data Loaded Successfully")
df_raw.head(10)


# US states list (for filtering)
us_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
             'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
             'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
             'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
             'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
             'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
             'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

# Step 1: Filter raw data (US states and post-2000)
df_filtered = df_raw[(df_raw['state'].isin(us_states)) & (df_raw['programFy'] >= 2000)].copy()
print(f"Shape after filtering (US states, post-2000): {df_filtered.shape}")

# Step 1.5: Keep Only Relevant Columns (includes model predictors and propertyAction for EDA)
cols_to_keep = [
    'state', 'county', 'damageCategory', 'structureType', 'typeOfResidency', 'foundationType',
    'actualAmountPaid', 'numberOfProperties', 'propertyAction', 'propertyPartOfProject', 'programFy'
]
available_cols = [col for col in cols_to_keep if col in df_filtered.columns]
df_filtered = df_filtered[available_cols].copy()
print(f"Kept columns: {available_cols}")

# Step 1.6: Handle Missing Values Early (for categoricals before standardization)
df_us_post2000 = df_filtered.copy()
df_us_post2000 = df_us_post2000.dropna(subset=['actualAmountPaid', 'state'])

categorical_fill_cols = ['damageCategory', 'structureType', 'typeOfResidency', 'foundationType', 'propertyAction', 'propertyPartOfProject', 'county']
for col in categorical_fill_cols:
    if col in df_us_post2000.columns:
        df_us_post2000[col] = df_us_post2000[col].fillna('Unknown')

if 'numberOfProperties' in df_us_post2000.columns:
    df_us_post2000['numberOfProperties'] = df_us_post2000['numberOfProperties'].fillna(1)

df_us_post2000['actualAmountPaid'] = df_us_post2000['actualAmountPaid'].fillna(0)  # Unpaid = 0

# Step 2: Type conversions (coerce non-numeric to NaN)
df_us_post2000['actualAmountPaid'] = pd.to_numeric(df_us_post2000['actualAmountPaid'], errors='coerce')
df_us_post2000['numberOfProperties'] = pd.to_numeric(df_us_post2000['numberOfProperties'], errors='coerce')
df_us_post2000['programFy'] = pd.to_numeric(df_us_post2000['programFy'], errors='coerce')

# Step 2.5: Standardize Categorical Values (now safe after filling)
categorical_std_cols = ['state', 'county', 'damageCategory', 'structureType', 'typeOfResidency', 'foundationType', 'propertyAction', 'propertyPartOfProject']
for col in categorical_std_cols:
    if col in df_us_post2000.columns:
        df_us_post2000[col] = df_us_post2000[col].astype(str).str.strip().str.title()

if 'damageCategory' in df_us_post2000.columns:
    df_us_post2000['damageCategory'] = df_us_post2000['damageCategory'].replace({
        'N/A': 'Unknown',
        'Major': 'Substantial',
        'Earth Quake': 'Earthquake'
    })

if 'propertyPartOfProject' in df_us_post2000.columns:
    df_us_post2000['propertyPartOfProject'] = df_us_post2000['propertyPartOfProject'].astype(str).str.title()

# Step 2.6: Convert Dates/Temporal Fields
df_us_post2000['date_approved_proxy'] = pd.to_datetime('09-30-' + df_us_post2000['programFy'].astype(str))

# Step 3.2: Clip Negative actualAmountPaid to 0
negatives_clipped = (df_us_post2000['actualAmountPaid'] < 0).sum()
df_us_post2000['actualAmountPaid'] = df_us_post2000['actualAmountPaid'].clip(lower=0)
if negatives_clipped > 0:
    print(f"⚠️ Clipped {negatives_clipped} negative actualAmountPaid values to 0.")

# Step 3.5: Remove duplicates (based on all columns for exact matches)
initial_len = len(df_us_post2000)
df_us_post2000 = df_us_post2000.drop_duplicates()
duplicates_removed = initial_len - len(df_us_post2000)
print(f"Duplicates removed: {duplicates_removed} rows (from {initial_len} to {len(df_us_post2000)})")

# Step 3.6: Derive Total Cost
df_us_post2000['totalMitigationCost'] = df_us_post2000['actualAmountPaid'] * df_us_post2000['numberOfProperties']

# Save cleaned data
data_folder = r"C:\Repos\capstone-project-anjana\data"
df_us_post2000.to_csv(f"{data_folder}/hma_mitigated_properties_cleaned.csv", index=False)
print("\nCleaned data saved to 'hma_mitigated_properties_cleaned_post2000.csv'")

print("✅ Cleaning complete! Files saved in data folder:")
print(f"   - hma_mitigated_properties_cleaned.csv ({df_us_post2000.shape[0]} rows)")

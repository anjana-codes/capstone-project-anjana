# ======================================================================
# FEMA HMA Mitigated Properties – Data Cleaning Script 
# ======================================================================


import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# 1️⃣ Load Dataset from Data Folder
file_path = r"C:\Repos\capstone-project-anjana\data\hma_mitigated_properties_v4.csv"
df = pd.read_csv(file_path)

# ======================================================================
# 2️⃣ Keep Only Relevant Columns
cols_to_keep = [
    'state', 'county', 'damageCategory', 'structureType',
    'actualAmountPaid', 'numberOfProperties', 'propertyPartOfProject', 'programFy'
]
available_cols = [col for col in cols_to_keep if col in df.columns]
df = df[available_cols]

# ======================================================================
# 3️⃣ Handle Missing Values
df = df.dropna(subset=['actualAmountPaid', 'state'])

categorical_fill_cols = ['damageCategory', 'structureType', 'propertyPartOfProject']
for col in categorical_fill_cols:
    if col in df.columns:
        df[col] = df[col].fillna('Unknown')

if 'numberOfProperties' in df.columns:
    df['numberOfProperties'] = df['numberOfProperties'].fillna(1)

# ======================================================================
# 4️⃣ Standardize Categorical Values
categorical_std_cols = ['state', 'county', 'damageCategory', 'structureType', 'propertyPartOfProject']
for col in categorical_std_cols:
    if col in df.columns:
        df[col] = df[col].str.strip().str.title()

if 'damageCategory' in df.columns:
    df['damageCategory'] = df['damageCategory'].replace({
        'N/A': 'Unknown',
        'Major': 'Substantial',
        'Earth Quake': 'Earthquake'
    })

if 'propertyPartOfProject' in df.columns:
    df['propertyPartOfProject'] = df['propertyPartOfProject'].astype(str).str.title()

# ======================================================================
# 5️⃣ Convert Dates/Temporal Fields
if 'programFy' in df.columns:
    df['programFy'] = pd.to_numeric(df['programFy'], errors='coerce')
    df['date_approved_proxy'] = pd.to_datetime('09-30-' + df['programFy'].astype(str))

# ======================================================================
# 6️⃣ Remove Outliers (Optional - Uncomment if Needed)
# upper_limit = df['actualAmountPaid'].quantile(0.99)
# df = df[df['actualAmountPaid'] <= upper_limit]

# ======================================================================
# 7️⃣ Remove Duplicates
df = df.drop_duplicates()

# ======================================================================
# 8️⃣ Derive Total Cost & Filter States
df['totalMitigationCost'] = df['actualAmountPaid'] * df['numberOfProperties']

valid_states = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
    'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
    'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
    'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
    'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
    'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
    'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming', 'District Of Columbia'
]
df = df[df['state'].isin(valid_states)]

# ======================================================================
# 9️⃣ Pandas-Only Encoding for Modeling
df_encoded = df.copy()
categorical_cols = ['state', 'county', 'damageCategory', 'structureType', 'propertyPartOfProject']

for col in categorical_cols:
    if col in df_encoded.columns:
        df_encoded[col] = df_encoded[col].fillna('Unknown')
        df_encoded[col + '_encoded'] = pd.Categorical(df_encoded[col]).codes

# ======================================================================
# 10️⃣ Save Files to Data Folder
data_folder = r"C:\Repos\capstone-project-anjana\data"
df.to_csv(f"{data_folder}/hma_mitigated_properties_cleaned.csv", index=False)
df_encoded.to_csv(f"{data_folder}/hma_mitigated_properties_cleaned_encoded.csv", index=False)

print("✅ Cleaning complete! Files saved in data folder:")
print(f"   - hma_mitigated_properties_cleaned.csv ({df.shape[0]} rows)")
print(f"   - hma_mitigated_properties_cleaned_encoded.csv ({df_encoded.shape[0]} rows)")
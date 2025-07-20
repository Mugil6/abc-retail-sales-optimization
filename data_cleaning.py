import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv("train.csv")

# Preview the dataset
print("Initial Preview:")
print(df.head())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Basic statistics
print("\nDescriptive Stats:")
print(df.describe(include='all'))

# ---------------------------------------------
# 1. Handling Missing Values
# ---------------------------------------------

# Fill numeric columns with median
num_cols = df.select_dtypes(include=[np.number]).columns
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

# Fill categorical columns with mode
cat_cols = df.select_dtypes(include=['object']).columns
for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# ---------------------------------------------
# 2. Standardizing date format (if date/time columns exist)
# ---------------------------------------------

date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
for col in date_columns:
    try:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        print(f"Converted '{col}' to datetime format.")
    except Exception as e:
        print(f"Could not convert '{col}': {e}")

# ---------------------------------------------
# 3. Standardize category name formatting
# ---------------------------------------------

if 'category' in df.columns:
    df['category'] = df['category'].str.strip().str.lower()

# ---------------------------------------------
# 4. Outlier Detection and Removal (IQR method)
# ---------------------------------------------

Q1 = df[num_cols].quantile(0.25)
Q3 = df[num_cols].quantile(0.75)
IQR = Q3 - Q1

# Detect outliers
outliers = ((df[num_cols] < (Q1 - 1.5 * IQR)) | (df[num_cols] > (Q3 + 1.5 * IQR))).any(axis=1)
print(f"\nNumber of outlier rows (IQR method): {outliers.sum()}")

# Remove outliers
df_cleaned = df[~outliers]

# ---------------------------------------------
# 5. Save Cleaned Data and Log
# ---------------------------------------------

# Save cleaned dataset
df_cleaned.to_csv("cleaned_train.csv", index=False)
print("\nCleaned dataset saved as cleaned_train.csv")

# Create a data cleaning log
with open("data_cleaning_log.txt", "w") as log:
    log.write("Data Cleaning Log\n")
    log.write("------------------\n")
    log.write("1. Filled missing numeric values with median.\n")
    log.write("2. Filled missing categorical values with mode.\n")
    log.write("3. Standardized date/time and category columns.\n")
    log.write("4. Removed outliers using IQR method.\n")
    log.write(f"   Total outlier rows removed: {outliers.sum()}\n")
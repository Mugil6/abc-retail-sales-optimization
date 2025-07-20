import pandas as pd
df = pd.read_csv("train.csv")
initial_assessment = df.describe(include='all').transpose()
initial_assessment = initial_assessment.round(2)
print(initial_assessment.head(10))

data_inventory = pd.DataFrame({
    "Column Name": df.columns,
    "Data Type": df.dtypes.values,
    "Missing Values": df.isnull().sum().values,
    "Unique Values": df.nunique().values

})

print(data_inventory)

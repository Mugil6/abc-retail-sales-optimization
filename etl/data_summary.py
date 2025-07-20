import pandas as pd
import os

file_path = "data/train.csv"
output_dir = "reports"
output_file = os.path.join(output_dir, "data_summary.txt")

os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv(file_path, low_memory=False)

summary_lines = []

summary_lines.append(f"Data shape: {df.shape}\n")
summary_lines.append(f"\nColumn types:\n{df.dtypes}\n")
summary_lines.append(f"\nMissing values:\n{df.isnull().sum()}\n")
summary_lines.append(f"\nUnique values:\n{df.nunique()}\n")
summary_lines.append(f"\nSummary stats:\n{df.describe(include='all')}\n")

print("".join(summary_lines))

with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(summary_lines)

print(f"\nSummary report saved to: {output_file}")

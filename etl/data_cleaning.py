import pandas as pd

def clean_data(input_path, output_path):
    df = pd.read_csv(input_path, low_memory=False)
    
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df['StateHoliday'] = df['StateHoliday'].astype(str)

    df['StateHoliday'] = df['StateHoliday'].replace({'0': 'None', 'a': 'Public', 'b': 'Easter', 'c': 'Christmas'})
    
    df = df[~((df['Open'] == 0) & (df['Sales'] == 0))]

    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    clean_data("data/train.csv", "data/train_cleaned.csv")
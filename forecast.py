import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv("train.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df[df["Sales"] > 0]
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["WeekOfYear"] = df["Date"].dt.isocalendar().week.astype(int)
df["DayOfWeek"] = df["Date"].dt.dayofweek + 1
df["Sales_Lag1"] = df.groupby("Store")["Sales"].shift(1)
df["Sales_Lag7"] = df.groupby("Store")["Sales"].shift(7)
df = df.dropna()
df = pd.get_dummies(df, columns=["StateHoliday"])
for col in ["StateHoliday_a", "StateHoliday_b", "StateHoliday_c"]:
    if col not in df.columns:
        df[col] = 0

FEATURES = [
    "Store", "DayOfWeek", "Promo", "SchoolHoliday", "Sales_Lag1",
    "Sales_Lag7", "Year", "Month", "WeekOfYear",
    "StateHoliday_a", "StateHoliday_b", "StateHoliday_c"
]

X = df[FEATURES]
y = df["Sales"]
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, shuffle=False)

model = RandomForestRegressor(n_estimators=100, n_jobs=-1, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_val)
mse = mean_squared_error(y_val, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_val, y_pred)
print(f"Validation RMSE: {rmse:,.2f}  |  MAE: {mae:,.2f}")

joblib.dump(model, "sales_model.pkl")

next_month_start = pd.Timestamp("2025-07-01")
next_month_end = pd.Timestamp("2025-07-31")
dates = pd.date_range(start=next_month_start, end=next_month_end, freq="D")

forecast_rows = []
for store in df["Store"].unique():
    store_df = df[df["Store"] == store].sort_values("Date")
    lag1_val = store_df[store_df["Date"] == pd.Timestamp("2025-06-30")]["Sales"]
    lag1 = lag1_val.values[0] if not lag1_val.empty else store_df["Sales"].iloc[-1]
    lag7_val = store_df[store_df["Date"] == pd.Timestamp("2025-06-24")]["Sales"]
    lag7 = lag7_val.values[0] if not lag7_val.empty else store_df["Sales"].mean()
    future = pd.DataFrame({
        "Date": dates,
        "Store": store,
        "DayOfWeek": dates.dayofweek + 1,
        "Promo": 0,
        "SchoolHoliday": 0,
        "Year": dates.year,
        "Month": dates.month,
        "WeekOfYear": dates.isocalendar().week.astype(int),
        "Sales_Lag1": lag1,
        "Sales_Lag7": lag7,
        "StateHoliday_a": 0,
        "StateHoliday_b": 0,
        "StateHoliday_c": 0
    })
    future["Predicted_Sales"] = model.predict(future[FEATURES])
    total = future["Predicted_Sales"].sum()
    forecast_rows.append({"Store": store, "Predicted_Total_Sales": total, "Forecast_Month": "July 2025"})

forecast_df = pd.DataFrame(forecast_rows).sort_values("Store")
forecast_df.to_csv("next_month_forecast_all_stores.csv", index=False)
print("Saved: next_month_forecast_all_stores.csv")

plt.figure(figsize=(12, 6))
plt.bar(forecast_df["Store"].astype(str), forecast_df["Predicted_Total_Sales"])
plt.xlabel("Store")
plt.ylabel("Predicted Sales")
plt.title("Forecasted Total Sales by Store - July 2025")
plt.tight_layout()
plt.savefig("forecast_bar.png")
plt.close()

plt.figure(figsize=(10, 5))
plt.scatter(y_val.values[:200], y_pred[:200], alpha=0.7)
plt.plot([y_val.min(), y_val.max()], [y_val.min(), y_val.max()], "k--", lw=1)
plt.xlabel("Actual Sales")
plt.ylabel("Predicted Sales")
plt.title("Validation Set: Actual vs Predicted")
plt.tight_layout()
plt.savefig("pred_vs_actual.png")
plt.close()

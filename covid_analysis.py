
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create a folder for output charts
os.makedirs("charts", exist_ok=True)

# STEP 1: LOAD DATASETS
daily = pd.read_csv("Data/full_grouped.csv")
latest = pd.read_csv("Data/country_wise_latest.csv")

print("Datasets loaded successfully!")

# STEP 2: CLEAN DATA
daily.columns = daily.columns.str.strip()
latest.columns = latest.columns.str.strip()

daily = daily.drop_duplicates()
daily["Date"] = pd.to_datetime(daily["Date"], errors="coerce")
daily = daily.dropna(subset=["Date"])

# Standardize country names
daily["Country/Region"] = (
    daily["Country/Region"].astype(str).str.strip()
)

latest["Country/Region"] = (
    latest["Country/Region"].astype(str).str.strip()
)

# Fill missing numeric values
for col in ["Confirmed", "Deaths", "Recovered",
            "New cases", "New deaths", "New recovered"]:
    if col in daily.columns:
        daily[col] = pd.to_numeric(
            daily[col], errors="coerce"
        ).fillna(0)

for col in ["Confirmed", "Deaths", "Recovered"]:
    if col in latest.columns:
        latest[col] = pd.to_numeric(
            latest[col], errors="coerce"
        ).fillna(0)

print("\nSTEP 2: DATA CLEANED")
print("Daily dataset shape:", daily.shape)
print("Missing values remaining:")
print(daily.isnull().sum())

# STEP 3: FILTER INDIA
india = daily[
    daily["Country/Region"].str.lower() == "india"
].copy()

india = india.sort_values("Date")

print("\nSTEP 3: INDIA DATA")
print(india[["Date", "Confirmed", "New cases"]].head())

# STEP 4: PLOT DAILY CASES
# New cases represents daily reported cases in this dataset.
india["Daily cases"] = india["New cases"].clip(lower=0)

plt.figure(figsize=(12, 6))
plt.plot(
    india["Date"],
    india["Daily cases"],
    label="Daily new cases"
)
plt.title("Daily COVID-19 Cases in India")
plt.xlabel("Date")
plt.ylabel("New cases")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("charts/india_daily_cases.png")
plt.show()

# STEP 5: CALCULATE 7-DAY ROLLING AVERAGE
india["Rolling average"] = (
    india["Daily cases"]
    .rolling(window=7, min_periods=1)
    .mean()
)

plt.figure(figsize=(12, 6))
plt.plot(
    india["Date"], india["Daily cases"],
    label="Daily cases", alpha=0.4
)
plt.plot(
    india["Date"], india["Rolling average"],
    label="7-day rolling average", linewidth=2
)
plt.title("India COVID-19 Cases with 7-Day Rolling Average")
plt.xlabel("Date")
plt.ylabel("New cases")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("charts/india_rolling_average.png")
plt.show()

print("\nLatest India rolling-average values:")
print(india[["Date", "Daily cases", "Rolling average"]].tail())

# STEP 6: COUNTRY COMPARISON
# Use the country-level snapshot for the comparison.
latest["Country key"] = (
    latest["Country/Region"].str.lower()
)

country_names = {
    "india": "India",
    "us": "USA",
    "china": "China"
}

comparison = latest[
    latest["Country key"].isin(country_names.keys())
].copy()

comparison["Country"] = comparison["Country key"].map(
    country_names
)

comparison = comparison[
    ["Country", "Confirmed", "Deaths", "Recovered"]
]

print("\nSTEP 6: COUNTRY COMPARISON")
print(comparison.to_string(index=False))

if not comparison.empty:
    comparison.set_index("Country")[
        ["Confirmed", "Deaths", "Recovered"]
    ].plot(kind="bar", figsize=(10, 6))

    plt.title("COVID-19 Comparison: India, USA and China")
    plt.xlabel("Country")
    plt.ylabel("Reported cases")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("charts/country_comparison.png")
    plt.show()

# BONUS: TOP 10 COUNTRIES
top10 = latest.nlargest(10, "Confirmed")

plt.figure(figsize=(11, 6))
plt.bar(top10["Country/Region"], top10["Confirmed"])
plt.title("Top 10 Countries by Confirmed COVID-19 Cases")
plt.xlabel("Country")
plt.ylabel("Confirmed cases")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("charts/top_10_countries.png")
plt.show()

print("\nPROJECT ANALYSIS COMPLETED!")
print("Check the charts folder for your saved graphs.")


# Chart 3: India's 7-day rolling average
india["Rolling average"] = (
    india["Daily cases"].rolling(window=7, min_periods=1).mean()
)

plt.figure(figsize=(12, 6))
plt.plot(india["Date"], india["Daily cases"], label="Daily Cases", alpha=0.5)
plt.plot(india["Date"], india["Rolling average"], label="7-Day Average")
plt.title("India COVID-19: Daily Cases and 7-Day Average")
plt.xlabel("Date")
plt.ylabel("Cases")
plt.legend()
plt.tight_layout()
plt.savefig("charts/india_rolling_average.png")
plt.show()

# Chart 4: India vs USA vs China
comparison = latest[
    latest["Country/Region"].str.strip().str.lower().isin(["india", "us", "china"])
].copy()

comparison.plot(
    x="Country/Region",
    y=["Confirmed", "Deaths", "Recovered"],
    kind="bar",
    figsize=(10, 6)
)
plt.title("COVID-19 Comparison: India, USA and China")
plt.ylabel("Cases")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/country_comparison.png")
plt.show()

print("All four chart files generated.")


# FINAL CHECK: India's actual statistics
print("\nINDIA SUMMARY")
print("Total confirmed cases:", india["Confirmed"].max())
print("Total deaths:", india["Deaths"].max())
print("Total recovered:", india["Recovered"].max())
print("Highest daily cases:", india["Daily cases"].max())
print("Average daily cases:", round(india["Daily cases"].mean(), 2))

print("\nHighest 7-day rolling average:")
print(round(india["Rolling average"].max(), 2))

print("\nCOUNTRY COMPARISON")
print(comparison.to_string(index=False))

print("\nAll analysis checks completed.")


print("\nCHECKING INDIA DATA")

print("Number of India rows:", len(india))
print("Date range:", india["Date"].min(), "to", india["Date"].max())
print("Maximum confirmed cases:", india["Confirmed"].max())
print("Maximum daily cases:", india["Daily cases"].max())

print("\nCountry names available:")
print(sorted(daily["Country/Region"].unique()))

print("\nDIAGNOSTIC COMPLETE")

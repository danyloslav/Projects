import pandas as pd
import matplotlib.pyplot as plt
import export
import gdp_renewables
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================
# DATA LOADING & CLEANING
# ============================================


df = pd.read_csv(
    BASE_DIR / 'owid-energy-data.csv')
print(f"Original dataset: {df.shape[0]} rows, {df.shape[1]} columns")


valid_countries = set(pd.read_csv(
    BASE_DIR / 'owid-energy-data.csv')["country"].unique())

while True:
    user_input = input("Enter countries separated by commas (minimum 5): ")
    COUNTRIES = [country.strip() for country in user_input.split(",")]

    if len(COUNTRIES) < 5:
        print(
            f"Please enter at least 5 countries. You entered {len(COUNTRIES)}.")
        continue

    invalid = [c for c in COUNTRIES if c not in valid_countries]
    if invalid:
        print(f"These countries were not found in the dataset: {invalid}")
        print("Check spelling — names must match exactly, e.g. 'United States' not 'USA'")
        continue

    break

print(f"Analysing: {COUNTRIES}")

while True:
    YEAR_START = int(input("Enter the start year: "))
    YEAR_END = int(input("Enter the final year: "))

    if YEAR_END - YEAR_START < 5:
        print("Year range must be at least 5 years. Try again.")
    elif YEAR_START < 1900 or YEAR_END > 2025:
        print("Years must be between 1900 and 2025.")
    else:
        break

base_cols = ["country", "iso_code", "year", "population", "gdp"]
renewable_cols = ['renewables_share_elec', 'renewables_share_energy',
                  'solar_share_elec', 'wind_share_elec',
                  'carbon_intensity_elec']

# Filter to selected countries and years
df = df[df["country"].isin(COUNTRIES)].copy()
df = df[(df["year"] >= YEAR_START) & (df["year"] <= YEAR_END)]

# Keep only relevant columns
df = df[renewable_cols + base_cols].copy()

# Drop columns with more than 30% missing data
missing_pct = df.isna().sum() / len(df) * 100
cols_to_drop = missing_pct[missing_pct > 30].index
df = df.drop(columns=cols_to_drop)

print(f"Dataset ready: {df.shape[0]} rows, {df.shape[1]} columns")

# ============================================
# PLOTTING FUNCTIONS
# ============================================


def plot_share(column, title, y_label):
    # Scatter plot of a renewable share metric over time, one series per country
    if column not in df.columns:
        print(
            f"Skipping '{column}' — not enough data for selected countries/years")
        return
    plt.figure(figsize=(10, 6))
    for country in COUNTRIES:
        data = df[df["country"] == country]
        plt.scatter(data["year"], data[column], label=country)
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel(y_label)
    plt.legend()
    plt.savefig(
        OUTPUT_DIR / f"{column}.png")


def plot_solar_vs_wind():
    # Solar (solid) vs wind (dashed) share of electricity
    if "solar_share_elec" not in df.columns or "wind_share_elec" not in df.columns:
        print("Skipping Solar vs Wind — not enough data for selected countries/years")
        return
    plt.figure(figsize=(10, 6))
    for country in COUNTRIES:
        data = df[df["country"] == country]
        line = plt.plot(data["year"], data["solar_share_elec"],
                        linestyle='solid', label=f"{country} - Solar")
        color = line[0].get_color()
        plt.plot(data["year"], data["wind_share_elec"],
                 linestyle='dashed', color=color, label=f"{country} - Wind")

    plt.title(f"Solar and Wind Electricity Share {YEAR_START}-{YEAR_END}")
    plt.xlabel("Year")
    plt.ylabel("Wind and Solar Share of Electricity (%)")
    plt.legend()
    plt.savefig(
        OUTPUT_DIR / "solar_vs_wind.png")


# ============================================
# MAIN
# ============================================

# Plot 1 — electricity mix
plot_share("renewables_share_elec",
           f"Renewable Share of Electricity ({YEAR_START}-{YEAR_END})",
           "Renewables Share of Electricity (%)")

# Plot 2 — total energy
plot_share("renewables_share_energy",
           f"Renewable Share of Total Energy  ({YEAR_START}-{YEAR_END})",
           "Renewables Share of Energy (%)")

# Plot 3 — solar vs wind adoption per country
plot_solar_vs_wind()

# Plot 4 - GDP per capits vs Renewable Share of Total
gdp_renewables.plot_gdp_vs_renewables(YEAR_START, YEAR_END)


df.to_excel(BASE_DIR / "energy_data.xlsx",
            index=False, sheet_name="Energy Data")

print(f"Dataset ready: {df.shape[0]} rows, {df.shape[1]} columns")

export.add_chart_sheets(YEAR_START, YEAR_END)
plt.show()

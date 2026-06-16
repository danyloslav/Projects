import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def plot_gdp_vs_renewables(year_start, year_end):

    df = pd.read_csv(BASE_DIR / 'owid-energy-data.csv')

    columns_needed = ['gdp', 'renewables_share_elec', 'population']
    df = df.dropna(subset=columns_needed).copy()
    df = df[(df["year"] >= year_start) & (df["year"] <= year_end)].copy()
    df = df[df["country"] != "World"]

    df = df.groupby("country")[columns_needed].mean().reset_index().copy()
    df["gdp_per_capita"] = df["gdp"] / df["population"]

    # Trend line
    coeffs = np.polyfit(df["gdp_per_capita"], df["renewables_share_elec"], 1)
    trend_x = np.linspace(df["gdp_per_capita"].min(),
                          df["gdp_per_capita"].max(), 100)
    trend_y = np.polyval(coeffs, trend_x)

    plt.figure(figsize=(10, 6))
    plt.scatter(df["gdp_per_capita"], df["renewables_share_elec"], alpha=0.6)
    plt.plot(trend_x, trend_y, color='red', label='Trend')
    plt.title(f"Renewables vs GDP per Capita ({year_start}-{year_end})")
    plt.xlabel(f"GDP per Capita average({year_start}-{year_end})$)")
    plt.ylabel("Renewables Share of Electricity (%)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(OUTPUT_DIR / "gdp_vs_renewables.png")

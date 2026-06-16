# Global Energy Transition Analysis (1900-2026)

A Python data analysis project exploring renewable energy adoption trends across countries, built on a real-world dataset of 23,000+ rows and 130 columns.

---

## What it does

The script takes user input for countries and a year range, cleans and filters the dataset, generates 4 visualisations, and automatically produces a formatted Excel report with embedded charts.

Run it once — get a complete, updated report.

---

## Dataset

**Global Energy Transition & Renewables (1900-2026)**  
Source: WADDAH ALI via Kaggle  
Original size: 23,232 rows × 130 columns  
Coverage: 200+ countries, 120+ years of energy data

---

## Key findings

- **Weak negative relationship between GDP per capita and renewable electricity share**
  — wealthier countries do not consistently have higher renewable adoption
  
- **Nordic countries are outliers on the high end**
  — Norway, Sweden, and Denmark lead in renewable electricity share, driven by hydro and wind
  
- **Middle Eastern countries are outliers on the low end**
  — Qatar, Saudi Arabia, and Kuwait are among the richest countries per capita yet have near-zero renewable electricity,
   due to relience on oil and gas
  
- **Solar and wind adoption accelerated sharply after 2015** across most countries in the dataset

---

## Project structure

```
project/
├── projct.py           — main script: user input, data cleaning, plots
├── gdp_renewables.py   — GDP per capita vs renewable share analysis
├── export.py           — automated Excel report with formatted chart sheets
├── owid-energy-data.csv
└── outputs/
    ├── renewables_share_elec.png
    ├── renewables_share_energy.png
    ├── solar_vs_wind.png
    ├── gdp_vs_renewables.png
    └── energy_data.xlsx
```

---

## How to run

1. Install dependencies:
```bash
pip install pandas matplotlib numpy openpyxl
```

2. Place `owid-energy-data.csv` in the project folder

3. Run the main script:
```bash
python3 projct.py
```

4. Enter at least 5 countries and a year range of at least 5 years when prompted

5. Open `energy_data.xlsx` for the full report

---

## Libraries used

- **Pandas** — data loading, cleaning, filtering, Excel export
- **Matplotlib** — scatter plots, line plots, visualisations
- **NumPy** — trend line calculation (polyfit)
- **openpyxl** — formatted Excel report with embedded charts

---

## Example output

**Plots generated:**
1. Renewable share of electricity over time — per country
2. Renewable share of total energy over time — per country
3. Solar vs wind adoption — solid/dashed lines per country
4. GDP per capita vs renewable electricity share — global scatter with trend line

**Excel report:**
- Sheet 1: cleaned data table
- Sheets 2-5: formatted charts with titles

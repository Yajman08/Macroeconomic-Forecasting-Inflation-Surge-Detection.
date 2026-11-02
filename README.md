# Macroeconomic Forecasting and Inflation Surge Detection

**A multi-indicator machine-learning framework using FRED data**

This repository contains the research notebook, FRED source datasets, processed datasets, forecast/evaluation CSVs, charts, final research report, and interactive presentation.

> This is an independent FRED-based research project inspired by macroeconomic forecasting. It is **not** a reproduction of Goldman Sachs' proprietary forecasting pipeline.

## Project objective

Explore and forecast year-over-year Producer Price Index (PPI) inflation for **Semiconductor and Other Electronic Component Manufacturing** and investigate whether sharp inflation accelerations can be identified using macroeconomic and industry indicators.

The project also includes raw-material forecasts and an illustrative phone-cost pass-through scenario. The phone scenario is a sensitivity illustration, **not** a validated retail smartphone-price forecast.

## Repository structure

```text
.
├── notebooks/
│   ├── Inflation_Forecasting_Research.ipynb
│   └── Inflation_Forecasting_Earlier_Version.ipynb
├── data/
│   ├── raw/                  # Original monthly FRED series
│   └── processed/            # Merged master and model-ready datasets
├── outputs/
│   ├── forecasts/            # Final PPI, raw-material and scenario forecasts
│   └── evaluation/           # Model comparisons, intervals and backtest outputs
├── figures/                  # EDA, model, diagnostics and forecast charts
├── reports/                  # Research report (PDF)
├── presentation/
│   └── index.html            # Self-contained interactive presentation
├── src/
│   └── build_semiconductor_dataset.py
├── requirements.txt
└── README.md
```

## Data sources and indicators

The six monthly FRED series used in the core analysis are:

| FRED series ID | Indicator | Role |
|---|---|---|
| `PCU3344133441` | Semiconductor and Other Electronic Component Manufacturing PPI | Target |
| `PCOPPUSDM` | Global copper price | Raw-material indicator |
| `PALUMUSDM` | Global aluminum price | Raw-material indicator |
| `PNICKUSDM` | Global nickel price | Raw-material indicator |
| `CAPUTLG3344S` | Semiconductor manufacturing capacity utilization | Industry indicator |
| `IPG3344S` | Semiconductor industrial production | Industry indicator |

The data are monthly. The original merged dataset spans January 1992 to September 2026 in the supplied project snapshot. FRED observations may be revised; a strict real-time backtest should use ALFRED vintages and account for each series' release calendar.

## Methodology overview

The notebook documents the end-to-end workflow, including:

1. Data loading, merging, missing-value and duplicate checks.
2. Exploratory data analysis, descriptive statistics and correlation analysis.
3. Stationarity checks (including the Augmented Dickey–Fuller test) and transformations.
4. Inflation target construction, lag features and momentum features.
5. Chronological train/validation/test design and baseline comparisons.
6. Machine-learning experiments (including Ridge, Random Forest and XGBoost where present in the notebook).
7. ARIMA/SARIMA/SARIMAX time-series experiments, rolling/expanding windows and exogenous-variable ablations.
8. Residual diagnostics and empirical/conformal prediction intervals.
9. Inflation-surge threshold analysis and warning outputs.
10. Direct multi-horizon forecasts for H1–H6 and illustrative raw-material/phone-cost scenarios.

**Important:** The notebook contains multiple experimental stages and forecast files. `Final_Corrected_PPI_Forecast.csv` is the latest corrected direct H1–H6 forecast output in this project snapshot. `Final_Six_Month_PPI_Forecast.csv` is retained as an earlier experiment and should not be confused with the corrected forecast.

## Main files

- `notebooks/Inflation_Forecasting_Research.ipynb` — primary research workflow.
- `data/processed/semiconductor_inflation_master_dataset.csv` — merged dataset.
- `data/processed/semiconductor_inflation_model_ready.csv` — model-ready dataset.
- `outputs/forecasts/Final_Corrected_PPI_Forecast.csv` — corrected H1–H6 PPI inflation forecast.
- `outputs/forecasts/Final_Inflation_Surge_Warnings.csv` — surge warning output.
- `outputs/forecasts/Final_Raw_Material_Forecasts.csv` — raw-material forecast output.
- `outputs/forecasts/Final_Illustrative_Phone_Cost_Scenario.csv` — illustrative cost-pass-through scenario.
- `outputs/evaluation/` — model evaluation and prediction interval outputs.
- `reports/` — final PDF research report.
- `presentation/index.html` — interactive widescreen presentation.

## Run the notebook

### Option A: Google Colab

1. Open `notebooks/Inflation_Forecasting_Research.ipynb` in Google Colab.
2. Upload `data/processed/semiconductor_inflation_master_dataset.csv` when the notebook requests a CSV upload.
3. Run cells from top to bottom.
4. If a cell requests additional files or an optional package, follow the notebook's prompt and install the package listed in `requirements.txt`.

### Option B: Local environment

```bash
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
jupyter notebook
```

Open the primary notebook. Some cells were originally authored for Google Colab and use `google.colab.files.upload`; in a local Jupyter environment, replace that upload cell with a `pandas.read_csv()` call pointing to the processed master dataset.

## View the presentation

Open `presentation/index.html` in Chrome or Edge. It is self-contained and does not need a frontend build step.

To publish it with GitHub Pages, configure Pages to deploy from the `main` branch and the `/presentation` folder (or move/copy `presentation/index.html` to the repository root if you want the presentation at the root URL).

## Interpretation and limitations

- The target is a **producer price index inflation measure**, not semiconductor unit prices or consumer electronics retail prices.
- The broad BLS NAICS 3344 category and the narrower FRED target series should not be treated as identical scopes.
- The 2026 BLS sub-industry comparisons indicate different price movements across sub-industries; they do not, by themselves, establish the cause of the observed increase.
- Prediction intervals are empirical research estimates. Temporal dependence and structural change mean nominal coverage should not be interpreted as a guaranteed future coverage rate.
- Overlapping forecast horizons and repeated model experimentation can affect statistical comparisons. Results should be described as exploratory unless evaluated on a genuinely untouched holdout period.
- Raw-material and phone-cost scenario outputs are conditional estimates, not causal claims.

## Citation and acknowledgement

Data are sourced from the Federal Reserve Bank of St. Louis FRED database and relevant Bureau of Labor Statistics Producer Price Index releases. Please retain the original series IDs and source attribution when reusing the data.

## License

No license has been specified. Add a license only after deciding how you want others to reuse the notebook, data-processing code, and presentation.

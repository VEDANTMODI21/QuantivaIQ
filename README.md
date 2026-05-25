# QuantivaIQ

Enterprise retail analytics with live Power BI integration, data export support, and a deployable Flask preview application.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Power BI](https://img.shields.io/badge/Power%20BI-DirectQuery-F2C811?style=flat-square&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)

---

## Overview

QuantivaIQ is a retail analytics platform that combines data warehousing, ETL, fraud detection, forecasting, and Power BI reporting into a single repository. It supports both live PostgreSQL-backed dashboards and CSV export feeds for Power BI Desktop.

## Key Features

- Power BI DirectQuery support for live dashboards
- `dashboards/powerbi_data/` CSV export ready for import into Power BI
- PostgreSQL warehouse with ETL and materialized views
- Fraud detection and customer segmentation
- Flask-based preview dashboard at `http://localhost:8000`
- Docker Compose deployment for local development
- Vercel deployment support for the Flask web preview

## Tech Stack

- Python 3.9+
- PostgreSQL 15+
- SQLAlchemy, pandas, scikit-learn
- Flask web preview
- Docker Compose
- Power BI Desktop

## Quick Start

### Prerequisites

- Python 3.9+ installed
- `pip` available
- Docker Desktop installed for container deployment
- Power BI Desktop installed for reporting

### Option A: Docker Compose (Recommended)

1. Clone the repository:
   ```powershell
   git clone https://github.com/VEDANTMODI21/QuantivaIQ.git
   cd QuantivaIQ
   ```

2. Copy the environment template and update values if needed:
   ```powershell
   cp .env.example .env
   ```

3. Start PostgreSQL with Docker Compose:
   ```powershell
   docker compose up -d postgres
   ```

4. Initialise the schema and seed data:
   ```powershell
   docker compose --profile setup run --rm setup
   ```

5. Start the Flask preview and live simulator:
   ```powershell
   docker compose up -d web simulator
   ```

6. Open the browser preview:
   ```text
   http://localhost:8000
   ```

### Option B: Local PostgreSQL

1. Install PostgreSQL and create a database user.
2. Copy the environment file:
   ```powershell
   cp .env.example .env
   ```
3. Set `DB_DRIVER=postgres` and confirm `DB_HOST=localhost`.
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Run database setup:
   ```powershell
   python python/db_setup.py
   ```
6. Run the ETL pipeline:
   ```powershell
   python python/etl_pipeline.py
   ```
7. Start the simulator and web preview:
   ```powershell
   python python/live_data_generator.py
   python python/web_dashboard.py
   ```

### Option C: In-Memory Demo

For a fast demo without PostgreSQL:

```powershell
pip install -r requirements.txt
python run_demo.py
```

## Power BI Integration

QuantivaIQ supports two Power BI workflows:

1. Live data through PostgreSQL DirectQuery
2. CSV export import using local datasets in `dashboards/powerbi_data/`

### Live DirectQuery Setup

1. Confirm the PostgreSQL database is running.
2. Open Power BI Desktop.
3. Select **Get Data → PostgreSQL database**.
4. Enter:
   - Server: `localhost`
   - Database: `quantivaiq`
   - Data Connectivity Mode: **DirectQuery**
   - Username: `postgres`
   - Password: `postgres`
5. Select the materialized views and tables required for the report.

> Use DirectQuery so Power BI reflects live simulator updates. Import mode caches a snapshot and does not refresh automatically.

### Recommended Views and Tables

- `mv_daily_revenue`
- `mv_customer_kpis`
- `mv_product_performance`
- `mv_fraud_summary`
- `mv_inventory_status`
- `customer_segments`
- `orders`
- `order_items`
- `products`
- `fraud_logs`

### Refreshing Power BI Views

After data updates, refresh the warehouse views with:

```powershell
python python/refresh_powerbi_views.py
```

This command only applies to PostgreSQL mode.

## Power BI CSV Export

The repository includes a ready-to-use CSV folder at `dashboards/powerbi_data/`.
Regenerate the export files with:

```powershell
python python/export_powerbi_csv.py
```

Power BI Desktop import options:

- **Get Data → Folder** to import all exported CSV files
- **Get Data → Text/CSV** to select individual files

Recommended dataset files:

- `customers.csv`
- `orders.csv`
- `order_items.csv`
- `products.csv`
- `inventory.csv`
- `payments.csv`
- `refunds.csv`
- `fraud_logs.csv`
- `mv_daily_revenue.csv`
- `mv_customer_kpis.csv`
- `mv_product_performance.csv`
- `mv_fraud_summary.csv`
- `mv_inventory_status.csv`

## Vercel Deployment

This repository is configured for Vercel deployment using `vercel.json` and `pyproject.toml`.

### Required files

- `vercel.json`
- `pyproject.toml`
- `requirements.txt`

### Recommended environment variables

For a simple demo using SQLite:

```text
DB_DRIVER=sqlite
SQLITE_DB_PATH=quantivaiq.db
```

For PostgreSQL deployment:

```text
DB_DRIVER=postgres
DB_HOST=<host>
DB_PORT=5432
DB_NAME=quantivaiq
DB_USER=postgres
DB_PASSWORD=<password>
```

### Deploying from the repository

1. Install the Vercel CLI if needed:
   ```powershell
   npm install -g vercel
   ```
2. From the repository root, run:
   ```powershell
   vercel login
   vercel --prod
   ```
3. Set the same environment variables in the Vercel project settings.
4. Redeploy after changes.

## Project Structure

```
QuantivaIQ/
├── datasets/                        # source CSV datasets
├── dashboards/                      # Power BI templates and exported CSV data
│   ├── powerbi_data/                # generated CSV exports for Power BI
│   ├── powerbi_dashboard_template.md
│   └── powerbi_template.md
├── notebooks/                       # exploratory and prototype notebooks
├── python/                          # main Python application and analytics code
│   ├── config.py
│   ├── db_setup.py
│   ├── etl_pipeline.py
│   ├── export_powerbi_csv.py
│   ├── fraud_detection.py
│   ├── forecasting.py
│   ├── live_data_generator.py
│   ├── refresh_powerbi_views.py
│   ├── recommendation_engine.py
│   ├── web_dashboard.py
│   └── utils.py
├── reports/
├── sql/
├── Dockerfile
├── docker-compose.yml
├── deploy.bat
├── deploy.ps1
├── pyproject.toml
├── requirements.txt
├── vercel.json
├── .env.example
└── README.md
```

## Notes

- The Flask preview app is independent of Power BI and is intended as a browser-based dashboard companion.
- Use the CSV export folder when direct database access is not available.
- For live dashboards, Power BI should connect to PostgreSQL in DirectQuery mode.

## Troubleshooting

- If Power BI cannot connect, verify `DB_HOST`, `DB_PORT`, and firewall rules.
- If data is stale, confirm DirectQuery is selected and refresh the report pages.
- If setup fails, re-run the Docker Compose setup step:
  ```powershell
  docker compose --profile setup run --rm setup
  ```

# QuantivaIQ — AI-Powered Retail Intelligence & Fraud Analytics Platform

> Enterprise-grade end-to-end Business Analytics and Fraud Intelligence platform for modern retail and e-commerce ecosystems — with live Power BI integration.

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Power BI](https://img.shields.io/badge/Power%20BI-DirectQuery-F2C811?style=flat-square&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
  - [Option A: Docker (Recommended)](#option-a-docker-recommended)
  - [Option B: Local PostgreSQL](#option-b-local-postgresql)
  - [Option C: In-Memory Demo](#option-c-in-memory-demo-no-database-required)
- [Power BI Live Integration](#power-bi-live-integration)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Starting the Stack](#starting-the-stack)
  - [Connecting Power BI Desktop](#connecting-power-bi-desktop)
  - [Selecting Views and Tables](#selecting-views-and-tables)
  - [Enabling Live Page Refresh](#enabling-live-page-refresh)
- [DAX Measures Reference](#dax-measures-reference)
  - [Revenue and Sales](#revenue--sales-measures)
  - [Customer and Retention](#customer--retention-measures)
  - [Fraud and Risk](#fraud--risk-measures)
  - [Inventory and Products](#inventory--product-measures)
  - [Formatting Helpers](#formatting--ui-helpers)
- [Recommended Dashboard Tabs](#recommended-dashboard-tabs)
- [Core Features](#core-features)
- [Enterprise Data Warehouse](#enterprise-data-warehouse)
- [Advanced SQL Analytics](#advanced-sql-analytics)
- [ETL Pipeline](#etl-pipeline)
- [Fraud Detection Engine](#fraud-detection-engine)
- [Customer Intelligence System](#customer-intelligence-system)
- [Demand Forecasting](#demand-forecasting)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## Overview

QuantivaIQ simulates a real-world analytics architecture similar to platforms used by Amazon, Flipkart, and Myntra. It performs:

- **Real-time business analytics** — revenue, orders, regional trends
- **Fraud detection** — ML-based anomaly detection on live transactions
- **Customer intelligence** — RFM segmentation, churn prediction, CLTV
- **Demand forecasting** — ARIMA, Prophet, Linear Regression
- **KPI monitoring** — live Power BI dashboards with DirectQuery + auto-refresh
- **Executive reporting** — automated ETL into a structured PostgreSQL warehouse

---

## System Architecture

```
Historical Datasets / Simulated Live Data
                ↓
        Python ETL Pipelines
     (etl_pipeline.py, db_setup.py)
                ↓
      PostgreSQL Data Warehouse
       (Docker or Local — port 5432)
                ↓
      Advanced SQL Analytics Layer
       (Materialized Views — mv_*)
                ↓
     Machine Learning Intelligence
   (fraud_detection.py, forecasting.py)
                ↓
    Power BI Real-Time Dashboards
     (DirectQuery + 5s Page Refresh)
                ↓
      Business Insights & Alerts
```

| Layer | Component | Role |
|---|---|---|
| Simulation | `live_data_generator.py` | Inserts orders, payments, fraud events every N seconds |
| ETL | `etl_pipeline.py` | Loads, transforms, normalises data into warehouse tables |
| Warehouse | PostgreSQL (Docker) | Source of truth — all analytics views live here |
| Views | `mv_*` materialized views | Pre-aggregated KPI tables refreshed on each load cycle |
| BI Layer | Power BI DirectQuery | Queries views on-demand; Page Refresh re-queries every 5 s |
| Web Preview | `web_dashboard.py` (Flask) | Browser preview at `localhost:8000` — independent of Power BI |

> **Note:** The Flask dashboard at `localhost:8000` and Power BI are **independent consumers** of the same PostgreSQL database. Running both simultaneously is safe and recommended during development.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Database | PostgreSQL 15+ |
| Backend Analytics | Python 3.9+ |
| Data Processing | pandas, numpy |
| Machine Learning | scikit-learn |
| Dashboarding | Power BI (DirectQuery) |
| Database ORM | SQLAlchemy |
| Real-Time Simulation | faker, random, schedule |
| Containerisation | Docker, Docker Compose |
| IDE | VS Code |
| Notebook Environment | Jupyter Notebook |
| Version Control | Git & GitHub |

---

## Quick Start

### Option A: Docker (Recommended)

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop) and ensure the daemon is running.

2. Clone the repository:
   ```bash
   git clone https://github.com/VEDANTMODI21/QuantivaIQ.git
   cd QuantivaIQ
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy and configure the environment file:
   ```bash
   cp .env.example .env
   ```
   > Set `DB_HOST=postgres` inside `.env` for Docker Compose containers. Keep `DB_HOST=localhost` when connecting Power BI Desktop from your host machine.

5. Start PostgreSQL container:
   ```bash
   docker compose up -d postgres
   ```

6. Wait 10 seconds, then initialise the schema and seed the warehouse:
   ```bash
   docker compose --profile setup run --rm setup
   ```

7. Start the web dashboard and live simulator:
   ```bash
   docker compose up -d web simulator
   ```

8. Open the browser dashboard:
   ```
   http://localhost:8000
   ```

**One-command alternative (PowerShell):**
```powershell
./deploy.ps1
```

---

### Option B: Local PostgreSQL

1. Install [PostgreSQL 15+](https://www.postgresql.org/download/).

2. Create the database and user:
   ```sql
   CREATE DATABASE quantivaiq;
   CREATE USER postgres WITH PASSWORD 'postgres';
   ALTER ROLE postgres SET client_encoding TO 'utf8';
   ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
   ALTER ROLE postgres SET default_transaction_deferrable TO on;
   ALTER ROLE postgres SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE quantivaiq TO postgres;
   ```

3. Clone and install:
   ```bash
   git clone https://github.com/VEDANTMODI21/QuantivaIQ.git
   cd QuantivaIQ
   pip install -r requirements.txt
   ```

4. Configure `.env` (copy from `.env.example`).

5. Initialise database schema:
   ```bash
   python python/db_setup.py
   ```

6. Run the ETL pipeline:
   ```bash
   python python/etl_pipeline.py
   ```

7. Start the live simulator:
   ```bash
   python python/live_data_generator.py
   ```

8. Launch the web dashboard:
   ```bash
   python python/web_dashboard.py
   ```

---

### Option C: In-Memory Demo (No Database Required)

```bash
git clone https://github.com/VEDANTMODI21/QuantivaIQ.git
cd QuantivaIQ
pip install -r requirements.txt
python run_demo.py
```

Runs a complete analytics pipeline in-memory — no PostgreSQL needed.

---

## Power BI Live Integration

### Prerequisites

- Docker Desktop installed and daemon running
- PostgreSQL 15+ accessible on port `5432`
- Power BI Desktop (latest)
- Python 3.9+ with all `requirements.txt` packages installed
- OS firewall open on ports `8000` and `5432`

---

### Environment Variables

| Variable | Docker Value | Local Value |
|---|---|---|
| `DB_HOST` | `postgres` | `localhost` |
| `DB_PORT` | `5432` | `5432` |
| `DB_NAME` | `quantivaiq` | `quantivaiq` |
| `DB_USER` | `postgres` | `postgres` |
| `DB_PASSWORD` | `postgres` | `postgres` |
| `SIMULATION_INTERVAL_SECONDS` | `5` | `5` |

---

### Starting the Stack

Verify all services are running before connecting Power BI:

```bash
docker compose ps
```

All three — `postgres`, `web`, `simulator` — should show status `Up`.

| Service | URL / Address | Notes |
|---|---|---|
| Flask Dashboard | `http://localhost:8000` | Browser preview — independent of Power BI |
| PostgreSQL (local PBI) | `localhost:5432` | Use when Power BI runs on the same machine |
| PostgreSQL (remote PBI) | `<host-ip>:5432` | Use when Power BI is on another device |
| Flask (remote device) | `http://<host-ip>:8000` | Flask binds `0.0.0.0` — reachable network-wide |

---

### Manual Power BI Refresh

If you need to refresh the Power BI materialized views without rerunning the entire ETL pipeline, use:

```bash
python python/refresh_powerbi_views.py
```

This script works only in PostgreSQL mode and is useful after data loads or direct database updates.

---

### Connecting Power BI Desktop

1. Open Power BI Desktop.
2. Click **Get Data** → **More…** → **Database** → **PostgreSQL database**.
3. Enter connection details:

   | Field | Value |
   |---|---|
   | Server | `localhost` (same machine) or `<host-ip>` (remote) |
   | Database | `quantivaiq` |
   | Data Connectivity Mode | **DirectQuery** |
   | Username | `postgres` |
   | Password | `postgres` |

> ⚠️ **Always choose DirectQuery — not Import.** Import mode caches a snapshot and will NOT reflect live simulator updates.

---

### Selecting Views and Tables

In the Navigator pane, choose these Power BI-optimized views and tables:

| View / Table | Dashboard Module | Key Columns |
|---|---|---|
| `mv_daily_revenue` | Executive | `date`, `total_revenue`, `order_count` |
| `mv_customer_kpis` | Customer | `customer_id`, `total_orders`, `total_spend` |
| `mv_product_performance` | Inventory | `product_id`, `product_name`, `total_units_sold`, `total_revenue` |
| `mv_fraud_summary` | Fraud | `fraud_type`, `detection_date`, `fraud_incidents` |
| `mv_inventory_status` | Inventory | `warehouse_location`, `quantity_on_hand`, `reorder_level` |
| `customer_segments` | Customer | `customer_id`, `segment_name`, `rfm_score` |
| `fraud_logs` | Fraud | `order_id`, `customer_id`, `risk_score`, `fraud_type` |
| `orders` | Executive | `order_id`, `customer_id`, `total_amount`, `order_date`, `region` |
| `order_items` | Executive | `order_id`, `product_id`, `quantity`, `unit_price`, `discount` |
| `products` | Inventory | `product_id`, `product_name`, `cost_price`, `stock_quantity`, `reorder_level` |

---

### Enabling Live Page Refresh

This makes the dashboard react to `python/live_data_generator.py` in near real-time:

1. In Power BI Desktop, select any report page.
2. Open the **Format** pane (paint roller icon).
3. Expand **Page refresh**.
4. Toggle **Auto page refresh** to ON.
5. Set refresh interval to **5 seconds** (matching `SIMULATION_INTERVAL_SECONDS`).

> **Note:** 5-second refresh is appropriate for development. For production, use 30–60 seconds to reduce query load.

---

## DAX Measures Reference

### Revenue & Sales Measures

```dax
Total Revenue = SUM(orders[total_amount])

PM Revenue = CALCULATE([Total Revenue], PREVIOUSMONTH('Date'[Date]))

MoM Growth % = DIVIDE([Total Revenue] - [PM Revenue], [PM Revenue], 0)

AOV = DIVIDE([Total Revenue], DISTINCTCOUNT(orders[order_id]))

Gross Profit = SUMX(order_items,
    order_items[quantity] * (order_items[unit_price] - RELATED(products[cost_price])))

Profit Margin % = DIVIDE([Gross Profit], [Total Revenue], 0)

YTD Revenue = TOTALYTD([Total Revenue], 'Date'[Date])

Total Discount = SUM(order_items[discount])
```

### Customer & Retention Measures

```dax
Total Customers = DISTINCTCOUNT(customers[customer_id])

Active Customers 30D = CALCULATE(
    DISTINCTCOUNT(orders[customer_id]),
    orders[order_date] >= TODAY() - 30)

New Customers = CALCULATE(
    DISTINCTCOUNT(customers[customer_id]),
    customers[registration_date] >= DATEADD(LASTDATE('Date'[Date]), -1, MONTH))

Retention Rate % = DIVIDE([Active Customers 30D], [Total Customers], 0)

Churn Rate % = 1 - [Retention Rate %]

Repeat Purchase Rate =
VAR CustomersWithMultipleOrders =
    FILTER(VALUES(orders[customer_id]),
        CALCULATE(COUNT(orders[order_id])) > 1)
RETURN DIVIDE(COUNTROWS(CustomersWithMultipleOrders), [Total Customers])

Avg CLTV = DIVIDE([Total Revenue], [Total Customers])
```

### Fraud & Risk Measures

```dax
Total Fraud Txns = COUNTROWS(fraud_logs)

Fraud Rate % = DIVIDE([Total Fraud Txns], COUNTROWS(orders), 0)

Value at Risk = CALCULATE(
    SUM(orders[total_amount]),
    USERELATIONSHIP(orders[order_id], fraud_logs[order_id]))

High Risk Customers = CALCULATE(
    DISTINCTCOUNT(fraud_logs[customer_id]),
    fraud_logs[risk_score] >= 80)

Avg Risk Score = AVERAGE(fraud_logs[risk_score])

Total Refunds = SUM(refunds[refund_amount])

Refund Rate % = DIVIDE([Total Refunds], [Total Revenue], 0)
```

### Inventory & Product Measures

```dax
Total Units Sold = SUM(order_items[quantity])

Total Inventory Value = SUMX(products,
    products[stock_quantity] * products[cost_price])

Out of Stock Items = CALCULATE(
    COUNTROWS(products),
    products[stock_quantity] <= 0)

Low Stock Items = CALCULATE(
    COUNTROWS(products),
    products[stock_quantity] <= products[reorder_level])

Inventory Turnover = DIVIDE(
    SUM(order_items[quantity]),
    AVERAGE(products[stock_quantity]), 0)

Top Product Revenue = MAXX(VALUES(products[product_name]), [Total Revenue])
```

### Formatting & UI Helpers

```dax
MoM Color = IF([MoM Growth %] > 0, "Green", "Red")

Risk Color = SWITCH(TRUE(),
    [Avg Risk Score] >= 80, "#FF0000",
    [Avg Risk Score] >= 50, "#FFA500",
    "#00FF00")

Dashboard Title = "QuantivaIQ Analytics - " & FORMAT(TODAY(), "MMMM YYYY")
```

---

## Recommended Dashboard Tabs

### Executive Dashboard

| Visual Type | Fields / Measure | Purpose |
|---|---|---|
| KPI Card | `Total Revenue` | Primary revenue headline |
| KPI Card | `MoM Growth %` (colour: `MoM Color`) | Revenue trend at a glance |
| KPI Card | `AOV` | Average order health |
| KPI Card | `YTD Revenue` | Year-to-date progress |
| Line Chart | `mv_daily_revenue[date]` vs `Total Revenue` | Revenue trend over time |
| Bar Chart | `orders[region]` vs `Total Revenue` | Revenue by region |
| Treemap | `products[product_name]` vs `Gross Profit` | Profitability by product |

### Customer Dashboard

| Visual Type | Fields / Measure | Purpose |
|---|---|---|
| KPI Card | `Total Customers` | Total customer base size |
| KPI Card | `Active Customers 30D` | Engagement snapshot |
| KPI Card | `Retention Rate %` | Retention health |
| KPI Card | `Avg CLTV` | Customer lifetime value |
| Donut Chart | `customer_segments[segment_name]` | RFM segment distribution |
| Table | `customer_segments` — all columns | Segment drill-through |
| Line Chart | `New Customers` over time | Acquisition trend |

### Fraud Dashboard

| Visual Type | Fields / Measure | Purpose |
|---|---|---|
| KPI Card | `Total Fraud Txns` | Incident count |
| KPI Card | `Fraud Rate %` | % of total orders flagged |
| KPI Card | `Value at Risk` | Total revenue exposed |
| KPI Card | `Avg Risk Score` (colour: `Risk Color`) | Current threat level |
| Bar Chart | `fraud_logs[fraud_type]` vs count | Fraud type breakdown |
| Map / Scatter | `orders[region]` vs `Fraud Rate %` | Geographic fraud heatmap |
| Table | `fraud_logs` — high `risk_score` rows | Incident drill-through |

### Inventory Dashboard

| Visual Type | Fields / Measure | Purpose |
|---|---|---|
| KPI Card | `Total Inventory Value` | Stock valuation |
| KPI Card | `Out of Stock Items` | Zero-stock alert count |
| KPI Card | `Low Stock Items` | Reorder alert count |
| KPI Card | `Inventory Turnover` | Efficiency metric |
| Bar Chart | `mv_inventory_status[product_name]` vs `quantity_on_hand` | Stock levels |
| Gauge | `Inventory Turnover` vs target` | Turnover vs benchmark |

---

## Core Features

- Real-time business analytics
- Fraud detection engine
- Customer segmentation
- Customer churn prediction
- Sales forecasting
- Inventory analytics
- KPI monitoring
- Recommendation system
- Live Power BI dashboards
- Automated ETL pipelines
- Real-time transaction simulation

---

## Enterprise Data Warehouse

### Database Domains

| Domain | Tables |
|---|---|
| Customer | `customers`, `customer_sessions`, `customer_segments` |
| Product | `products`, `categories`, `suppliers`, `inventory` |
| Sales | `orders`, `order_items`, `payments`, `refunds` |
| Fraud | `fraud_logs`, `suspicious_transactions` |
| Feedback | `reviews`, `ratings` |

---

## Advanced SQL Analytics

SQL concepts used across `sql/analytics_queries.sql`:

- Complex JOINs and CTEs
- Window Functions
- Views and Materialized Views (`mv_*`)
- Stored Procedures and Triggers
- Transactions, Indexing, and Query Optimization

---

## ETL Pipeline

### Extract
- Retail datasets
- Transaction datasets
- Simulated live data streams via `live_data_generator.py`

### Transform
- Missing value handling
- Duplicate removal
- Data normalisation and outlier detection
- Feature engineering for ML models

### Load
- Automated loading into PostgreSQL warehouse tables
- Materialized view refresh on each pipeline run

---

## Fraud Detection Engine

### Fraud Scenarios Detected
- Abnormal transaction frequency
- Excessive refund requests
- Suspicious payment patterns
- Bot-generated transactions

### ML Algorithms
- Isolation Forest
- Z-Score Anomaly Detection
- Clustering-Based Detection

---

## Customer Intelligence System

### RFM Segmentation

| Segment | Description |
|---|---|
| VIP Customers | High recency, frequency, and monetary value |
| Loyal Customers | Consistent purchasers with strong engagement |
| At-Risk Customers | Previously active, declining engagement |
| Inactive Customers | No recent activity — churn likely |

### Predictive Analytics
- **Churn Prediction** — Logistic Regression, Random Forest
- **CLTV Prediction** — regression models on historical spend patterns
- **Product Recommendations** — Collaborative Filtering, Cosine Similarity

---

## Demand Forecasting

Forecasts future sales demand, seasonal trends, and inventory requirements using:
- ARIMA
- Linear Regression
- Prophet

---

## Project Structure

```
QuantivaIQ/
│
├── datasets/                    # Historical retail and transaction datasets
├── sql/
│   ├── schema.sql               # Full DDL — all table definitions
│   ├── procedures.sql           # Stored procedures and triggers
│   └── analytics_queries.sql    # SQL behind each mv_* materialized views
├── python/
│   ├── db_setup.py              # Creates PostgreSQL schema and materialized views
│   ├── etl_pipeline.py          # Loads and transforms data; populates mv_* views
│   ├── fraud_detection.py       # ML-based fraud detection engine
│   ├── forecasting.py           # ARIMA / Prophet demand forecasting
│   ├── live_data_generator.py   # Continuous simulator — drives live DirectQuery data
│   └── web_dashboard.py         # Flask preview server on port 8000
├── notebooks/
│   └── analytics.ipynb          # Exploratory analysis and model prototyping
├── reports/                     # Generated reports and exports
├── docker-compose.yml           # Service definitions: postgres, web, simulator, setup
├── deploy.ps1                   # PowerShell one-click full-stack launch
├── run_demo.py                  # In-memory demo (no database required)
├── .env.example                 # Environment variable template
└── README.md
```

> **Note:** Power BI report/template files are not included in this repository. Build the report locally using Power BI Desktop and connect it to the PostgreSQL data warehouse using the steps above.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Power BI cannot connect to PostgreSQL | `DB_HOST` mismatch | Use `localhost` for same machine; use `<host-ip>` for remote. Check firewall allows port `5432`. |
| Dashboard shows stale data | Import mode selected instead of DirectQuery | Delete the dataset, reconnect using **DirectQuery**. |
| Page refresh not working | Feature not enabled on the page | Format pane → Page refresh → ON, set 5 s interval. |
| `mv_daily_revenue` is empty | ETL not run | Run: `python python/etl_pipeline.py` |
| Simulator not generating data | Process not started | Run: `python python/live_data_generator.py` |
| Flask dashboard at 8000 not loading | `web` service not started | Run: `docker compose up -d web` or `python python/web_dashboard.py` |
| Docker postgres not starting | Port 5432 already in use | Stop local PostgreSQL service or remap port in `docker-compose.yml`. |
| `mv_*` views all empty after setup | `--profile setup` step skipped | Re-run: `docker compose --profile setup run --rm setup` |

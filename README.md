# QuantivaIQ — AI-Powered Retail Intelligence & Fraud Analytics Platform

## Overview

QuantivaIQ is an enterprise-grade end-to-end Business Analytics and Fraud Intelligence platform designed for modern retail and e-commerce ecosystems.

The platform performs:
- real-time business analytics
- fraud detection
- customer intelligence
- demand forecasting
- KPI monitoring
- executive reporting

using advanced SQL, Python, Machine Learning, and Power BI.

The system simulates a real-world analytics architecture similar to platforms used by Amazon, Flipkart, and Myntra.

---

## Repository

**GitHub:** https://github.com/VEDANTMODI21/QuantivaIQ

---

## Quick Start

### Option A: Using Docker (Recommended)

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Ensure Docker daemon is running
3. Clone the repository:
   ```bash
   git clone https://github.com/VEDANTMODI21/QuantivaIQ.git
   cd QuantivaIQ
   ```
4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start PostgreSQL container:
   ```bash
   docker-compose up -d
   ```
6. Wait 10 seconds for PostgreSQL to be ready, then initialize the database:
   ```bash
   python python/db_setup.py
   ```
7. Seed initial data:
   ```bash
   python python/etl_pipeline.py
   ```
8. Start live data simulation:
   ```bash
   python python/live_data_generator.py
   ```

### Option B: Local PostgreSQL

1. Install [PostgreSQL 15+](https://www.postgresql.org/download/)
2. Create database and user:
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
4. Configure `.env` file (copy from `.env.example`)
5. Initialize database schema:
   ```bash
   python python/db_setup.py
   ```
6. Run ETL pipeline:
   ```bash
   python python/etl_pipeline.py
   ```
7. Start live simulation:
   ```bash
   python python/live_data_generator.py
   ```

### Option C: In-Memory Demo (No Database Required)

```bash
git clone https://github.com/VEDANTMODI21/QuantivaIQ.git
cd QuantivaIQ
pip install -r requirements.txt
python run_demo.py
```

This runs a complete analytics pipeline in-memory without needing PostgreSQL.

### Launch the Local Web Dashboard

Once PostgreSQL and ETL are initialized, start the live dashboard with:

```bash
python python/web_dashboard.py
```

Then open your browser to:

```text
http://localhost:8000
```

If you want to access it from another machine on the same network, use the host IP address instead of `localhost`:

```text
http://<your-machine-ip>:8000
```

The dashboard shows:
- total customers
- total orders
- total revenue
- fraud flags
- top products by revenue
- revenue by region
- customer segments

> Note: The current project includes a Flask-based browser dashboard for local preview. Power BI integration is supported separately by connecting Power BI Desktop to the backend PostgreSQL database.

### Power BI Live Integration

This repository now supports a full PostgreSQL-backed analytics stack with live Power BI connectivity.

1. Ensure Docker Desktop is installed and running.
2. Copy `.env.example` to `.env` and fill in your credentials.
3. Start the local stack with Docker Compose:
   ```powershell
   docker compose up -d postgres
   ```
4. Initialize the database and seed the warehouse:
   ```powershell
   docker compose --profile setup run --rm setup
   ```
5. Start the web dashboard and live simulator:
   ```powershell
   docker compose up -d web simulator
   ```
6. Open Power BI Desktop and connect to PostgreSQL at `localhost:5432` using **DirectQuery**.
7. Enable **Page refresh** in Power BI and use a 5-second interval to see live simulation updates.

Alternatively, run the helper script from the repository root:

```powershell
./deploy.ps1
```

### What is now integrated

- PostgreSQL data warehouse running in Docker
- Python ETL pipeline loading analytics tables
- Live data simulator updating the database continuously
- Power BI-ready materialized views refreshed automatically
- Flask dashboard available at `http://localhost:8000`

For detailed Power BI connection instructions and DAX formulas, see:
- `dashboards/powerbi_connection_guide.md`
- `dashboards/dax_measures.md`

---

# Tech Stack

| Layer | Technology |
|---|---|
| Database | PostgreSQL |
| Backend Analytics | Python |
| Data Processing | pandas, numpy |
| Machine Learning | scikit-learn |
| Dashboarding | Power BI |
| Database ORM | SQLAlchemy |
| Real-Time Simulation | faker, random, schedule |
| IDE | VS Code |
| Notebook Environment | Jupyter Notebook |
| Version Control | Git & GitHub |

---

# System Architecture

Historical Datasets / Simulated Live Data
                ↓
        Python ETL Pipelines
                ↓
      PostgreSQL Data Warehouse
                ↓
      Advanced SQL Analytics Layer
                ↓
     Machine Learning Intelligence
                ↓
    Power BI Real-Time Dashboards
                ↓
      Business Insights & Alerts

---

# Core Features

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

# Enterprise Data Warehouse

## Database Domains

### Customer Domain
- customers
- customer_sessions
- customer_segments

### Product Domain
- products
- categories
- suppliers
- inventory

### Sales Domain
- orders
- order_items
- payments
- refunds

### Fraud Domain
- fraud_logs
- suspicious_transactions

### Feedback Domain
- reviews
- ratings

---

# Advanced SQL Analytics

## SQL Concepts Used

- Complex JOINs
- CTEs
- Window Functions
- Views
- Materialized Views
- Stored Procedures
- Triggers
- Transactions
- Indexing
- Query Optimization

---

# Business KPI Analytics

## Revenue Metrics
- Monthly Revenue Growth
- Regional Revenue Trends
- Product Category Performance
- Profitability Analysis

## Customer Metrics
- Customer Retention Rate
- Customer Churn Rate
- Repeat Purchase Rate
- Customer Lifetime Value (CLTV)

## Inventory Metrics
- Inventory Turnover
- Low Stock Detection
- Overstock Monitoring

## Fraud Metrics
- Fraud Transaction Ratio
- Suspicious Refund Detection
- High-Risk Customer Monitoring

---

# ETL Pipeline

## Extract
- Retail datasets
- Transaction datasets
- Simulated live data streams

## Transform
- Missing value handling
- Duplicate removal
- Data normalization
- Outlier detection
- Feature engineering

## Load
- Automated loading into PostgreSQL warehouse

---

# Real-Time Data Simulation

A Python-based simulation engine continuously generates:
- customer activity
- orders
- payments
- refunds
- inventory updates

This creates a near real-time analytics environment.

---

# Fraud Detection Engine

## Fraud Scenarios
- abnormal transaction frequency
- excessive refund requests
- suspicious payment patterns
- bot-generated transactions

---

## ML Algorithms Used
- Isolation Forest
- Z-Score Anomaly Detection
- Clustering-Based Detection

---

# Customer Intelligence System

## RFM Segmentation
Customers classified into:
- VIP Customers
- Loyal Customers
- At-Risk Customers
- Inactive Customers

---

## Predictive Analytics
- Customer Churn Prediction
- Customer Lifetime Value Prediction

Algorithms:
- Logistic Regression
- Random Forest

---

# Recommendation Engine

Product recommendation system using:
- Collaborative Filtering
- Cosine Similarity

Example:
"Customers who bought X also bought Y"

---

# Demand Forecasting

Forecasts:
- future sales demand
- seasonal trends
- inventory requirements

Models:
- ARIMA
- Linear Regression
- Prophet

---

# Power BI Real-Time Dashboard

## Dashboard Modules

### Executive Dashboard
- Revenue KPIs
- Profit Analysis
- Growth Trends

### Customer Dashboard
- Customer Segmentation
- Churn Analytics
- CLTV Insights

### Fraud Dashboard
- Suspicious Transactions
- Fraud Heatmaps
- Refund Abuse Monitoring

### Inventory Dashboard
- Stock Monitoring
- Inventory Trends
- Low Stock Alerts

---

# Dashboard Features

- DirectQuery Integration
- Auto Refresh
- DAX Measures
- Interactive Filters
- Drill-Through Reports
- KPI Cards
- Forecast Visualizations
- Geographic Analysis

---

# Real-Time Integration

Python continuously inserts live transactional data into PostgreSQL.

Power BI connects using:
- DirectQuery
- Auto Refresh

This enables near real-time dashboard monitoring.

---

# Dataset Sources

## Historical Datasets
- E-commerce transaction datasets
- Retail sales datasets
- Customer behavior datasets

Sources:
- Kaggle
- UCI Repository

---

# Project Structure

project/
│
├── datasets/
├── sql/
│   ├── schema.sql
│   ├── procedures.sql
│   ├── analytics_queries.sql
│
├── python/
│   ├── etl_pipeline.py
│   ├── fraud_detection.py
│   ├── forecasting.py
│   ├── live_data_generator.py
│
├── dashboards/
│   ├── quantivaiq_dashboard.pbix
│
├── notebooks/
│   ├── analytics.ipynb
│
├── reports/
│
└── README.md

---

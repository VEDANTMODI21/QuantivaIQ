# QuantivaIQ — AI-Powered Retail Intelligence & Fraud Analytics Platform

QuantivaIQ is an enterprise-grade end-to-end Business Analytics and Fraud Intelligence platform designed for modern retail and e-commerce ecosystems.

## Features

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

## Tech Stack

- **Database:** PostgreSQL
- **Backend Analytics:** Python (pandas, numpy, scikit-learn)
- **Dashboarding:** Power BI
- **Database ORM:** SQLAlchemy

## Project Structure

```
QuantivaIQ/
├── datasets/              # CSV exports & seed data
├── sql/                   # PostgreSQL schema, procedures, queries
├── python/                # ETL, Machine Learning, Simulation
├── dashboards/            # Power BI connection guides & DAX
├── notebooks/             # Interactive Jupyter notebooks
├── reports/               # Generated reports and forecasts
├── .env.example           # Environment template
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Setup Instructions

1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and configure your PostgreSQL database connection.
3. Run `python/etl_pipeline.py` to seed initial data.
4. Run `python/live_data_generator.py` for real-time simulation.

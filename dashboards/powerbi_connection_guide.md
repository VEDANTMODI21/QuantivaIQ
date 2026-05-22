# QuantivaIQ — Power BI Connection Guide

This guide explains how to connect your local Power BI Desktop instance to the QuantivaIQ PostgreSQL Data Warehouse using DirectQuery for real-time analytics.

## Prerequisites
1. **Power BI Desktop** installed on your machine.
2. **PostgreSQL ODBC Driver (psqlODBC)** or the native Npgsql connector installed on your system.
3. The PostgreSQL database (`quantivaiq`) must be running.

## Step 1: Connect to PostgreSQL
1. Open Power BI Desktop.
2. Click **Get Data** -> **More...**
3. Search for **PostgreSQL database** and select it, then click **Connect**.
4. Enter the Server and Database details:
   - **Server**: `localhost` (or your DB_HOST)
   - **Database**: `quantivaiq`
5. **Data Connectivity mode**: Select **DirectQuery**! (This is critical for the real-time simulation to work).
6. Click **OK**.
7. Enter your credentials (User: `postgres`, Password: `your_password`).

## Step 2: Import Tables and Views
Do NOT import the raw transactional tables (`orders`, `order_items`) if you only need high-level KPIs. Import the Materialized Views and highly indexed tables instead to ensure fast dashboard performance.

Recommended Tables/Views to load:
- `mv_daily_revenue`
- `mv_customer_kpis`
- `mv_product_performance`
- `mv_fraud_summary`
- `mv_inventory_status`
- `customer_segments`
- `fraud_logs`

## Step 3: Establish Relationships (Data Model)
In the Power BI Model View, create the following relationships:
- `fraud_logs[customer_id]` -> `customer_segments[customer_id]` (1 to 1)
- Map your date dimensions if using a separate Date table.

## Step 4: Configure Auto-Refresh
To see the `live_data_generator.py` in action:
1. In Power BI Desktop, click on the **Page background** to clear selection.
2. Go to the **Format** pane -> **Page refresh**.
3. Turn it **On**.
4. Set the refresh interval to **5 seconds** (or matching your `SIMULATION_INTERVAL`).

## Step 5: Dashboard Blueprints
You should build 4 separate tabs:

### 1. Executive Dashboard
- **Cards**: Total Revenue, MoM Growth, Total Active Customers.
- **Line Chart**: Daily Revenue over time (from `mv_daily_revenue`).
- **Bar Chart**: Top Categories by Revenue (from `mv_product_performance`).

### 2. Customer Dashboard
- **Donut Chart**: RFM Segment Distribution (from `customer_segments`).
- **Scatter Plot**: Recency vs Monetary Value.
- **Cards**: Average Customer Lifetime Value.

### 3. Fraud & Security Dashboard
- **Cards**: Fraud Rate %, Total Suspicious Value.
- **Tree Map**: Fraud Incidents by Type.
- **Table**: Recent Fraud Logs with Risk Score conditional formatting (Red > 80).

### 4. Inventory Health
- **Cards**: Items Out of Stock, Average Inventory Turnover.
- **Bar Chart**: Quantity on Hand vs Reorder Level by Product.

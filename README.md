## Sales Data Pipeline & Live Monitoring Dashboard

End-to-End Data Engineering Capstone · BZAN 545 – Data Engineering · University of Tennessee, Knoxville

## Business Objective

Static datasets quickly become obsolete, leading to stale insights and poor decision-making. The objective was to design and deploy an automated system that eliminates manual data handling, ensures historical integrity, and provides decision-makers with always-current, observable analytics - separating the data engineering, data access, and data consumption layers the way production systems do.

## System Architecture (End-to-End)

| Layer | Component | Purpose |
|---|---|---|
| Ingestion | External API + Python | Daily automated data pull, no manual intervention |
| Staging | Local pickle files | Raw file validation and date-stamped storage |
| Storage | PostgreSQL | Historical records, analytics queries, idempotent inserts |
| Access | Flask API | Programmatic downstream data serving |
| Consumption | Dash Dashboard | Live KPI monitoring, filtering, and pipeline health |

The pipeline runs on a fully automated OS-level schedule. Config-driven ingestion scripts manage credentials and environment settings securely, and idempotent database inserts prevent duplicates while preserving historical integrity.

## Key Engineering Contributions

- Owned and managed the GitHub repository, reviewing pull requests and maintaining a stable main branch
- Built config-driven ingestion scripts (config.py) to securely manage credentials and environment variables via .env
- Automated daily data pulls using Python and OS-level task scheduling - zero manual intervention required
- Implemented idempotent database inserts to prevent duplicates and preserve full historical integrity
- Developed a Flask API to serve cleaned, validated data downstream
- Designed and deployed a live Dash dashboard with KPI cards, interactive filters, real-time visualizations, and pipeline status monitoring

## Dashboard Capabilities

Executive view - designed to remain interpretable for non-technical stakeholders:

## KPI Cards
- Total items sold
- Average discount
- Free shipping rate

## Interactive Filters
- Region
- Product ID

## Visualizations
- Daily items sold over time (time-series line chart)
- Sales by region (categorical bar chart)
- Product ID vs. items sold (product-level bar chart)
  
## Pipeline Health
- Last data load timestamp
- Automatic Pipeline Fresh / Pipeline Stale status based on data recency

## Technical Implementation Notes

config.py - Centralized configuration layer; loads credentials from environment variables, defines data directory structure, and sets date-stamped file naming conventions (raw_data_MM-DD-YYYY.pkl)

fetch_data_sub.py - Retrieves the external dataset, validates the resulting DataFrame, and saves it as a timestamped pickle file to the local staging directory

data_insert_sub.py - Identifies the most recent staged pickle file, loads it into a DataFrame, and inserts records into the PostgreSQL data_daily table using SQLAlchemy with schema type enforcement

FINAL_flask_app.py - Loads data directly from PostgreSQL, calculates KPIs, applies user-selected filters, and renders all three interactive visualizations via Dash callbacks

## Tech Stack

Python · PostgreSQL · Flask · Dash · Plotly · SQLAlchemy · psycopg2 · SQL · Git / GitHub · Task Scheduler · Pickle · dotenv · Spark

## My Role

Repo Owner · Data Engineer · Pipeline Architect · Dashboard Developer

I designed the full system architecture, implemented the automated ingestion and database pipeline, built the API layer, and developed the live dashboard end-to-end. I was responsible for code quality, reproducibility, and system reliability, and for translating engineering decisions into a clear technical and executive narrative during the final presentation.


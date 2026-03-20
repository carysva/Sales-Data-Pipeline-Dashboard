# Sales Data Pipeline & Live Monitoring Dashboard

An end-to-end data engineering capstone that delivers fresh analytics via an automated ingestion pipeline, a production-ready database, an API layer, and a live KPI dashboard.

## Business Objective
Static datasets quickly become obsolete. The project objective was to design and deploy a fully automated system that:
- Continuously ingests external data
- Stores it in a production-ready database
- Serves it via an API
- Visualizes both business performance and pipeline health in real time

## System Architecture (End-to-End)
- Daily automated ingestion from a remote external source
- Local staging and validation of raw data files
- PostgreSQL database for historical storage and analytics queries
- Flask API to expose cleaned data programmatically
- Dash dashboard for live KPI monitoring, filtering, and data quality checks
- Pipeline freshness indicator (fresh vs. stale data)

## Dashboard Highlights
Executive view designed for non-technical stakeholders:
- KPI cards (example KPIs referenced in the project narrative):
  - Total items sold
  - Average discount
  - Free shipping rate
- Interactive filters:
  - Region
  - Product
- Visualizations:
  - Time-series performance
  - Categorical breakdowns
- Pipeline health visibility:
  - Data recency and freshness status

## Tech Stack
Python, PostgreSQL, Flask, Dash, SQL, Git/GitHub, VS Code, task scheduling, APIs, and Spark (as referenced in the narrative).

## Portfolio Artifacts (recommended to include)
- `Untitled document (3).docx` (portfolio summary narrative)

## Next Step (so this repo can be fully public)
To complete the public repo package, I need the corresponding GitHub repository URL that contains the pipeline code, runbooks, and/or presentation slides.


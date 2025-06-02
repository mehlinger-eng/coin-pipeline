# Coin Pipeline

A modular, cloud-native pipeline for collecting, streaming, and analyzing cryptocurrency price data using FastAPI, Google Pub/Sub, and BigQuery.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Extending the Pipeline](#extending-the-pipeline)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

This project provides a robust, extensible pipeline for ingesting real-time cryptocurrency price data, streaming it through Google Pub/Sub, and persisting it in BigQuery for analytics and reporting. The system is designed for modularity, scalability, and cloud deployment.

---

## Architecture

```
[CoinGecko API] 
      |
      v
[Collector Service (FastAPI)]
      |
      v
[Google Pub/Sub Topic]
      |
      v
[Subscriber Service] ---> [BigQuery Table]
```

- **Collector Service**: Periodically fetches crypto prices and publishes them to Pub/Sub.
- **Pub/Sub**: Decouples ingestion from processing.
- **Subscriber Service**: Consumes messages and writes validated data to BigQuery.
- **BigQuery**: Stores and enables analytics on historical price data.

---

## Features

- Modular Python services (Collector, Subscriber)
- FastAPI for health checks and extensibility
- Google Pub/Sub integration for scalable streaming
- BigQuery integration for analytics-ready storage
- Configurable via `config.json`
- Utility scripts for setup (e.g., BigQuery table creation)
- Ready for cloud deployment and CI/CD

---

## Project Structure

```
coin-pipeline/
├── config.json                # Main configuration file
├── setup.py                   # Project install script
├── README.md                  # This file
├── services/
│   ├── collector/             # Collector service (FastAPI, scheduler)
│   └── pubsub_subscriber/     # Pub/Sub subscriber (BigQuery writer)
├── scripts/                   # Utility scripts (e.g., BQ table creation)
├── infra/                     # Infrastructure as code (WIP)
├── dbt/                       # (Optional) Analytics models (WIP)
└── venv/                      # Python virtual environment
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- Google Cloud account with Pub/Sub and BigQuery enabled
- Service account with appropriate permissions
- (Optional) Docker

### Installation

1. **Clone the repo:**
   ```bash
   git clone <repo-url>
   cd coin-pipeline
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e .
   ```

4. **Configure Google credentials:**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account.json
   ```

---

## Configuration

Edit `config.json` to match your GCP project, Pub/Sub, and BigQuery setup:

```json
{
  "gcp": {
    "project_id": "your-gcp-project"
  },
  "pubsub": {
    "subscription_id": "your-subscription"
  },
  "bigquery": {
    "dataset": "your_dataset",
    "table": "your_table"
  }
}
```

---

## Usage

### 1. Create the BigQuery Table

```bash
python scripts/create_bq_table.py
```

### 2. Start the Collector Service

From the project root:
```bash
uvicorn services.collector.app:app --reload
```
- This will start the FastAPI app and the price scheduler.

### 3. Start the Pub/Sub Subscriber

From the project root:
```bash
python services/pubsub_subscriber/subscriber.py
```
- This will listen to Pub/Sub and write to BigQuery.

### 4. Health Check

Visit [http://localhost:8000/health](http://localhost:8000/health) to verify the collector is running.

---

## Development

- All services are installable as a package (`pip install -e .`).
- Add new dependencies to `setup.py`.
- Use `__init__.py` in all packages for importability.
- Tests can be added under `services/collector/tests/` and similar.

---

## Extending the Pipeline

- **Add new coins**: Edit the `COINS` list in `services/collector/scheduler.py`.
- **Add new data sources**: Extend the collector or add new services.
- **Analytics**: Add dbt models in the `dbt/` directory.
- **Infrastructure**: Add Terraform or other scripts in `infra/`.

---

## Troubleshooting

- **ModuleNotFoundError: No module named 'services'**  
  - Ensure you are running commands from the project root.
  - Ensure you have run `pip install -e .`.
  - Ensure all directories have `__init__.py`.

- **BigQuery errors**  
  - Ensure the table exists (`python scripts/create_bq_table.py`).
  - Check your service account permissions.

- **Pub/Sub errors**  
  - Ensure the topic and subscription exist in GCP.

---

## Roadmap

- [ ] Add CI/CD pipeline
- [ ] Add monitoring and alerting
- [ ] Complete infrastructure as code
- [ ] Add more data sources and analytics

---

## License

MIT License

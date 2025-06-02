import json
from google.cloud import bigquery

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

PROJECT_ID = config["gcp"]["project_id"]
DATASET = config["bigquery"]["dataset"]
TABLE = config["bigquery"]["table"]

# Initialize BigQuery client
client = bigquery.Client(project=PROJECT_ID)

# Read SQL from file
with open("scripts/create_bq_table.sql", "r") as f:
    sql = f.read()

# Execute the query
query_job = client.query(sql)
query_job.result()  # Wait for the query to complete

print(f"✅ Table {PROJECT_ID}.{DATASET}.{TABLE} created successfully!") 
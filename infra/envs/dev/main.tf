terraform {
    required_version = ">= 1.7"
    backend "gcs" {
        bucket = "tfstate-coin-pipeline-dev"
        prefix = "dev"
    }
}

provider "google" {
    project = var.project_id
    region  = var.region
}

locals {
  services = [
    "artifactregistry.googleapis.com",
    "bigquery.googleapis.com",
    "cloudbuild.googleapis.com",
    "cloudfunctions.googleapis.com",
    "compute.googleapis.com",
    "container.googleapis.com",
    "dataproc.googleapis.com",
    "pubsub.googleapis.com",
    "run.googleapis.com",
    "serviceusage.googleapis.com",
    "storage.googleapis.com",
  ]
}

resource "google_project_service" "required" {
  for_each           = toset(local.services)
  service            = each.value
  disable_on_destroy = false
}

resource "google_service_account" "terraform" {
  account_id   = "terraform"
  display_name = "Terraform deploy SA"
}

resource "google_project_iam_member" "terraform_owner" {
  project = var.project_id
  role    = "roles/owner"
  member  = "serviceAccount:${google_service_account.terraform.email}"
}

resource "google_storage_bucket" "raw_parquet" {
  name          = "coin-raw-parquet-dev"
  location      = var.region
  force_destroy = true
}


resource "google_storage_bucket" "spark_checkpoints" {
  name          = "coin-spark-checkpoints-dev"
  location      = var.region
  storage_class = "NEARLINE"
  force_destroy = true
}

output "terraform_sa_email" {
  value = google_service_account.terraform.email
}

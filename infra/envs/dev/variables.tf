terraform {
  required_version = ">= 0.12"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 3.5"
    }
  }
}

variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "us-central1"
}

provider "google" {
  project = var.project_id
  region  = var.region
}
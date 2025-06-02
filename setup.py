from setuptools import setup, find_packages

setup(
    name="coin-pipeline",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic",
        "google-cloud-pubsub",
        "google-cloud-bigquery",
    ],
) 
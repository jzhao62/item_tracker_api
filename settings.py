# settings.py
import os

INGESTION_KEY = os.environ.get("INGESTION_KEY")
TABLE_NAME = os.environ.get("TABLE_NAME")
REGION = os.environ.get("REGION")
#!/usr/bin/env python3
import time
import json
import logging
import os
import sys

import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone  # Add timezone import

from garth.exc import GarthHTTPError
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError
)

# Configure debug logging
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()  # Automatically loads .env from the current directory

# Load environment variables if defined
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
tokenstore = os.getenv("TOKENSTORE")
auth_token = os.getenv("AUTH_TOKEN")  # Move Authorization token to .env
api = None

# Example selections and settings
today = datetime.now()
startdate = today - timedelta(days=7) # Select past week

def init_api(email, password):
    """Initialize Garmin API with your credentials."""

    # Login to Garmin Connect portal with credentials since session is invalid or not present.
    #api = Garmin(email, password)
    try:  
        api = Garmin()
        api.login(tokenstore)
    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
        garmin = Garmin(email,password)
        garmin.login()
        garmin.garth.dump(tokenstore)

    return api

# Init API
if not api:
    api = init_api(email, password)

# If the API requires authentication, add your token or credentials
headers = {
    'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json'
}

url = 'https://api.libra-app.eu/values/weight/%s'

def fetch_latest_date():
    """Fetch the latest date from the API."""
    try:
        response = requests.get(url % 'latest', headers=headers)
        response.raise_for_status()
        return datetime.strptime(response.json()['date'], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc) - timedelta(days=1)
    except requests.RequestException as e:
        logger.error(f"Error fetching latest date: {e}")
        sys.exit(1)

def upload_weight_data(weight_data):
    """Upload weight data to the API."""
    for i in weight_data['dateWeightList']:
        d = datetime.fromtimestamp(i['date'] / 1000, tz=timezone.utc).isoformat()  # Ensure UTC timezone
        data = {
            'weight': i['weight'] / 1000,
            'body_fat': (i['bodyFat'] / 100) * (i['weight'] / 1000),
            'muscle_mass': i['muscleMass'] / 1000,
            'log': ''
        }
        logger.info(f"Date: {d}")
        logger.info(f"Data: {data}")
        try:
            response = requests.put(url % d, data=json.dumps(data), headers=headers)
            response.raise_for_status()
            logger.info(f"Response status code: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Error uploading data for {d}: {e}")
        time.sleep(1)

def main():
    """Main function to execute the script logic."""
    last_date = fetch_latest_date()
    logger.info(f"Last date: {last_date}")

    weight = api.get_body_composition(last_date.isoformat(), today.isoformat())
    upload_weight_data(weight)

if __name__ == "__main__":
    main()

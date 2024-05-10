# Imports
import requests
import json
import os
import argparse
import sys

from azure.storage.blob import BlobServiceClient

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'libs'))
import credentials as c

# Function Definitions
def define_storage_mode(argparser):
    args = argparser.parse_args()

    if args.storage.lower() not in ["local", "azure"]:
        print("Invalid --storage (-s) option. Provide 'local' or 'azure'")
        sys.exit(1)

    if args.storage.lower() == "local":
        return True
    else:
        return False

def ingest_season_playoffs(season_id):
    # Individual playoffs endpoint: https://api-web.nhle.com/v1/playoff-series/carousel/20222023
    r = requests.get(f"{base_url}playoff-series/carousel/{season_id}")
    data = r.json()
    if save_locally:
        filename = os.path.join(os.path.dirname(__file__), "data", "playoffs", f"{str(season_id)}.json")
        with open(filename, "w") as f:
            json.dump(data, f)
    else:
        blob_name = f"{AZURE_CONTAINER}{str(season_id)}.json"
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(data=json.dumps(data), overwrite=True)

# Script gives you the option to save files locally or on Azure
# If an invalid option is provided, quit
parser = argparse.ArgumentParser()
parser.add_argument("--storage", "-s", default="local")
save_locally = define_storage_mode(parser)

if save_locally == False:
    # Configure Azure Blob Storage Credentials
    AZURE_CONTAINER = "raw/nhl/playoffs/"
    account_url = c.get_storage_account_url()
    default_credential = c.get_storage_account_credential()
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    container_name = "sports-bot"

# First step, get the end date for each season (it'll be used as a criteria to call standings for each season)
base_url = "https://api-web.nhle.com/v1/"
all_seasons_endpoint =  "season"
r = requests.get(f"{base_url}{all_seasons_endpoint}")
season_list = r.json()

# Then get full season standings and save them as {season_id}.json
# Either locally or in blob storage
for season in season_list:
    ingest_season_playoffs(season)

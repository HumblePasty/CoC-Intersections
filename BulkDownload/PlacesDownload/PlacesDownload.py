"""
Author: Haolin Li
Last Updated: 12/21/2023

This script is for downloading the Census Place Shapefiles from the TIGER/Line database.
The shapefiles are downloaded and extracted into the Data directory.

Target Directory Structure (Data):
Data
├── 2007
│   ├── 01_ALABAMA
│   │   └── place shapefile
│   ├── 02_ALASKA
│   │   └── place shapefile
│   ├── 04_ARIZONA
│   │   └── ...
│   ├── ...
│   ...
├── 2008

"""

import os
import requests
import zipfile
from io import BytesIO

# Define the base URL for the Census shapefiles.
base_url = "https://www2.census.gov/geo/tiger/"

# Define the ANSI codes and names for all states and territories.
states_and_territories = {
    "01": "ALABAMA",
    "02": "ALASKA",
    "04": "ARIZONA",
    "05": "ARKANSAS",
    "06": "CALIFORNIA",
    "08": "COLORADO",
    "09": "CONNECTICUT",
    "10": "DELAWARE",
    "11": "DISTRICT_OF_COLUMBIA",
    "12": "FLORIDA",
    "13": "GEORGIA",
    "15": "HAWAII",
    "16": "IDAHO",
    "17": "ILLINOIS",
    "18": "INDIANA",
    "19": "IOWA",
    "20": "KANSAS",
    "21": "KENTUCKY",
    "22": "LOUISIANA",
    "23": "MAINE",
    "24": "MARYLAND",
    "25": "MASSACHUSETTS",
    "26": "MICHIGAN",
    "27": "MINNESOTA",
    "28": "MISSISSIPPI",
    "29": "MISSOURI",
    "30": "MONTANA",
    "31": "NEBRASKA",
    "32": "NEVADA",
    "33": "NEW_HAMPSHIRE",
    "34": "NEW_JERSEY",
    "35": "NEW_MEXICO",
    "36": "NEW_YORK",
    "37": "NORTH_CAROLINA",
    "38": "NORTH_DAKOTA",
    "39": "OHIO",
    "40": "OKLAHOMA",
    "41": "OREGON",
    "42": "PENNSYLVANIA",
    "44": "RHODE_ISLAND",
    "45": "SOUTH_CAROLINA",
    "46": "SOUTH_DAKOTA",
    "47": "TENNESSEE",
    "48": "TEXAS",
    "49": "UTAH",
    "50": "VERMONT",
    "51": "VIRGINIA",
    "53": "WASHINGTON",
    "54": "WEST_VIRGINIA",
    "55": "WISCONSIN",
    "56": "WYOMING",
    "60": "AMERICAN_SAMOA",
    "66": "GUAM",
    "69": "COMMONWEALTH_OF_THE_NORTHERN_MARIANA_ISLANDS",
    "72": "PUERTO_RICO",
    "78": "VIRGIN_ISLANDS_OF_THE_UNITED_STATES"
}

def download_and_extract(year, code, name):
    # Create the correct URL based on the year.
    if year == 2007:
        url = f"{base_url}TIGER{year}FE/{code}_{name}/fe_{year}_{code}_place.zip"
    elif year == 2010:
        url = f"{base_url}TIGER{year}/PLACE/2010/tl_{year}_{code}_place10.zip"
    elif year >= 2011:
        url = f"{base_url}TIGER{year}/PLACE/tl_{year}_{code}_place.zip"
    else:  # For 2008 and 2009
        url = f"{base_url}TIGER{year}/{code}_{name}/tl_{year}_{code}_place.zip"

    # Define the directory path based on the year, code, and name.
    dir_path = f"Data/{year}/{code}_{name}"

    # Create the directory if it does not exist.
    os.makedirs(dir_path, exist_ok=True)

    # Download the zip file.
    response = requests.get(url)
    if response.status_code == 200:
        zip_file = zipfile.ZipFile(BytesIO(response.content))

        # Extract the shapefile into the specified directory.
        zip_file.extractall(path=dir_path)
        print(f"Successfully downloaded and extracted files for {name}, {year}")
    else:
        print(f"Failed to download data for {code} - {name}, {year}. HTTP status code: {response.status_code}")

# Loop through each year and state/territory to download and extract the shapefiles.
for year in range(2007, 2024):
    for code, name in states_and_territories.items():
        download_and_extract(year, code, name)

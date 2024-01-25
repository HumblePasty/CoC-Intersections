import os
import requests
import zipfile
from io import BytesIO

# Define the base URL for the Census shapefiles.
base_url = "https://www2.census.gov/geo/tiger/"

# Define the ANSI codes and names for the specified states requiring county subdivision data.
specified_states = {
    "09": "CONNECTICUT",
    "17": "ILLINOIS",
    "18": "INDIANA",
    "20": "KANSAS",
    "25": "MASSACHUSETTS",
    "23": "MAINE",
    "26": "MICHIGAN",
    "27": "MINNESOTA",
    "29": "MISSOURI",
    "38": "NORTH_DAKOTA",
    "33": "NEW_HAMPSHIRE",
    "34": "NEW_JERSEY",
    "36": "NEW_YORK",
    "39": "OHIO",
    "42": "PENNSYLVANIA",
    "44": "RHODE_ISLAND",
    "45": "SOUTH_CAROLINA",
    "50": "VERMONT",
    "55": "WISCONSIN"
}

def download_and_extract_cousub(year, code, name):
    # Modify the URL and directory structure based on the year.
    if year >= 2011:
        url = f"{base_url}TIGER{year}/COUSUB/tl_{year}_{code}_cousub.zip"
        dir_path = f"Data/{year}/{code}_{name}"
    elif year == 2010:
        url = f"{base_url}TIGER{year}/COUSUB/2010/tl_{year}_{code}_cousub10.zip"
        dir_path = f"Data/{year}/{code}_{name}"
    elif year == 2007:
        # 2007 data is within each county directory, so this requires a different approach to fetch all counties.
        pass  # Placeholder for now, as it requires fetching county-specific data.
    else:  # For 2008 and 2009
        url = f"{base_url}TIGER{year}/{code}_{name}/tl_{year}_{code}_cousub.zip"
        dir_path = f"Data/{year}/{code}_{name}"

    # Create the directory if it does not exist.
    os.makedirs(dir_path, exist_ok=True)

    # Download the zip file.
    response = requests.get(url)
    if response.status_code == 200:
        zip_file = zipfile.ZipFile(BytesIO(response.content))

        # Extract the shapefile into the specified directory.
        zip_file.extractall(path=dir_path)
        print(f"Successfully downloaded and extracted cousub files for {name}, {year}")
    else:
        print(f"Failed to download cousub data for {name}, {year}. HTTP status code: {response.status_code}")

# Modify the loop to download and extract the county subdivision shapefiles.
for year in range(2007, 2024):
    if year != 2007:
        # For 2008 onwards, download files for specified states.
        for code, name in specified_states.items():
            download_and_extract_cousub(year, code, name)
    else:
        # TODO: Implement the logic for 2007 data, which requires county-specific URLs.
        pass  # Placeholder for 2007 logic.

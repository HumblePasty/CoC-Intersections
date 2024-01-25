"""
Author: Haolin Li
Last Updated: 12/10/2023

This script downloads the Continuum of Care (CoC) shapefiles from the
HUD Exchange website. The script downloads the shapefiles for all
states for a given year. The script creates a directory structure
that is organized by year and state. The script will not download
shapefiles for a state if the shapefiles already exist in the
target directory.

target directory structure:
    Data
    ├── 2007
    │   ├── Alabama
    │   │   ├── CoC_GIS_2007.shp
    │   │   ├── CoC_GIS_2007.shx
    │   │   ├── ...
    │   ├── Alaska
    │   │   ├── ...
    │   ├── ...
    ├── 2008
    │   ├── ...
    ├── ...
"""

import os
import requests
import zipfile
from io import BytesIO

# states and their abbreviations
states = {
    # 50 states
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota",
    "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island",
    "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin",
    "WY": "Wyoming",
    # and 4 territories
    "DC": "District of Columbia",
    "GU": "Guam",
    "PR": "Puerto Rico",
    "VI": "Virgin Islands of the United States"
}

base_url = "https://files.hudexchange.info/reports/published"
target_directory = "Data"


def download_and_extract_coc_shapefiles(year, states, base_url, target_directory):
    for state_abbr, state_name in states.items():
        url = f"{base_url}/CoC_GIS_State_Shapefile_{state_abbr}_{year}.zip"
        response = requests.get(url)

        if response.status_code == 200:
            # make sure the target directory exists
            state_directory = os.path.join(target_directory, str(year), state_name)
            os.makedirs(state_directory, exist_ok=True)

            # process the zip file
            with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
                for member in zip_ref.infolist():
                    # add the year and state name to the path
                    path_parts = member.filename.split('/')[1:]
                    extracted_path = os.path.join(state_directory, *path_parts)

                    if member.is_dir():
                        os.makedirs(extracted_path, exist_ok=True)
                    else:
                        with open(extracted_path, 'wb') as file:
                            file.write(zip_ref.read(member.filename))

            print(f"Downloaded and extracted {state_name} data for {year}")
        else:
            print(f"Failed to download data for {state_name} in {year}")


# download the shapefiles for 2010
# download_and_extract_coc_shapefiles(2010, states, base_url, target_directory)
#
# # and other years
for year in range(2007, 2024):
    download_and_extract_coc_shapefiles(year, states, base_url, target_directory)

# download_and_extract_coc_shapefiles(2009, states, base_url, target_directory)

import os
import requests
import zipfile
from io import BytesIO
import csv

state_names = {
    "AL": "01_ALABAMA",
    "AK": "02_ALASKA",
    "AZ": "04_ARIZONA",
    "AR": "05_ARKANSAS",
    "CA": "06_CALIFORNIA",
    "CO": "08_COLORADO",
    "CT": "09_CONNECTICUT",
    "DE": "10_DELAWARE",
    "DC": "11_DISTRICT_OF_COLUMBIA",
    "FL": "12_FLORIDA",
    "GA": "13_GEORGIA",
    "HI": "15_HAWAII",
    "ID": "16_IDAHO",
    "IL": "17_ILLINOIS",
    "IN": "18_INDIANA",
    "IA": "19_IOWA",
    "KS": "20_KANSAS",
    "KY": "21_KENTUCKY",
    "LA": "22_LOUISIANA",
    "ME": "23_MAINE",
    "MD": "24_MARYLAND",
    "MA": "25_MASSACHUSETTS",
    "MI": "26_MICHIGAN",
    "MN": "27_MINNESOTA",
    "MS": "28_MISSISSIPPI",
    "MO": "29_MISSOURI",
    "MT": "30_MONTANA",
    "NE": "31_NEBRASKA",
    "NV": "32_NEVADA",
    "NH": "33_NEW HAMPSHIRE",
    "NJ": "34_NEW JERSEY",
    "NM": "35_NEW MEXICO",
    "NY": "36_NEW YORK",
    "NC": "37_NORTH CAROLINA",
    "ND": "38_NORTH DAKOTA",
    "OH": "39_OHIO",
    "OK": "40_OKLAHOMA",
    "OR": "41_OREGON",
    "PA": "42_PENNSYLVANIA",
    "RI": "44_RHODE ISLAND",
    "SC": "45_SOUTH CAROLINA",
    "SD": "46_SOUTH DAKOTA",
    "TN": "47_TENNESSEE",
    "TX": "48_TEXAS",
    "UT": "49_UTAH",
    "VT": "50_VERMONT",
    "VA": "51_VIRGINIA",
    "WA": "53_WASHINGTON",
    "WV": "54_WEST VIRGINIA",
    "WI": "55_WISCONSIN",
    "WY": "56_WYOMING"
}

states_to_download = {
    "09_CONNECTICUT",
    "17_ILLINOIS",
    "18_INDIANA",
    "20_KANSAS",
    "25_MASSACHUSETTS",
    "23_MAINE",
    "26_MICHIGAN",
    "27_MINNESOTA",
    "29_MISSOURI",
    "38_NORTH DAKOTA",
    "33_NEW HAMPSHIRE",
    "34_NEW JERSEY",
    "36_NEW YORK",
    "39_OHIO",
    "42_PENNSYLVANIA",
    "44_RHODE ISLAND",
    "45_SOUTH CAROLINA",
    "50_VERMONT",
    "55_WISCONSIN"
}

def read_csv_to_dict(csv_path):
    counties_by_state = {}
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            state = state_names[row['state']]  # Adjust this if your column name for states is different
            fips = row['fips']  # Adjust this if your column name for FIPS codes is different
            name = row['name'].replace("County", "").replace(".","").strip().replace(" ", "_")  # Adjust this if your column name for county names is different

            if state not in counties_by_state:
                counties_by_state[state] = []
            counties_by_state[state].append({"fips": fips, "name": name})
    return counties_by_state

# url: https://www2.census.gov/geo/tiger/TIGER2007FE/09_CONNECTICUT/09001_Fairfield/fe_2007_09001_cousub.zip
def download_and_extract_shapefile(state, county, year, fips):
    # Constructing the download URL
    base_url = "https://www2.census.gov/geo/tiger/TIGER{year}FE/{state_fips}_{state_name}/{county_fips}_{county}/fe_{year}_{county_fips}_cousub.zip"
    state_fips, state_name = state.split('_')
    county_fips = fips
    county_dir_name = f"{county_fips}_{county.replace(' ', '_')}"
    download_url = base_url.format(year=year, state_fips=state_fips, state_name=state_name.replace(' ', '_'), county_fips=county_fips, county=county)

    # Download the file
    response = requests.get(download_url)
    if response.status_code == 200:
        # Define the path to save the zip file and extract to
        county_dir_path = os.path.join('Data', '2007', state, county_dir_name)
        zip_path = os.path.join(county_dir_path, f'{county_fips}_{county}.zip')

        # Ensure the directories exist
        os.makedirs(county_dir_path, exist_ok=True)

        # Write the zip file to the specified path
        with open(zip_path, 'wb') as file:
            file.write(response.content)

        # Extract the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(county_dir_path)
        os.remove(zip_path)  # Remove the zip file after extracting

        print(f'Successfully downloaded and extracted {county} in {state}')
    else:
        print(f'Failed to download data for {county} in {state}. URL: {download_url} returned status code {response.status_code}')

# Replace 'path_to_your_csv' with the actual path to your CSV file
counties_by_state = read_csv_to_dict("fips-by-state.csv")
for state, counties in counties_by_state.items():
    if state in states_to_download:  # Only proceed if the state is in the list of states to download
        for county in counties:
            download_and_extract_shapefile(state, county['name'], 2007, county['fips'])

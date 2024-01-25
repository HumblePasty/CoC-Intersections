import os
import pandas as pd
import geopandas as gpd


def merge_county_subdivisions(base_dir, year, states_fips):
    merged_base_dir = os.path.join(base_dir, 'shapefiles', 'county subdivisions', 'Merged', str(year))

    for state, fips in states_fips.items():
        # Define the directory for the current state and year within the county subdivisions folder
        state_dir = os.path.join(base_dir, 'shapefiles', 'county subdivisions', str(year), f"{fips}_{state.upper()}")
        # Define the directory to store merged shapefiles in the 'Merged' folder within the specific state directory
        merged_state_dir = os.path.join(merged_base_dir, f"{fips}_{state.upper()}")

        # Create a directory for merged shapefiles if it doesn't exist
        if not os.path.exists(merged_state_dir):
            os.makedirs(merged_state_dir)

        # Initialize an empty list to hold GeoDataFrames
        gdfs = []

        # Check if the state directory exists and list all subdirectories (each representing a county)
        if os.path.exists(state_dir):
            counties = [d for d in os.listdir(state_dir) if os.path.isdir(os.path.join(state_dir, d))]

            # Loop through each county directory to find and process shapefiles
            for county in counties:
                county_dir = os.path.join(state_dir, county)
                shapefiles = [f for f in os.listdir(county_dir) if f.endswith('.shp')]
                for shp in shapefiles:
                    filepath = os.path.join(county_dir, shp)
                    gdf = gpd.read_file(filepath)
                    gdfs.append(gdf)

        # Merge all GeoDataFrames into one
        if gdfs:  # Check if the list is not empty
            merged_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))

            # Save the merged GeoDataFrame to a new shapefile in the specific state's Merged directory
            output_filename = f'fe_{year}_{fips}_cousub.shp'
            merged_gdf.to_file(os.path.join(merged_state_dir, output_filename))


# Base directory where the 'county subdivisions' folder is located
base_directory = 'D:\\UMich\\z-others\\Haolin_Code'  # Adjust this path to your specific setup

# Specify the year you want to process
year_to_process = 2007

# Dictionary of states and their corresponding FIPS codes you want to process
states_fips_codes = {
    'Connecticut': '09',
    'Illinois': '17',
    'Indiana': '18',
    'Kansas': '20',
    'Maine': '23',
    'Massachusetts': '25',
    'Michigan': '26',
    'Minnesota': '27',
    'Missouri': '29',
    'New Hampshire': '33',
    'New Jersey': '34',
    'New York': '36',
    'North Dakota': '38',
    'Ohio': '39',
    'Pennsylvania': '42',
    'Rhode Island': '44',
    'South Carolina': '45',
    'Vermont': '50',
    'Wisconsin': '55',
}

# Call the function with the specified parameters
merge_county_subdivisions(base_directory, year_to_process, states_fips_codes)

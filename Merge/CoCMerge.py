import os
import geopandas as gpd
import pandas as pd


def merge_shapefiles(base_dir, years, states):
    for year in years:
        for state in states:
            # Define the directory for the current state and year within the Continuum of Care folder
            state_dir = os.path.join(base_dir, 'Continuums of Care', str(year), state)
            # Define the directory to store merged shapefiles outside the Continuum of Care folder, in a parallel 'Merged' folder
            merged_dir = os.path.join(base_dir, 'CoC_Merged', str(year), state)

            # Create a directory for merged shapefiles if it doesn't exist
            if not os.path.exists(merged_dir):
                os.makedirs(merged_dir)

            # Initialize an empty list to hold GeoDataFrames
            gdfs = []

            # Adjust the path and filename handling based on the year
            if year in [2007, 2008, 2009]:
                # List all shapefiles in the state's directory for the year
                if os.path.exists(state_dir):
                    shapefiles = [f for f in os.listdir(state_dir) if f.endswith('.shp')]

                    # Load each shapefile into a GeoDataFrame and add it to the list
                    for shp in shapefiles:
                        filepath = os.path.join(state_dir, shp)
                        gdf = gpd.read_file(filepath)
                        # Extract the CoC number from the filename based on year-specific patterns
                        if year == 2007:
                            coc_number = shp.split('-')[1].split('.')[0]
                        elif year == 2008:
                            coc_number = shp.split('_')[1].split('.')[0]
                        elif year == 2009:
                            coc_number = shp.split('_')[1].split('.')[0]
                        # Create a new column 'CoC_Number' with the extracted CoC number
                        gdf['CoC_Number'] = coc_number
                        gdfs.append(gdf)

            elif year >= 2010:
                # For 2010, each shapefile is stored in a subfolder
                subdirs = [d for d in os.listdir(state_dir) if os.path.isdir(os.path.join(state_dir, d))]
                for subdir in subdirs:
                    shp_path = os.path.join(state_dir, subdir)
                    shapefiles = [f for f in os.listdir(shp_path) if f.endswith('.shp')]
                    for shp in shapefiles:
                        filepath = os.path.join(shp_path, shp)
                        gdf = gpd.read_file(filepath)
                        # Extract the CoC number from the subdirectory name
                        coc_number = subdir.split('_')[1]
                        # Create a new column 'CoC_Number' with the extracted CoC number
                        gdf['CoC_Number'] = coc_number
                        gdfs.append(gdf)

            # Merge all GeoDataFrames into one
            if gdfs:  # Check if the list is not empty
                merged_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))

                # Save the merged GeoDataFrame to a new shapefile
                output_filename = f'{state.replace(" ", "_")}_{year}_CoC_Merged.shp'
                merged_gdf.to_file(os.path.join(merged_dir, output_filename))
                print(f'Saved Merged File for {state} {year}')  # Print a message to the console


# Base directory where the 'Continuum of Care' folders are located
base_directory = "D:\\UMich\\z-others\\Haolin_Code\\shapefiles"
# Specify the years and states you want to process
# years_to_process = range(2007, 2024)
years_to_process = [2018]
states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"
]

# Adding additional territories
territories = ["District of Columbia", "Guam", "Puerto Rico", "Virgin Islands of the United States"]

# Combine the states and territories into one list
states_to_process = states + territories

# Call the function with the specified parameters
merge_shapefiles(base_directory, years_to_process, states_to_process)

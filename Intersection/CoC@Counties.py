"""
author: Haolin Li
last updated: 1/2/2023

This script performs the overlay operation between CoC and county shapefiles. (CoC@Counties)

output: shapefile and csv table

Structure of the input files:
- shapefiles
    - CoC_Merged
        - 2007
            - Alabama
                - AL_2007_CoC_Merged.shp
                - AL_2007_CoC_Merged.shx
                - ...
            - Alaska
            - ...
        - 2008
        - 2009
        - 2010
    - counties
        - 2007
            - 01_ALABAMA
                - fe_2007_01_county10.shp
                - fe_2007_01_county10.shx
                - ...
            - 02_ALASKA
            - ...
        - 2008
        - 2009
        - 2010

Structure of the output files:
- Intersection
    - Output
        - 2007
            - CoC@Counties
                - shp
                    - CoC_Counties_AL_07.shp
                    - CoC_Counties_AK_07.shp
                    - ...
                - csv
                    - CoC_Counties_AL_07.csv
                    - CoC_Counties_AK_07.csv
                    - ...
        - 2008
        - 2009
        - 2010
"""

import os
import geopandas as gpd


def overlay_coc_counties(years, states_fips, base_dir='D:\\UMich\\z-others\\Haolin_Code'):
    for year in years:
        for state, fips in states_fips.items():
            # Construct the CoC shapefile path
            coc_shp_path = os.path.join(base_dir, 'shapefiles', 'CoC_Merged', str(year), state,
                                        f"{state.replace(' ', '_')}_{year}_CoC_Merged.shp")

            # Construct the county shapefile path with a year-based prefix
            county_prefix = 'fe' if year == 2007 else 'tl'
            county_suffix = '10' if year == 2010 else ''
            county_shp_path = os.path.join(base_dir, 'shapefiles', 'counties', str(year),
                                           f"{fips}_{state.upper().replace(' ', '_')}",
                                           f"{county_prefix}_{year}_{fips}_county{county_suffix}.shp")

            # Read the shapefiles
            coc_gdf = gpd.read_file(coc_shp_path)
            county_gdf = gpd.read_file(county_shp_path)

            # Check CRS and reproject if necessary
            if coc_gdf.crs is None:
                print(f"Missing CRS for CoC shapefile: {coc_shp_path}, passing for now")
                continue
            if county_gdf.crs is None:
                print(f"Missing CRS for county shapefile: {county_shp_path}, passing for now")
                continue
            try:
                if coc_gdf.crs != county_gdf.crs:
                    county_gdf = county_gdf.to_crs(coc_gdf.crs)  # Reproject county shapefile to match CoC shapefile
            except ValueError as e:
                print(f"Error reprojecting CoC shapefile: {e}")
                continue

            # Perform overlay operation
            # set the buffer distance and simplify tolerance
            buffer_distance = 0.0001
            simplify_tolerance = 0.0001

            # simplify the geometry of the coc_gdf and county_gdf
            coc_gdf['geometry'] = coc_gdf['geometry'].buffer(buffer_distance).simplify(simplify_tolerance)
            county_gdf['geometry'] = county_gdf['geometry'].buffer(buffer_distance).simplify(simplify_tolerance)
            intersected_gdf = gpd.overlay(coc_gdf, county_gdf, how='intersection')

            # create new column in the intersected_gdf to store the % area of the current county that is in each CoC
            intersected_gdf['area'] = intersected_gdf['geometry'].area
            county_gdf['total_area'] = county_gdf['geometry'].area
            county_areas = county_gdf[['COUNTYFP' if year != 2010 else 'COUNTYFP10', 'total_area']].drop_duplicates()

            # merge the county_areas with the intersected_gdf
            intersected_gdf = intersected_gdf.merge(county_areas, on='COUNTYFP' if year != 2010 else 'COUNTYFP10', how='left')

            # calculate the % area of the belonging county
            intersected_gdf['%of_county'] = intersected_gdf['area'] / intersected_gdf['total_area']

            # coc_gdf['total_area'] = coc_gdf['geometry'].area
            # coc_areas = coc_gdf[['CoC_Number', 'total_area']].drop_duplicates()
            #
            # # merge the coc_areas with the intersected_gdf
            # intersected_gdf = intersected_gdf.merge(coc_areas, on='CoC_Number', how='left')
            #
            # # calculate the % area of each county / place / county subdivision that is in each CoC
            # intersected_gdf['%of_coc'] = intersected_gdf['area'] / intersected_gdf['total_area']

            # drop the columns that are not needed
            intersected_gdf = intersected_gdf.drop(columns=['total_area', 'area'])

            # Define the output path
            output_dir = os.path.join(base_dir, 'Intersection', 'Output', str(year), 'CoC@Counties', 'shp')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_path = os.path.join(output_dir, f"CoC_Counties_{fips}_{state}_{str(year)[2:]}.shp")

            # Save the output shapefile
            intersected_gdf.to_file(output_path)

            # export the csv table
            output_dir = os.path.join(base_dir, 'Intersection', 'Output', str(year), 'CoC@Counties')
            if not os.path.exists(os.path.join(output_dir, 'csv')):
                os.makedirs(os.path.join(output_dir, 'csv'))
            csv_output_path = os.path.join(output_dir, 'csv', f"CoC_Counties_{fips}_{state}_{str(year)[2:]}.csv")
            intersected_gdf.drop('geometry',axis=1).to_csv(csv_output_path, index=False)

            print(f"Saved CoC@Counties for {state} {year}")


# Example usage
# year_to_process = range(2007, 2024)
year_to_process = range(2018, 2024)
states_fips_codes = {
    'Alabama': '01',
    'Alaska': '02',
    'Arizona': '04',
    'Arkansas': '05',
    'California': '06',
    'Colorado': '08',
    'Connecticut': '09',
    'Delaware': '10',
    'District of Columbia': '11',
    'Florida': '12',
    'Georgia': '13',
    'Hawaii': '15',
    'Idaho': '16',
    'Illinois': '17',
    'Indiana': '18',
    'Iowa': '19',
    'Kansas': '20',
    'Kentucky': '21',
    'Louisiana': '22',
    'Maine': '23',
    'Maryland': '24',
    'Massachusetts': '25',
    'Michigan': '26',
    'Minnesota': '27',
    'Mississippi': '28',
    'Missouri': '29',
    'Montana': '30',
    'Nebraska': '31',
    'Nevada': '32',
    'New Hampshire': '33',
    'New Jersey': '34',
    'New Mexico': '35',
    'New York': '36',
    'North Carolina': '37',
    'North Dakota': '38',
    'Ohio': '39',
    'Oklahoma': '40',
    'Oregon': '41',
    'Pennsylvania': '42',
    'Rhode Island': '44',
    'South Carolina': '45',
    'South Dakota': '46',
    'Tennessee': '47',
    'Texas': '48',
    'Utah': '49',
    'Vermont': '50',
    'Virginia': '51',
    'Washington': '53',
    'West Virginia': '54',
    'Wisconsin': '55',
    'Wyoming': '56',
    'Guam': '66',
    'Puerto Rico': '72',
    'Virgin Islands of the United States': '78'
}

overlay_coc_counties(year_to_process, states_fips_codes)

"""
author: Haolin Li
Last updated: 1/8/2023

This script performs the overlay operation between CoC and places shapefiles. (CoC@Places)

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
    - places
        - 2007
            - 01_ALABAMA
                - fe_2007_01_place10.shp
                - fe_2007_01_place10.shx
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
            - CoC@Places
                - shp
                    - CoC_Places_AL_07.shp
                    - CoC_Places_AK_07.shp
                    - ...
                - csv
                    - CoC_Places_AL_07.csv
                    - CoC_Places_AK_07.csv
                    - ...
        - 2008
        - 2009
        - 2010
"""

import os
import geopandas as gpd


def overlay_coc_places(years, states_fips, base_dir='D:\\UMich\\z-others\\Haolin_Code'):
    for year in years:
        for state, fips in states_fips.items():
            # Construct the CoC shapefile path
            coc_shp_path = os.path.join(base_dir, 'shapefiles', 'CoC_Merged', str(year), state,
                                        f"{state.replace(' ', '_')}_{year}_CoC_Merged.shp")
            # Construct the places shapefile path
            places_prefix = 'fe' if year == 2007 else 'tl'
            places_suffix = '10' if year == 2010 else ''
            places_shp_path = os.path.join(base_dir, 'shapefiles', 'Census places', str(year),
                                           f"{fips}_{state.upper().replace(' ', '_')}",
                                           f"{places_prefix}_{year}_{fips}_place{places_suffix}.shp")

            # Read the intersecting shapefiles
            coc_shp = gpd.read_file(coc_shp_path)
            places_shp = gpd.read_file(places_shp_path)

            # Check CRS and reproject if necessary
            if coc_shp.crs is None:
                print(f"Missing CRS for CoC shapefile: {coc_shp_path}, passing for now")
                continue
            if places_shp.crs is None:
                print(f"Missing CRS for place shapefile: {places_shp_path}, passing for now")
                continue
            try:
                if coc_shp.crs != places_shp.crs:
                    places_shp = places_shp.to_crs(coc_shp.crs)  # Reproject county shapefile to match CoC shapefile
            except ValueError as e:
                print(f"Error reprojecting CoC shapefile: {e}")
                continue

            # Perform the overlay operation
            intersected_gdf = gpd.overlay(coc_shp, places_shp, how='intersection')

            # create new column in the intersected_gdf to store the % area of each places
            intersected_gdf['area'] = intersected_gdf['geometry'].area
            places_shp['total_area'] = places_shp['geometry'].area
            places_areas = places_shp[['PLACEFP' if year != 2010 else 'PLACEFP10', 'total_area']].drop_duplicates()

            # merge the places_areas with the intersected_gdf
            intersected_gdf = intersected_gdf.merge(places_areas, on='PLACEFP' if year != 2010 else 'PLACEFP10', how='left')

            # calculate the % area of each places in each place
            intersected_gdf['%of_place'] = intersected_gdf['area'] / intersected_gdf['total_area']

            # drop the unnecessary columns
            intersected_gdf = intersected_gdf.drop(columns=['total_area', 'area'])

            # save the output
            shp_output_dir = os.path.join(base_dir, 'Intersection', 'Output', str(year), 'CoC@Places', 'shp')
            if not os.path.exists(shp_output_dir):
                os.makedirs(shp_output_dir)
            intersected_gdf.to_file(os.path.join(shp_output_dir, f"CoC_Places_{fips}_{state}_{str(year)[2:]}.shp"))

            csv_output_dir = os.path.join(base_dir, 'Intersection', 'Output', str(year), 'CoC@Places', 'csv')
            if not os.path.exists(csv_output_dir):
                os.makedirs(csv_output_dir)
            intersected_gdf.drop('geometry',axis=1).to_csv(os.path.join(csv_output_dir, f"CoC_Places_{fips}_{state}_{str(year)[2:]}.csv"), index=False)

            print(f"Finished processing for {state} {year}")


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

overlay_coc_places(year_to_process, states_fips_codes)
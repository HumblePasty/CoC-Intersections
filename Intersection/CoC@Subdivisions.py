"""
author: Haolin Li
Last updated: 1/8/2023

This script performs the overlay operation between CoC and subdivisions shapefiles. (CoC@Places)

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
    - Subdivisions
        - 2007
            - 01_ALABAMA
                - fe_2007_01_Subdivisions.shp
                - fe_2007_01_Subdivisions.shx
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
            - CoC@Subdivisions
                - shp
                    - CoC_Subdivisions_AL_07.shp
                    - CoC_Subdivisions_AK_07.shp
                    - ...
                - csv
                    - CoC_Subdivisions_AL_07.csv
                    - CoC_Subdivisions_AK_07.csv
                    - ...
        - 2008
        - 2009
        - 2010
"""

import os
import geopandas as gpd


def overlay_coc_subdivisions(years, states_fips, base_dir='D:\\UMich\\z-others\\Haolin_Code'):
    for year in years:
        for state, fips in states_fips.items():
            # Construct the CoC shapefile path
            coc_shp_path = os.path.join(base_dir, 'shapefiles', 'CoC_Merged', str(year), state,
                                        f"{state.replace(' ', '_')}_{year}_CoC_Merged.shp")
            # Construct the subdivisions shapefile path
            subdivisions_prefix = 'fe' if year == 2007 else 'tl'
            subdivisions_suffix = '10' if year == 2010 else ''
            year_dir = year if year != 2007 else '2007_Merged'
            subdivisions_shp_path = os.path.join(base_dir, 'shapefiles', 'county subdivisions', str(year_dir),
                                                 f"{fips}_{state.upper().replace(' ', '_')}",
                                                 f"{subdivisions_prefix}_{year}_{fips}_cousub{subdivisions_suffix}.shp")

            # Read the shapefiles as GeoDataFrames
            coc_gdf = gpd.read_file(coc_shp_path)
            subdivisions_gdf = gpd.read_file(subdivisions_shp_path)

            # Check CRS
            if coc_gdf.crs is None:
                print(f'CRS for {coc_shp_path} is None. passing for now ...')
                continue
            if subdivisions_gdf.crs is None:
                print(f'CRS for {subdivisions_shp_path} is None. passing for now ...')
                continue
            try:
                if coc_gdf.crs != subdivisions_gdf.crs:
                    subdivisions_gdf = subdivisions_gdf.to_crs(
                        coc_gdf.crs)  # Reproject subdivisions shapefile to match CoC shapefile
            except ValueError as e:
                print(f"Error reprojecting CoC shapefile: {e}")
                continue

            # Perform the overlay operation
            intersected_gdf = gpd.overlay(coc_gdf, subdivisions_gdf, how='intersection')

            intersected_gdf['area'] = intersected_gdf['geometry'].area
            subdivisions_gdf['total_area'] = subdivisions_gdf['geometry'].area
            subdivisions_areas = subdivisions_gdf[['COUSUBFP' if year != 2010 else 'COUSUBFP10', 'total_area']].drop_duplicates()

            # merge the total area of each subdivision to the intersected_gdf
            intersected_gdf = intersected_gdf.merge(subdivisions_areas, on='COUSUBFP' if year != 2010 else 'COUSUBFP10', how='left')

            # calculate the percentage
            intersected_gdf['%of_subdiv'] = intersected_gdf['area'] / intersected_gdf['total_area']

            # drop the columns that are not needed
            intersected_gdf = intersected_gdf.drop(columns=['total_area', 'area'])

            output_dir = os.path.join(base_dir, 'Intersection', 'Output', str(year), 'CoC@Subdivisions')
            if not os.path.exists(os.path.join(output_dir, 'shp')):
                os.makedirs(os.path.join(output_dir, 'shp'))
            output_shp_path = os.path.join(output_dir, 'shp', f"CoC_Subdivisions_{fips}_{state}_{str(year)[2:]}.shp")

            intersected_gdf.to_file(output_shp_path)
            output_dir = os.path.join(base_dir, 'Intersection', 'Output', str(year), 'CoC@Subdivisions')
            if not os.path.exists(os.path.join(output_dir, 'csv')):
                os.makedirs(os.path.join(output_dir, 'csv'))
            output_csv_path = os.path.join(output_dir, 'csv', f"CoC_Subdivisions_{fips}_{state}_{str(year)[2:]}.csv")
            intersected_gdf.drop('geometry',axis=1).to_csv(output_csv_path, index=False)

            print(f"Finished CoC@Subdivisions processing for {state} {year}")

year_to_process = range(2007, 2024)
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

overlay_coc_subdivisions(year_to_process, states_fips_codes)

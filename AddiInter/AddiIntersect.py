import os
import geopandas as gpd

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


def construct_shapefile_paths(year, state, layer_type, base_dir='D:\\UMich\\Win24\\IntersectionProject'):
    if layer_type == 'CoC':
        layer_dir = os.path.join(base_dir, 'shapefiles', 'CoC_Merged', str(year), state,
                                        f"{state.replace(' ', '_')}_{year}_CoC_Merged.shp")
        return layer_dir
    elif layer_type == 'counties':
        county_prefix = 'fe' if year == 2007 else 'tl'
        county_suffix = '10' if year == 2010 else ''
        fips = states_fips_codes[state]
        layer_dir = os.path.join(base_dir, 'shapefiles', 'counties', str(year),
                                       f"{fips}_{state.upper().replace(' ', '_')}",
                                       f"{county_prefix}_{year}_{fips}_county{county_suffix}.shp")
        return layer_dir
    elif layer_type == 'county subdivisions':
        subdivisions_prefix = 'fe' if year == 2007 else 'tl'
        subdivisions_suffix = '10' if year == 2010 else ''
        fips = states_fips_codes[state]
        year_dir = year if year != 2007 else '2007_Merged'
        layer_dir = os.path.join(base_dir, 'shapefiles', 'county subdivisions', str(year_dir),
                                       f"{fips}_{state.upper().replace(' ', '_')}",
                                       f"{subdivisions_prefix}_{year}_{fips}_cousub{subdivisions_suffix}.shp")
        return layer_dir
    elif layer_type == 'Census places':
        places_prefix = 'fe' if year == 2007 else 'tl'
        places_suffix = '10' if year == 2010 else ''
        fips = states_fips_codes[state]
        layer_dir = os.path.join(base_dir, 'shapefiles', 'Census places', str(year),
                                       f"{fips}_{state.upper().replace(' ', '_')}",
                                       f"{places_prefix}_{year}_{fips}_place{places_suffix}.shp")
        return layer_dir



def perform_intersections(intersections, base_dir='D:\\UMich\\Win24\\IntersectionProject'):
    for year, combinations in intersections.items():
        for combo in combinations:
            state_a, layer_a, state_b, layer_b = combo
            fips_a = states_fips_codes[state_a]
            fips_b = states_fips_codes[state_b]

            # Construct paths for each layer
            layer_a_path = construct_shapefile_paths(year, state_a, layer_a, base_dir)
            layer_b_path = construct_shapefile_paths(year, state_b, layer_b, base_dir)

            # Read the shapefiles
            gdf_a = gpd.read_file(layer_a_path)
            gdf_b = gpd.read_file(layer_b_path)

            # Ensure CRS match or reproject
            if gdf_a.crs is None:
                print(f"Missing CRS for shapefile: {layer_a_path}, passing for now")
                continue
            if gdf_b is None:
                print(f"Missing CRS for shapefile: {layer_b_path}, passing for now")
                continue
            try:
                if gdf_a.crs != gdf_b.crs:
                    gdf_b = gdf_b.to_crs(gdf_a.crs)
            except ValueError as e:
                print(f"Error reprojecting CoC shapefile: {e}")
                continue

            # Perform intersection
            try:
                intersected_gdf = gpd.overlay(gdf_a, gdf_b, how='intersection')
            except Exception as e:
                print(f"Error during overlay operation for {state_a}-{state_b} in {year}: {e}")
                continue

            # create new column
            intersected_gdf['area'] = intersected_gdf['geometry'].area
            gdf_a['total_area'] = gdf_a['geometry'].area
            if layer_a == 'counties':
                gdf_a_area = gdf_a[['COUNTYFP' if year != 2010 else 'COUNTYFP10', 'total_area']].drop_duplicates()
                intersected_gdf = intersected_gdf.merge(gdf_a_area, on='COUNTYFP' if year != 2010 else 'COUNTYFP10', how='left')
                intersected_gdf['%of_county'] = intersected_gdf['area'] / intersected_gdf['total_area']
                # drop the unnecessary columns
                intersected_gdf = intersected_gdf.drop(columns=['total_area', 'area'])
                # save the shp output
                shp_output_dir = os.path.join(base_dir, 'AddiInter', 'Output', str(year), 'CoC@Counties', 'shp')
                if not os.path.exists(shp_output_dir):
                    os.makedirs(shp_output_dir)
                intersected_gdf.to_file(os.path.join(shp_output_dir, f"CoCOf{state_b}_CountyOf{state_a}_{str(year)[2:]}.shp"))
                # save the csv output
                csv_output_dir = os.path.join(base_dir, 'AddiInter', 'Output', str(year), 'CoC@Counties', 'csv')
                if not os.path.exists(csv_output_dir):
                    os.makedirs(csv_output_dir)
                csv_output_path = os.path.join(csv_output_dir, f"CoCOf{state_b}_CountyOf{state_a}_{str(year)[2:]}.csv")
                intersected_gdf.drop('geometry', axis=1).to_csv(csv_output_path, index=False)

            if layer_a == 'Census places':
                gdf_a_area = gdf_a[['PLACEFP' if year != 2010 else 'PLACEFP10', 'total_area']].drop_duplicates()
                intersected_gdf = intersected_gdf.merge(gdf_a_area, on='PLACEFP' if year != 2010 else 'PLACEFP10', how='left')
                intersected_gdf['%of_place'] = intersected_gdf['area'] / intersected_gdf['total_area']
                # drop the unnecessary columns
                intersected_gdf = intersected_gdf.drop(columns=['total_area', 'area'])
                # save the shp output
                shp_output_dir = os.path.join(base_dir, 'AddiInter', 'Output', str(year), 'CoC@Places', 'shp')
                if not os.path.exists(shp_output_dir):
                    os.makedirs(shp_output_dir)
                intersected_gdf.to_file(os.path.join(shp_output_dir, f"CoCOf{state_b}_PlacesOf{state_a}_{str(year)[2:]}.shp"))
                # save the csv output
                csv_output_dir = os.path.join(base_dir, 'AddiInter', 'Output', str(year), 'CoC@Places', 'csv')
                if not os.path.exists(csv_output_dir):
                    os.makedirs(csv_output_dir)
                csv_output_path = os.path.join(csv_output_dir, f"CoCOf{state_b}_PlacesOf{state_a}_{str(year)[2:]}.csv")
                intersected_gdf.drop('geometry', axis=1).to_csv(csv_output_path, index=False)


            elif layer_a == 'county subdivisions':
                gdf_a_area = gdf_a[['COUSUBFP' if year != 2010 else 'COUSUBFP10', 'total_area']].drop_duplicates()
                intersected_gdf = intersected_gdf.merge(gdf_a_area, on='COUSUBFP' if year != 2010 else 'COUSUBFP10', how='left')
                intersected_gdf['%of_subdivision'] = intersected_gdf['area'] / intersected_gdf['total_area']
                # drop the unnecessary columns
                intersected_gdf = intersected_gdf.drop(columns=['total_area', 'area'])
                # save the shp output
                shp_output_dir = os.path.join(base_dir, 'AddiInter', 'Output', str(year), 'CoC@Subdivisions', 'shp')
                if not os.path.exists(shp_output_dir):
                    os.makedirs(shp_output_dir)
                intersected_gdf.to_file(os.path.join(shp_output_dir, f"CoCOf{state_b}_PlacesOf{state_a}_{str(year)[2:]}.shp"))
                # save the csv output
                csv_output_dir = os.path.join(base_dir, 'AddiInter', 'Output', str(year), 'CoC@Subdivisions', 'csv')
                if not os.path.exists(csv_output_dir):
                    os.makedirs(csv_output_dir)
                csv_output_path = os.path.join(csv_output_dir, f"CoCOf{state_b}_PlacesOf{state_a}_{str(year)[2:]}.csv")
                intersected_gdf.drop('geometry', axis=1).to_csv(csv_output_path, index=False)


# Define intersections to perform
# Format: {year: [(state_a, layer_a, state_b, layer_b), ...], ...}
intersections_to_perform = {}
for year in range (2007, 2024):
    intersections_to_perform[year] = [
        ('Iowa', 'counties', 'Nebraska', 'CoC'),
        ('Iowa', 'Census places', 'Nebraska', 'CoC'),
        ('Nebraska', 'counties', 'Iowa', 'CoC'),
        ('Nebraska', 'Census places', 'Iowa', 'CoC'),
        ('Kansas', 'counties', 'Missouri', 'CoC'),
        ('Kansas', 'Census places', 'Missouri', 'CoC'),
        ('Kansas', 'county subdivisions', 'Missouri', 'CoC'),
        ('Alabama', 'counties', 'Georgia', 'CoC'),
        ('Alabama', 'Census places', 'Georgia', 'CoC'),
    ]
# intersections_to_perform = {
#     2007: [
#         ('Iowa', 'counties', 'Nebraska', 'CoC'),
#         ('Iowa', 'Census places', 'Nebraska', 'CoC'),
#         ('Nebraska', 'counties', 'Iowa', 'CoC'),
#         ('Nebraska', 'Census places', 'Iowa', 'CoC'),
#         ('Kansas', 'counties', 'Missouri', 'CoC'),
#         ('Kansas', 'Census places', 'Missouri', 'CoC'),
#         ('Kansas', 'county subdivisions', 'Missouri', 'CoC'),
#         ('Alabama', 'counties', 'Georgia', 'CoCs'),
#         ('Alabama', 'Census places', 'Georgia', 'CoCs'),
#     ],
# }

perform_intersections(intersections_to_perform)

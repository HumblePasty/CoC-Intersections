"""
This script is for breaking down the county shapefiles into state-based shapefiles from year 2011 on.
author: Haolin Li
Last updated: 1/15/2024
"""

import os
import geopandas as gpd


state_fips_to_name = {
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

base_dir = "D:\\UMich\\z-others\\Haolin_Code\\shapefiles\\counties"

for year in range(2011, 2024):
    file_path = os.path.join(base_dir, str(year), f"tl_{year}_us_county.shp")
    gdf = gpd.read_file(file_path)
    # Group by state
    for statefp, group in gdf.groupby('STATEFP'):
        state_name = state_fips_to_name.get(statefp, 'UNKNOWN')
        output_dir = os.path.join(base_dir, str(year), f"{statefp}_{state_name}")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file = os.path.join(output_dir, f"tl_{year}_{statefp}_county.shp")
        group.to_file(output_file)
        print(f"Saved {state_name} {year}")

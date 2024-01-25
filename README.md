# CoC-Intersections
A repository for codes generated during RA for residential land use regulations and child homelessness project, Dr. Joe LaBriola.

This job meant to create intersection between CoC and Census shapefiles [Counties/Places/Subdivisions] with new attribute that indicate the % that each polygon occupy the original county/place/subdivision.



## Glossaries

> **CoC**: Continuum of Care (regions where homelessness is evaluated by HUD and fundings for health care are delegated )
>
> **Census Places**: geographies that include Incorporated Places and Census Designated Places (CDPs).
>
> **Census Subdivisions**: minor civil divisions (MCDs) and census county divisions (CCDs)



## Data Sources

- [CoC Data Source](https://www.hudexchange.info/programs/coc/gis-tools/):

  by HUD (Housing and Urbanization Department of USA)

- Census Counties/Places/Subdivisions

  [TIGER Database](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)



## How to Run

1. Use codes in ``.\BulkDownload`` to bulk download all the data from the related sites, the downloaded data would be located in ``.\Data`` in each folder

2. Put the data into ``.\shapefiles`` folder in the following structure:

   ```
   - shapefiles
   	- Census places
   	- CoC_Merged
   	- Contiuumns of Care
   	- counties
   	- county subdivisions
   ```

   This would be the input data for the later process

3. Run codes in ``CountyProcess`` and ``Merge`` to process the data

4. Run all codes in ``Intersection`` to intersection the layers. The output would be in the ``.\Output`` folder

   Structure:

   ```
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
               - CoC@Places
               	- shp
               		- CoC_Places_AL_07_shp
               		- CoC_Places_AK_07.shp
               		- ...
                   - csv
                   	- CoC_Places_AL_07.csv
                       - CoC_Places_AK_07.csv
                       - ...
               - CoC@Subdivisions
               	- shp
               		- CoC_Subdivisions_AL_07_shp
               		- CoC_Subdivisions_AK_07.shp
               		- ...
                   - csv
                   	- CoC_Subdivisions_AL_07.csv
                       - CoC_Subdivisions_AK_07.csv
                       - ...
           - 2008
           	- ...
           - ...
   ```



## Sample Output Project on ArcGIS

[Sample input and output in 2007 for Connecticut](https://umich.maps.arcgis.com/home/item.html?id=b300cdb6d4ad412fb05c3f486599a328)

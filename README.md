# Cook
a data engineering package that facilitates spatial data ETL (based on GDAL)

### Environmental variables: 
- RECIPE_ENGINE=postgresql://USERNAME:PASSWORD@HOST:PORT/DBNAME
- BUILD_ENGINE=postgresql://USERNAME:PASSWORD@HOST:PORT/DBNAME

### What is `cook`?
This package is based on GDAL and mainly does the following:
- Archiving data from all different sources into an Archive database, which we call `recipe`
    - From open data or bytes of big apple:
        - [ ] __csv__
        - [ ] __geojson__
        - [ ] __shapefile__
    - From local:
        - [ ] __csv__
        - [ ] __geojson__
        - [ ] __shapefile__
    - From FTP:
        - [ ] __csv__
        - [ ] __geojson__
        - [ ] __shapefile__

- Importing data from `recipe` to any production database (`build`)

### __Archiver__ Features
Archiver can be initaited with a `RECIPE_ENGINE` database url and the `archive_table` method takes in a dictionary of configurations for each dataset

e.g.
```
from cook import Archiver
import os

engine = os.environ.get('RECIPE_ENGINE', '')
archiver = Archiver(engine=engine)

archiver.archive_table(config={
                'schema_name': 'qpl_libraries',
                'path': 'https://data.cityofnewyork.us/api/views/kh3d-xhq7/rows.csv', 
                'geometryType':'POINT',
                'srcSRS':'EPSG:4326',
                'dstSRS':'EPSG:4326',
                'layerCreationOptions':['OVERWRITE=YES'],
                'srcOpenOptions': ['AUTODETECT_TYPE=NO',
                                'EMPTY_STRING_AS_NULL=YES',
                                'GEOM_POSSIBLE_NAMES=*geom*',
                                'X_POSSIBLE_NAMES=longitude,x',
                                'Y_POSSIBLE_NAMES=latitude,y']
                })
```
+ The dataset `qpl_libraries` will be archived in the `recipe` database under schema `qpl_libraries` with the current date (in `%Y/%m/%d` format) as table name
+ gdal will be pulling directly from NYC open data, no intermediary directories or files are created
+ `geometryType` specifies geometry type, can also be `MULTIPOLYGON`, `POLYGON` and etc.
+ `srcSRS` and `dstSRS` allows you to convert projection
+ `layerCreationOptions` allows you to overwrite a table or append, for most use cases we default to `overwrite`
+ `srcOpenOptions` allows geom detection, or coordinates detection, if detected, a `wkb_geometry` field will be automatically generated.
+ `SQLStatement` a SQL statement that allows you to filter transform the data you would like to load, this is currently in developement because it's unclear what the table name is when you are loading a layer from a arbitrary url.

### __Importer__ Features
+ first of all you need to have a `recipe` database set up with version-controlled datasets
+ `import_table` will automatically move the latest version of wanted table to the `build` database (if no version timestamps are specified)
e.g.
```
from cook import Importer
import os
RECIPE_ENGINE = os.environ.get('EDM_DATA', '')
BUILD_ENGINE=os.environ.get('BUILD_ENGINE', '')

importer = Importer(RECIPE_ENGINE, BUILD_ENGINE)
importer.import_table(schema_name='qpl_libraries', version='latest')
importer.import_table(schema_name='dpr_parksproperties', version='latest')
importer.import_table(schema_name='facilities', version='latest')
```

### Nice to have and Next steps
+ mechanisms to delete datasets
+ archive entire `recipe` database to s3
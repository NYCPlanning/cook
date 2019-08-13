def test_geojson_to_archive():
        from cook import Archiver
        import os
        engine = os.environ.get('RECIPE_ENGINE', '')

        archiver = Archiver(engine=engine)

        archiver.archive_table(config={
                'schema_name': 'parks_properties',
                'path': 'https://data.cityofnewyork.us/api/geospatial/k2ya-ucmv?method=export&format=GeoJSON', 
                'geometryType':'MULTIPOLYGON',
                'srcSRS':'EPSG:4326',
                'dstSRS':'EPSG:4326',
                'layerCreationOptions':['OVERWRITE=YES'],
                })

test_geojson_to_archive()

def test_csv_to_archive():
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

test_csv_to_archive()
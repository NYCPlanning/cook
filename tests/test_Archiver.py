# External url tests (including opendata, bytes of big apple)
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

def test_ziped_shp_to_archive():
        from cook import Archiver
        import os
        engine = os.environ.get('RECIPE_ENGINE', '')

        archiver = Archiver(engine=engine)

        archiver.archive_table(config={
                'schema_name': 'dcp_censustracts',
                'path': 'https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyct2010wi_19b.zip/nyct2010wi_19b/nyct2010wi.shp', 
                'geometryType':'MULTIPOLYGON',
                'srcSRS':'EPSG:2263',
                'dstSRS':'EPSG:4326',
                'layerCreationOptions':['OVERWRITE=YES', 'PRECISION=NO'], #precision=No otherwise have numeric field overflow
                'srcOpenOptions': []
                })

def test_ftp_ziped_shp_to_archive():
        from cook import Archiver
        import os
        engine = os.environ.get('RECIPE_ENGINE', '')
        ftp_prefix = os.environ.get('FTP_PREFIX', '')
        archiver = Archiver(engine=engine)

        archiver.archive_table(config={
                'schema_name': 'dcp_censustracts',
                # 'path': 'ftp://user:password@example.com/foldername/file.zip/example.shp',
                'path': f'{ftp_prefix}/foldername/file.zip/example.shp',
                'geometryType':'MULTIPOLYGON',
                'srcSRS':'EPSG:2263',
                'dstSRS':'EPSG:4326',
                'layerCreationOptions':['OVERWRITE=YES', 'PRECISION=NO'],
                'srcOpenOptions': []
                })
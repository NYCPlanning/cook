# External url tests (including opendata, bytes of big apple)
def test_geojson():
        from cook import Archiver
        import os
        
        engine = os.environ.get('RECIPE_ENGINE', '')
        ftp_prefix = os.environ.get('FTP_PREFIX', '')
        archiver = Archiver(engine=engine, ftp_prefix=ftp_prefix)

        archiver.archive_table(config={
                'schema_name': 'test',
                'version_name': 'opendata_geojson',
                'path': 'https://data.cityofnewyork.us/api/geospatial/k2ya-ucmv?method=export&format=GeoJSON', 
                'geometryType':'MULTIPOLYGON',
                'srcSRS':'EPSG:4326',
                'dstSRS':'EPSG:4326',
                'layerCreationOptions':['OVERWRITE=YES'],
                })

def test_csv():
        from cook import Archiver
        import os
        engine = os.environ.get('RECIPE_ENGINE', '')
        ftp_prefix = os.environ.get('FTP_PREFIX', '')

        archiver = Archiver(engine=engine, ftp_prefix=ftp_prefix)
        
        archiver.archive_table(config={
                'schema_name': 'test',
                'version_name': 'opendata_csv',
                'path': 'https://data.cityofnewyork.us/api/views/n5mv-nfpy/rows.csv', 

                'geometryType':'POINT',
                'srcSRS':'EPSG:4326',
                'dstSRS':'EPSG:4326',

                'layerCreationOptions':['OVERWRITE=YES'],

                'srcOpenOptions': ['AUTODETECT_TYPE=NO',
                                'EMPTY_STRING_AS_NULL=YES',
                                'GEOM_POSSIBLE_NAMES=*geom*', 
                                'X_POSSIBLE_NAMES=longitude,x',
                                'Y_POSSIBLE_NAMES=latitude,y'],

                'newFieldNames': ['BOROUGH', 'BLOCK', 'LOT', 'PARCEL_NAME', 
                                'PARCEL_ADDRESS', 'JURIS', 'JurisDescription', 
                                'RPAD', 'RPAD_DESCRIPTION', 'PROP_FRONT', 
                                'PROP_DEPTH', 'PROP_SQFT', 'IRREG', 'BLD_FRONT', 
                                'BLD_DEPTH', 'BLD_SQFT', 'NUM_BLD', 'FLOORS', 
                                'CommunityBoard','COUNCILDISTRICT', 'COUNCILMEMBER_NAME', 
                                'PR_ZONE','OV_ZONE', 'SD_ZONE', 'BBL', 'WATERFRONT', 
                                'URBANRENEWALSITE', 'Agency', 'Owned_Leased', 'PrimaryUse', 
                                'FinalCommitment', 'Agreement_Lease_Out', 'Postcode', 
                                'Latitude', 'Longitude', 'CensusTract', 'BIN', 'NTA'],

                'SQLStatement': 'SELECT * FROM dcas_ipis LIMIT 5'
                })

def test_ftp_ziped_shp():
        from cook import Archiver
        import os
        engine = os.environ.get('RECIPE_ENGINE', '')
        ftp_prefix = os.environ.get('FTP_PREFIX', '')

        archiver = Archiver(engine=engine, ftp_prefix=ftp_prefix)

        archiver.archive_table(config={
                'schema_name': 'test',
                'version_name': 'ziped_shp',
                "path": "ftp://agencySourceData/dcp/DCP_Quartersection_Index.zip", 
                'geometryType':'MULTIPOLYGON',
                'srcSRS':'EPSG:2263',
                'dstSRS':'EPSG:4326',
                'layerCreationOptions':['OVERWRITE=YES', 'PRECISION=NO'],
                'srcOpenOptions': []
                })

def test_ziped_csv():
        from cook import Archiver
        import os
        engine = os.environ.get('RECIPE_ENGINE', '')
        ftp_prefix = os.environ.get('FTP_PREFIX', '')

        archiver = Archiver(engine=engine, ftp_prefix=ftp_prefix)

        archiver.archive_table(config={
                'schema_name': 'test',
                'version_name': 'ziped_csv',
                "path": "https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyczoningtaxlotdb_20190731.zip/NY_ZoningTaxLotDB_20190731.csv", 
                'geometryType':'POINT',
                'srcSRS':'EPSG:2263',
                'dstSRS':'EPSG:4326',
                'layerCreationOptions':['OVERWRITE=YES', 'PRECISION=NO'],
                'srcOpenOptions': []
                })

def test_s3_zip():
        from cook import Archiver
        import os
        engine = os.environ.get('RECIPE_ENGINE', '')
        ftp_prefix = os.environ.get('FTP_PREFIX', '')
        s3_endpoint = os.environ.get('AWS_S3_ENDPOINT', '')
        s3_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
        s3_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', '')

        archiver = Archiver(engine=engine, 
                        ftp_prefix=ftp_prefix, 
                        s3_endpoint=s3_endpoint,
                        s3_secret_access_key=s3_secret_access_key,
                        s3_access_key_id=s3_access_key_id)

        archiver.archive_table(config={
                'schema_name': 'test',
                'version_name': 's3_zip',
                'path': 's3://edm-storage/ZONING_FEATURES/commercial_overlays/20190830/commercial_overlays.zip', 
                'geometryType':'NONE'})

def test_s3_csv():
        from cook import Archiver
        import os
        engine = os.environ.get('RECIPE_ENGINE', '')
        ftp_prefix = os.environ.get('FTP_PREFIX', '')
        s3_endpoint = os.environ.get('AWS_S3_ENDPOINT', '')
        s3_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
        s3_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', '')

        archiver = Archiver(engine=engine, 
                        ftp_prefix=ftp_prefix, 
                        s3_endpoint=s3_endpoint,
                        s3_secret_access_key=s3_secret_access_key,
                        s3_access_key_id=s3_access_key_id)

        archiver.archive_table(config={
                'schema_name': 'test',
                'version_name': 's3_csv',
                'path': 's3://edm-recipes/2019-11-14/recipes.csv', 
                'geometryType':'NONE'})
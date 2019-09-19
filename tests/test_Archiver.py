# External url tests (including opendata, bytes of big apple)
def test_geojson_to_archive():
        from cook import Archiver
        import os
        engine = os.environ.get('RECIPE_ENGINE', '')
        ftp_prefix = os.environ.get('FTP_PREFIX', '')

        archiver = Archiver(engine=engine, ftp_prefix=ftp_prefix)

        archiver.archive_table(config={
                'schema_name': 'parks_properties',
                'version_name': 'test_test',
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
        ftp_prefix = os.environ.get('FTP_PREFIX', '')

        archiver = Archiver(engine=engine, ftp_prefix=ftp_prefix)
        
        archiver.archive_table(config={
                'schema_name': 'dcas_ipis',
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

def test_ziped_shp_to_archive():
        from cook import Archiver
        import os
        engine = os.environ.get('RECIPE_ENGINE', '')
        ftp_prefix = os.environ.get('FTP_PREFIX', '')

        archiver = Archiver(engine=engine, ftp_prefix=ftp_prefix)

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

        archiver = Archiver(engine=engine, ftp_prefix=ftp_prefix)

        archiver.archive_table(config={
                'schema_name': 'dcp_zoningmapindex',
                "path": "FTP_PREFIX/agencySourceData/dcp/DCP_Quartersection_Index.zip/DCP_Quartersection_Index.shp", 
                'geometryType':'MULTIPOLYGON',
                'srcSRS':'EPSG:2263',
                'dstSRS':'EPSG:4326',
                'layerCreationOptions':['OVERWRITE=YES', 'PRECISION=NO'],
                'srcOpenOptions': []
                })

def test_ziped_csv_to_archive():
        from cook import Archiver
        import os
        engine = os.environ.get('RECIPE_ENGINE', '')
        ftp_prefix = os.environ.get('FTP_PREFIX', '')

        archiver = Archiver(engine=engine, ftp_prefix=ftp_prefix)

        archiver.archive_table(config={
                'schema_name': 'dcp_zoningtaxlots',
                "path": "https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyczoningtaxlotdb_20190731.zip/NY_ZoningTaxLotDB_20190731.csv", 
                'geometryType':'POINT',
                'srcSRS':'EPSG:2263',
                'dstSRS':'EPSG:4326',
                'layerCreationOptions':['OVERWRITE=YES', 'PRECISION=NO'],
                'srcOpenOptions': []
                })
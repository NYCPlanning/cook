from sqlalchemy import create_engine
import os
from datetime import datetime
from operator import itemgetter
from osgeo.gdalconst import GA_ReadOnly
from osgeo import ogr
from urllib.parse import urlparse
from osgeo import gdal
from dateutil import parser

class Importer():
    def __init__(self, 
                RECIPE_ENGINE=os.environ.get('RECIPE_ENGINE', ''), 
                BUILD_ENGINE=os.environ.get('BUILD_ENGINE', '')):

        self.src_engine_url = RECIPE_ENGINE
        self.dst_engine_url = BUILD_ENGINE

        self.src_engine = self.parse_engine(RECIPE_ENGINE)
        self.dst_engine = self.parse_engine(BUILD_ENGINE)
    
    def parse_engine(self, engine):
        result = urlparse(engine)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        portnum = result.port
        
        return f'PG:host={hostname} port={portnum} user={username} dbname={database} password={password}'

    def import_table(self, schema_name, version='latest'):
        srcDS = gdal.OpenEx(self.src_engine, gdal.OF_VECTOR)
        dstDS = gdal.OpenEx(self.dst_engine, gdal.OF_VECTOR)

        print(f'Importing {schema_name}."{version}" to build...\n')

        try: 
            gdal.VectorTranslate(
                dstDS,
                srcDS,
                SQLStatement=f'SELECT * FROM {schema_name}."{version}"',
                format='PostgreSQL',
                layerName=schema_name,
                accessMode='overwrite',
                callback=gdal.TermProgress)
        except: 
            print(f'Importing {schema_name}."{version}" failed...\n')
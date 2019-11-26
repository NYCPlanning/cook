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

    def get_latest_version(self, schema_name):
        src_connection = create_engine(self.src_engine_url).connect()
        query = f'SELECT table_name\
                FROM information_schema.tables AS t\
                WHERE t.table_schema=\'{schema_name}\''

        result = src_connection.execute(query)

        def try_date(date): 
            try: 
                return parser.parse(date, dayfirst=False)
            except: 
                return None

        date_times = [i for i in [(try_date(date[0]), date[0]) for date in result] if i[0] is not None]
        if len(date_times) == 0: 
            return 'latest'
        else: 
            return max(date_times, key=itemgetter(0))[1]

    def import_table(self, schema_name, version='latest'):
        if version == 'latest': 
            version = self.get_latest_version(schema_name)
            
        srcDS = gdal.OpenEx(self.src_engine, gdal.OF_VECTOR)
        dstDS = gdal.OpenEx(self.dst_engine, gdal.OF_VECTOR)

        print(f'Importing {schema_name} to build...\n')

        gdal.VectorTranslate(
            dstDS,
            srcDS,
            format='PostgreSQL',
            layerName=f'{schema_name}."{version}"',
            accessMode='overwrite',
            callback=gdal.TermProgress)
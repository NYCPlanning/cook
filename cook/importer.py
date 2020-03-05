from sqlalchemy import create_engine
import os
from datetime import datetime
from operator import itemgetter
from osgeo.gdalconst import GA_ReadOnly
from osgeo import ogr
from .utils import parse_engine
from osgeo import gdal
from dateutil import parser

class Importer():
    def __init__(self, 
                RECIPE_ENGINE=os.environ.get('RECIPE_ENGINE', ''), 
                BUILD_ENGINE=os.environ.get('BUILD_ENGINE', '')):

        self.src_engine_url = RECIPE_ENGINE
        self.dst_engine_url = BUILD_ENGINE

        self.src_engine = parse_engine(RECIPE_ENGINE)
        self.dst_engine = parse_engine(BUILD_ENGINE)

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
    
    def import_table_expert(self, schema_name, version, 
                            target_schema_name, target_version):

        srcDS = gdal.OpenEx(self.src_engine, gdal.OF_VECTOR)
        dstDS = gdal.OpenEx(self.dst_engine, gdal.OF_VECTOR)

        print(f'Importing {schema_name}."{version}" to {target_schema_name}."{target_version}"...\n')

        try:
            gdal.VectorTranslate(
                dstDS,
                srcDS,
                SQLStatement=f'SELECT * FROM {schema_name}."{version}"',
                format='PostgreSQL',
                layerName=f'{target_schema_name}."{target_version}"',
                accessMode='overwrite',
                callback=gdal.TermProgress)
        except: 
            print(f'Importing {schema_name}."{version}" failed...\n')
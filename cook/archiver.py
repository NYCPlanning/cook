import os
import logging
from osgeo import ogr
from osgeo import gdal
from pathlib import Path
from urllib.parse import urlparse
from osgeo.gdalconst import GA_ReadOnly
from datetime import datetime
from sqlalchemy import engine

class Archiver():
    def __init__(self,
                 engine='env://RECIPE_ENGINE'):

        if engine.startswith('env://'):
            env_var = engine[6:]
            engine = os.environ.get(env_var)
            if engine is None:
                raise ValueError("Couldn't connect to DB - "
                                 "Please set your '%s' environment variable" % env_var)

        self.engine = self.parse_engine(engine)

    def parse_engine(self, engine):
        result = urlparse(engine)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        portnum = result.port
        
        return f'PG:host={hostname} port={portnum} user={username} dbname={database} password={password}'
    
    @staticmethod
    def format_path(path):
        """ Adds vsizip to [path] if [path] is a ShapeFile."""
        filename, extension = os.path.splitext(os.path.basename(path))
        
        if extension == '.shp' or extension == '.zip':
            path = "/vsizip/vsicurl/" + path
        return path
        
    def get_allowed_drivers(path):
        """ Returns allowed drivers for OpenEx given the file type of [path]"""
        allowed_drivers = [gdal.GetDriver(i).GetDescription() for i in range(gdal.GetDriverCount())]
        
        filename, extension = os.path.splitext(os.path.basename(path))
        if extension == '.csv':
            allowed_drivers = [driver for driver in allowed_drivers if "JSON" not in driver]
        return allowed_drivers
        
    
    @staticmethod
    def load_srcDS(path, open_options):
        path = Archiver.format_path(path)        
        allowed_drivers = Archiver.get_allowed_drivers(path)
        srcDS = gdal.OpenEx(path, 
                            gdal.OF_VECTOR,
                            open_options=open_options,
                            allowed_drivers=allowed_drivers)

        # OpenEx returns None if the file can't be opened
        if (srcDS is None):
            raise Exception(f'Could not open {path}') 

        return srcDS
    
    def archive_table(self, config):
        tab = [ 0 ]
        def my_cbk(pct, _, arg):
            assert pct >= tab[0]
            tab[0] = pct
            return 1

        schema_name = config.get('schema_name', '')
        path = config.get('path', '')
        layerCreationOptions=config.get('layerCreationOptions', ['OVERWRITE=YES'])
        dstSRS=config.get('dstSRS', 'EPSG:4326')
        srcSRS=config.get('srcSRS', 'EPSG:4326')
        geometryType=config.get('geometryType', 'POINT')
        SQLStatement=config.get('SQLStatement', None)
        srcOpenOptions=config.get('srcOpenOptions', 
                                ['AUTODETECT_TYPE=NO',
                                'EMPTY_STRING_AS_NULL=YES'])

        # initiate destination
        dstDS = gdal.OpenEx(self.engine, gdal.OF_VECTOR)

        # initiate source
        srcDS = Archiver.load_srcDS(path, srcOpenOptions)

        # check on schema
        dstDS.ExecuteSQL(f'CREATE SCHEMA IF NOT EXISTS {schema_name};')
        
        layerName = f'{schema_name}.{datetime.today().strftime("%Y/%m/%d")}'
        
        print(f'Archiving {layerName} to recipes...\n')

        gdal.VectorTranslate(
            dstDS,
            srcDS,
            SQLStatement=SQLStatement,
            format='PostgreSQL',
            layerCreationOptions=layerCreationOptions,
            dstSRS=dstSRS,
            srcSRS=srcSRS,
            geometryType=geometryType,
            layerName=layerName,
            accessMode='overwrite',
            callback=gdal.TermProgress)
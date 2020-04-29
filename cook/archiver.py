import os
from osgeo import ogr
from osgeo import gdal
from pathlib import Path
from .utils import parse_engine
from datetime import datetime
from sqlalchemy import engine

class Archiver():
    def __init__(self, ftp_prefix, engine, s3_endpoint='', 
                s3_secret_access_key='', s3_access_key_id=''):

        self.engine = parse_engine(engine)
        self.ftp_prefix=ftp_prefix
        self.s3_endpoint=s3_endpoint
        self.s3_secret_access_key=s3_secret_access_key
        self.s3_access_key_id=s3_access_key_id
    
    @staticmethod
    def format_path(path):
        """ 
            Adds vsis3 if path is from s3
            - s3://edm-recipes/recipes.csv

            Adds vsizip to [path] if [path] is zipped.
            - abcd.zip/abcd.shp
            - abcd.zip/abcd.csv
            - etc
        """
        if '.zip' in path:
            if 'http' in path:
                path = "/vsizip/vsicurl/" + path
            elif 's3://' in path: 
                path = "/vsizip/vsis3/" + path.replace('s3://', '')
            else:
                path = "/vsizip/" + path
        if 's3://' in path and '.zip' not in path:
            path = path.replace('s3://', '/vsis3/')
        
        return path
        
    def get_allowed_drivers(path):
        """ 
            Returns allowed drivers for OpenEx 
            given the file type of [path]
        """
        allowed_drivers = [gdal.GetDriver(i).GetDescription() for i in range(gdal.GetDriverCount())]

        filename, extension = os.path.splitext(os.path.basename(path))
        if extension == '.csv':
            allowed_drivers = [driver for driver in allowed_drivers if "JSON" not in driver]
        return allowed_drivers
        
    @staticmethod
    def load_srcDS(path, open_options, newFieldNames, 
                    s3_endpoint,
                    s3_secret_access_key, 
                    s3_access_key_id):
        
        gdal.SetConfigOption('AWS_S3_ENDPOINT', s3_endpoint)
        gdal.SetConfigOption('AWS_SECRET_ACCESS_KEY', s3_secret_access_key)
        gdal.SetConfigOption('AWS_ACCESS_KEY_ID', s3_access_key_id)

        path = Archiver.format_path(path)
        allowed_drivers = Archiver.get_allowed_drivers(path)
        srcDS = gdal.OpenEx(path,
                            gdal.OF_VECTOR,
                            open_options=open_options,
                            allowed_drivers=allowed_drivers)
        # OpenEx returns None if the file can't be opened
        if (srcDS is None):
            raise Exception(f'Could not open {path}')
        
        srcDS = Archiver.change_field_names(srcDS, newFieldNames)
        return srcDS

    @staticmethod
    def lower_underscore(field_name): 
        return field_name.replace(' ', '_').lower()

    @staticmethod
    def change_field_names(srcDS, newFieldNames): 
        layer = srcDS.GetLayer(0)
        layerDefn = layer.GetLayerDefn()

        if len(newFieldNames) == 0: 
            for i in range(layerDefn.GetFieldCount()):
                fieldDefn = layerDefn.GetFieldDefn(i)
                fieldName = fieldDefn.GetName()
                fieldDefn.SetName(Archiver.lower_underscore(fieldName))
        else:
            for i in range(len(newFieldNames)):
                fieldDefn = layerDefn.GetFieldDefn(i)
                fieldDefn.SetName(newFieldNames[i])

        return srcDS

    def archive_table(self, config):
        tab = [ 0 ]
        def my_cbk(pct, _, arg):
            assert pct >= tab[0]
            tab[0] = pct
            return 1

        schema_name = config.get('schema_name', '')
        version_name = config.get('version_name', '')
        path = config.get('path', '')
        layerCreationOptions = config.get('layerCreationOptions',
                                            ['OVERWRITE=YES'])
        dstSRS = config.get('dstSRS', 'EPSG:4326')
        srcSRS = config.get('srcSRS', 'EPSG:4326')
        geometryType = config.get('geometryType', 'NONE')
        SQLStatement = config.get('SQLStatement', None)
        srcOpenOptions = config.get('srcOpenOptions',
                                ['AUTODETECT_TYPE=NO',
                                'EMPTY_STRING_AS_NULL=YES'])
        newFieldNames = config.get('newFieldNames', [])

        # initiate destination
        dstDS = gdal.OpenEx(self.engine, gdal.OF_VECTOR)

        # initiate source
        path = path.replace('ftp:/', self.ftp_prefix)
        path = path.replace('FTP_PREFIX', self.ftp_prefix) # for backward compatibility

        srcDS = Archiver.load_srcDS(path, srcOpenOptions, 
                                    newFieldNames, 
                                    self.s3_endpoint, 
                                    self.s3_secret_access_key, 
                                    self.s3_access_key_id)

        originalLayerName = srcDS.GetLayer().GetName()
        
        # check on schema
        dstDS.ExecuteSQL(f'CREATE SCHEMA IF NOT EXISTS {schema_name};')
        
        version = datetime.today().strftime("%Y/%m/%d") if version_name == '' else version_name
        layerName = f'{schema_name}.{version}'

        print(f'\nArchiving {layerName} to recipes...')
        gdal.VectorTranslate(
            dstDS,
            srcDS,
            SQLStatement=SQLStatement.replace(schema_name, originalLayerName) if SQLStatement else None,
            format='PostgreSQL',
            layerCreationOptions=layerCreationOptions,
            dstSRS=dstSRS,
            srcSRS=srcSRS,
            geometryType=geometryType,
            layerName=layerName,
            accessMode='overwrite',
            callback=gdal.TermProgress)

        # tag version as latest
        print(f'\nTagging {layerName} as {schema_name}.latest ...')

        try: 
            dstDS.ExecuteSQL(f'''
            DROP VIEW IF EXISTS {schema_name}.latest;
            ''')
        except: 
            pass

        try:
            dstDS.ExecuteSQL(f'''
            DROP TABLE IF EXISTS {schema_name}.latest;
            ''')
        except: 
            pass

        dstDS.ExecuteSQL(f'''
        CREATE VIEW {schema_name}.latest as (SELECT \'{version}\' as v, * from {schema_name}."{version}");
        ''')
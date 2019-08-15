import os
from osgeo import ogr
from osgeo import gdal
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
from sqlalchemy import engine

class Exporter():
    def __init__(self,
                engine='env://RECIPE_ENGINE'):

        if engine.startswith('env://'):
            env_var = engine[6:]
            engine = os.environ.get(env_var)
            if engine is None:
                raise ValueError("Couldn't connect to DB - "
                                 "Please set your '%s' environment variable" % env_var)

        self.engine = self.parse_engine(engine)
        self.ftp_prefix=os.environ.get('FTP_PREFIX', '')

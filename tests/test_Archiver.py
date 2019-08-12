def test_dump_to_archive():
    from cook import Archiver
    import os
    engine = os.environ.get('RECIPE_ENGINE', '')

    importer = Importer(engine=engine)

    archiver.dump_to_archive(config={
        'schema_name': 'parks_properties',
        'path': 'https://data.cityofnewyork.us/api/geospatial/k2ya-ucmv?method=export&format=GeoJSON', 
        'geometryType':'MULTIPOLYGON',
        'srcSRS':'EPSG:4326',
        'dstSRS':'EPSG:4326',
        'layerCreationOptions':['OVERWRITE=YES'],
        })
        
test_dump_to_archive()
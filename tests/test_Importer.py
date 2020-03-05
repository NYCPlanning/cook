def test_import():
    from cook import Importer
    import os
    RECIPE_ENGINE = os.environ.get('RECIPE_ENGINE', '')
    BUILD_ENGINE=os.environ.get('BUILD_ENGINE', '')
    importer = Importer(RECIPE_ENGINE, BUILD_ENGINE)
    importer.import_table(schema_name='test')

def test_import_expert():
    from cook import Importer
    import os
    RECIPE_ENGINE = os.environ.get('RECIPE_ENGINE', '')
    BUILD_ENGINE=os.environ.get('BUILD_ENGINE', '')
    importer = Importer(RECIPE_ENGINE, BUILD_ENGINE)
    importer.import_table_expert(schema_name='test', version='latest', 
                            target_schema_name='public', target_version='test2')
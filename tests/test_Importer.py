def test_import_1():
    from cook import Importer
    import os
    RECIPE_ENGINE = os.environ.get('RECIPE_ENGINE', '')
    BUILD_ENGINE=os.environ.get('BUILD_ENGINE', '')

    importer = Importer(RECIPE_ENGINE, BUILD_ENGINE)
    importer.import_table(schema_name='parks_properties')

def test_import_2():
    from cook import Importer
    import os
    RECIPE_ENGINE = os.environ.get('EDM_DATA', '')
    BUILD_ENGINE=os.environ.get('BUILD_ENGINE', '')

    importer = Importer(RECIPE_ENGINE, BUILD_ENGINE)
    importer.import_table(schema_name='facilities', version='latest')
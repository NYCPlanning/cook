def test_import_to_build():
    from cook import Importer
    import os
    RECIPE_ENGINE = os.environ.get('RECIPE_ENGINE', '')
    BUILD_ENGINE=os.environ.get('BUILD_ENGINE', '')

    importer = Importer(RECIPE_ENGINE, BUILD_ENGINE)
    importer.import_to_build(schema_name='parks_properties')

test_import_to_build()
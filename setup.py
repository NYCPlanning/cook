from setuptools import setup, find_packages

setup(name='cook',
      version='0.1',
      description='cooking...',
      author='Baiyue Cao',
      author_email='caobaiyue@gmail.com',
      license='MIT',
      pacakges=find_packages(),
      install_requires=[
            'click',
            'psycopg2-binary',
            'sqlalchemy',
            'pytest',
            'shapely', 
            'usaddress', 
            'bs4']
      )
FROM osgeo/gdal:ubuntu-small-latest

RUN apt update\
    && apt install -y\
        git\
        python3-pip\
        postgresql-client-common\
        postgresql-client-10

COPY . /home/cook/

WORKDIR /home/cook/

RUN pip3 install -e .
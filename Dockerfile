FROM osgeo/gdal:ubuntu-small-latest

ENV DEBIAN_FRONTEND=noninteractive

COPY . /home/cook/

WORKDIR /home/cook/

RUN ./setup.sh

RUN pip3 install -e .

WORKDIR /
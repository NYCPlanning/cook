FROM osgeo/gdal:ubuntu-small-latest

RUN apt install -y\
        git\
        python3-pip

COPY . /home/cook/

WORKDIR /home/cook/

RUN pip3 install -e .
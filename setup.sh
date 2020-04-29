#!/bin/bash
apt update
apt install -y curl zip python3-pip

tee /etc/apt/sources.list.d/pgdg.list <<END
deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main
END
# get the signing key and import it
curl -O https://www.postgresql.org/media/keys/ACCC4CF8.asc
apt-key add ACCC4CF8.asc

apt update
apt install -y postgresql-client-11 postgis
apt autoremove
rm ACCC4CF8.asc
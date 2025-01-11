#!/bin/bash

docker volume create kf2ds_magicked
docker volume create kf2ds_overrides
docker volume create kf2ds_webserver

sudo chown 1000:1000 /var/lib/docker/volumes/kf2ds_magicked/_data/ \
                /var/lib/docker/volumes/kf2ds_overrides/_data/ \
                /var/lib/docker/volumes/kf2ds_webserver/_data/

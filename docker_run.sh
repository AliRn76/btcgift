#!/bin/bash

docker run \
-p 75:75 \
--name btcgift \
--volume /srv/btcgift/media:/app/media \
--volume /srv/btcgift/static:/app/static \
--restart always \
-d \
btcgift:v1
docker logs -f btcgift

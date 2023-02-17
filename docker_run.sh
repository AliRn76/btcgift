#!/bin/bash

docker run \
-p 75:75 \
--name btcgift \
--volume /srv/btcgift/media:/app/media \
--volume /srv/btcgift/static:/app/static \
--volume /srv/btcgift/logs:/app/logs \
--restart always \
-d \
btcgift:v1

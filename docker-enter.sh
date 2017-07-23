#!/bin/bash

sudo docker rm -f better-steam-se
sudo docker run -it \
                --name better-steam-se \
                --volume $PWD:/data/repo \
                imhuwq/better-steam-se /bin/bash

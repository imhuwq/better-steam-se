#!/usr/bin/env bash

if [ "$1" == "build" ]
then
    sudo docker build -t imhuwq/better-steam-se .
fi

if [ "$1" == "enter" ]
then
    sudo docker rm -f better-steam-se
    sudo docker run -it \
                    --volume $PWD:/data/repo \
                    --name better-steam-se \
                    --link redis \
                    imhuwq/better-steam-se /bin/bash
fi

if [ "$1" == "pip" ]
then
    if [ "$2" == "uninstall" ]
    then
        cmd="pip $2 -y ${@:3} ; pip freeze > requirements.txt"
    else
        cmd="pip ${@:2} ; pip freeze > requirements.txt"
    fi
    sudo docker rm -f better-steam-se
    sudo docker run --volume $PWD:/data/repo \
                    --name better-steam-se \
                    imhuwq/better-steam-se /bin/bash -c "$cmd"

    sudo docker build -t imhuwq/better-steam-se .
fi

if [ "$1" == "logs" ]
then
    docker-compose logs -f --tail 10 ${@:2}
fi

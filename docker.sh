#!/usr/bin/env bash

if [ "$1" == "build" ]; then
    docker build -t imhuwq/better-steam-se .

elif [ "$1" == "enter" ]; then
    docker rm -f better-steam-se
    docker run -it \
                    --volume $PWD:/data/repo \
                    --name better-steam-se \
                    --link redis \
                    imhuwq/better-steam-se /bin/bash

elif [ "$1" == "pip" ]; then
    if [ "$2" == "uninstall" ]; then
        cmd="pip $2 -y ${@:3} ; pip freeze > requirements.txt"
    else
        cmd="pip ${@:2} ; pip freeze > requirements.txt"
    fi
    docker rm -f better-steam-se
    docker run --volume $PWD:/data/repo \
                    --name better-steam-se \
                    imhuwq/better-steam-se /bin/bash -c "$cmd"

    docker build -t imhuwq/better-steam-se .

elif [ "$1" == "compose" ]; then
     if [ "$2" == "logs" ]; then
        docker-compose logs -f --tail 10 ${@:3}
    else
        docker-compose ${@:2}
    fi
fi

#!/bin/bash

# Проверяем, запущен ли Docker
if ! systemctl is-active --quiet docker; then
    echo "Запускаем Docker демон..."
    sudo systemctl start docker
    sleep 2
fi

# Проверяем, запущен ли уже SearXNG
if ! docker ps | grep -q searxng; then
    echo "Запускаем SearXNG..."
    cd ~/searxng-docker
    docker-compose up -d
fi

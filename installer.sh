#!/bin/bash
if [ "$(id -u)" -ne 0 ]; then
  echo "Скрипт должен запускаться от имени root пользователя"
  exit 1
fi
#Обязательная установка git
sudo pacman -S git

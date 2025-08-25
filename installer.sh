#!/bin/bash
#Проверка на root
if [ "$(id -u)" -ne 0 ]; then
  echo "Скрипт должен запускаться от имени root пользователя"
  exit 1
fi

#Переменные для упрощения
user="${SUDO_USER:-$USER}"
user_home=$(eval echo ~"$user")

#Обязательная установка git
sudo pacman -S git --noconfirm

#Копирование репозитория
if [ -d "$user_home/myrice" ]; then
  rm -rf "$user_home/myrice"
fi
sudo -u $(logname) mkdir "$user_home/myrice"
sudo -u $(logname) git clone https://github.com/makaYtech/myrice "$user_home/myrice"

#Запуск установки yay
chmod +x $user_home/myrice/yayinstall.sh
sudo -u "$user" bash "$user_home/myrice/yayinstall.sh"

#Копирование конфигов
directories=("hypr" "gtk-3.0" "mako" "kitty" "nvim" "waybar" "wofi")

source_dir="$user_home/myrice"

for dir in "${directories[@]}"; do
  target="$user_home/.config/$dir"
  source="$source_dir/$dir"

  if [ -d "$target" ]; then
    rm -rf "${target:?}/"*
    cp -r "$source/." "$target"
    echo "Обновлена директория: $dir"
  else
    cp -r "$source" "$target"
    echo "Создана и скопирована директория: $dir"
  fi
done

#Запуск установки пакетов
chmod +x $user_home/myrice/pacmaninstall.sh
bash "$user_home/myrice/pacmaninstall.sh"

echo "Done!"

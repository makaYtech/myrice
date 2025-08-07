#!/bin/bash
echo "Установка yay"
if command -v yay &>/dev/null; then
  echo "yay уже существует"
  exit 0
fi

if [ -d "$HOME/yay" ]; then
  echo "Директоря yay уже существует. Будет осуществлена попытка установки из неё"
  cd "$HOME/yay"

  if makepkg -si; then
    echo "yay был установлен из существующей директории"
    exit 0
  else
    echo "Неудалось установить из существующей директории. Yay будет установлен с нуля"
  fi
fi
cd "$HOME" || exit 1
git clone https://aur.archlinux.org/yay.git
cd yay || exit 1
makepkg -si

if command -v yay &>/dev/null; then
  echo "yay успешно установлен"
else
  echo "установка yay не удалась" >&2
  exit 1
fi

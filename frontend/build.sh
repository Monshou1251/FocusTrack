#!/bin/sh
# Скрипт для сборки с чтением переменных из .env

if [ -f .env ]; then
  set -a
  . .env
  set +a
fi

npm run build



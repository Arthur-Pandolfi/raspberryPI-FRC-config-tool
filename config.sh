#!/bin/bash

# Variáveis para armazenar os valores das flags
type=""

# Processa as opções
while getopts t: opt; do
  case $opt in
    t)
      type=$OPTARG
      ;;
    *)
      echo "Uso: $0 -t <total|network>"
      exit 1
      ;;
  esac
done

if [ "$type" = "total" ]; then
    cd /home
    sudo python3 -m frc_os.main --type total
elif [ "$type" = "network" ]; then
    cd /home
    sudo python3 -m frc_os.main --type network
else
    echo "Invalid option, use -t total to config all things or -t network to setup network settings"

fi

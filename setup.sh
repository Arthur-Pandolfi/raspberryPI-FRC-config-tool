#!/bin/bash

type=""

while getopts t: opt; do
  case $opt in
    t)
      type=$OPTARG
      ;;
    *)
      echo "Use: $0 -t <total|network>"
      exit 1
      ;;
  esac
done

if [ "$type" = "total" ]; then
  cd ..
    sudo python -m frc_os.setup --type total
elif [ "$type" = "network" ]; then
    sudo python -m frc_os.setup --type total
else
    echo "Invalid option, use -t total to config all things or -t network to setup network settings"

fi

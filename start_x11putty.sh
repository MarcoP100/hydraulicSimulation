#!/bin/bash

if [ -z "$DISPLAY" ]
then
    echo "La variabile DISPLAY non è impostata. Uscita."
    exit 1
fi

echo "DISPLAY ok"

tail -f /dev/null
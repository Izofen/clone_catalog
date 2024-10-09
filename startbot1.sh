#!/bin/sh
i=1
cd /home/izofen/Main/clone
while [ "$i" -le 11500 ]; do
    python3 clone_catalog.py -m 1
    i=$(( i + 1 ))
done







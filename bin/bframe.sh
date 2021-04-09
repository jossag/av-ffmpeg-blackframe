#!/bin/sh

INPUT=$1
BFRAME_OUTPUT="bframe_output.txt"

echo 'Input file:' $1

ffmpeg -hide_banner -nostats -loglevel info -i $INPUT -vf blackdetect=d=1:pix_th=0.00 -f rawvideo -y /dev/null > $BFRAME_OUTPUT 2>&1
./parse_bframe.py

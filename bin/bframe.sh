#!/bin/sh -e

INPUT="$1"
BFRAME_OUTPUT="bframe_output.txt"

# Black frame parameters, see https://ffmpeg.org/ffmpeg-all.html#blackdetect
DURATION=1
PIC_TH=0.98
PIX_TH=0.10

echo 'Input file:' $INPUT
ffmpeg -hide_banner -nostats -loglevel info -i "$INPUT" -vf blackdetect=d=$DURATION:pic_th=$PIC_TH:pix_th=$PIX_TH -f rawvideo -y /dev/null 2>&1 | tee $BFRAME_OUTPUT

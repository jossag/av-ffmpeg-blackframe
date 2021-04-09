# FFmpeg black frame detection for Accurate.Video


```
fmpeg -hide_banner -nostats -loglevel info -i Sintel.2010.720p.mkv -vf blackdetect=d=2:pix_th=0.00 -f rawvideo -y /dev/null > bframe_output.txt 2>&1
```


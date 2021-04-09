# FFmpeg black frame detection for Accurate.Video

Integration to use FFmpeg for black frame detection during ingest in Accurate.Video using a custom ingest template.

## blackdetect

Using the blackdetect video filter in FFmpeg.  
https://ffmpeg.org/ffmpeg-all.html#blackdetect

### Usage

```
fmpeg -i input -vf blackdetect=d=1:pic_th=0.98:pix_th=0.10 -f rawvideo -y /dev/null
```

### Parameters

`black_min_duration, d`  
Set the minimum detected black duration expressed in seconds. Default value is 2.0.

`picture_black_ratio_th, pic_th`  
Set the threshold for considering a picture "black". Default value is 0.98.

`pixel_black_th, pix_th`  
Set the threshold for considering a pixel "black". Default value is 0.10.

## Parsing

Python script `bin/parse_bframe.py` parses FFmpeg output and transforms into Accurate.Video timespan format.

### Example

Output from FFmpeg:

```
[blackdetect @ 0x55e3ac098840] black_start:0 black_end:3.625 black_duration:3.625
```

Converted JSON timespan:
```json
[
  {
    "type": "Black_Frame",
    "startSeconds": "0",
    "endSeconds": "3.625",
    "metadata": [
      {
        "key": "name",
        "value": "Black frame"
      },
      {
        "key": "description",
        "value": "Duration: 3.625 seconds"
      },
      {
        "key": "subtype",
        "value": "av:track:video:black_frame"
      }
    ]
  }
]
```

## Ingest template






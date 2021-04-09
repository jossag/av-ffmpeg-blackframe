# FFmpeg black frame detection for Accurate.Video

Integration to use FFmpeg for black frame detection during ingest in Accurate.Video using a custom ingest template. Using the blackdetect video filter in FFmpeg it's easy to detect video intervals that are (almost) completely black. This is useful to detect chapter transitions, commercials, or invalid recordings, and this example shows a complete integration on how to integrate this with Accurate.Video for visualization in the timeline.

## FFmpeg blackdetect

Refer to the blackdetect filter in the FFmpeg docs for more details.  
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

### Script

A convenient bash-script in `bin/bframe.sh` can be used with the video input file as argument. This script redirects the output from FFmpeg into a file called `bframe_output.txt` which is later parsed and converted to json. 

## Parsing

A Python script `bin/parse_bframe.py` parses the FFmpeg output and transforms it into Accurate.Video timespan format.

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

The default video ingest template is replaced with `partials/video_ingest.j2.json` to include three `SHELL` jobs:

```json
{
  "type": "SHELL",
  "metadata": [
    {
      "key": "command",
      "value": "/usr/local/bin/bframe.sh"
    },
    {
      "key": "command",
      "value": "${target_path_export}"
    }
  ]
},
{
  "type": "SHELL",
  "metadata": [
    {
      "key": "command",
      "value": "/usr/local/bin/parse_bframe.py"
    }
  ]
},
{
  "type": "SHELL",
  "metadata": [
    {
      "key": "command",
      "value": "/usr/local/bin/import_timespan.sh"
    },
    {
      "key": "command",
      "value": "{{metadata.target_asset_id}}"
    }
  ]
},
```

The `SHELL` commands executes the following:

* `bframe.sh <file_name>` - runs FFmpeg on asset video file
* `parse_bframe.py` - parses FFmpeg output and converts into timespan format
* `import_timespans.sh <asset_id>` - ingests timespans onto asset

## Configure timeline

```json
  markers: {
    groups: [
      {
        match: marker => marker && marker.type === "Black_Frame",
        title: "Black frames",
        id: "blackFrame",
        readOnly: true,
        alwaysShow: false,
        trackType: "Black_Frame",
        rows: [
          {
            match: (marker, track) =>
              !!marker?.metadata.get("trackId") || !!track,
            track: (marker, track) => track.id,
            title: (marker, track) => track?.metadata.get("name"),
            tooltip: ({ metadata }) => metadata.get("description")
            order: (marker, track) => parseInt(track?.id, 10) ?? 4,
            markerType: "Black_Frame",
            alwaysShow: false
          }
        ]
      },
    ],
  },
```

# Black frame detection using FFmpeg in Accurate.Video

This repository contains an integration to use FFmpeg to detect video intervals that are (almost) completely black, 
commonly referred to as black frame detection. This detection is described using custom job templates, which are 
configured to run during ingest, but on-demand execution is possible too. Visualization of black intervals in the 
video is done by configuring the Accurate.Video timeline. This is useful for QC operators performing validation of 
content to highlight and suggest chapter transitions, commercials, or invalid recordings. 

## FFmpeg blackdetect

There is a video filter to FFmpeg called blackdetect which can be used specifically for this use case. The filter will
run an analysis on each frame in a video, defined by some parameters which can be set. For every matching interval 
found that is within the minimum duration, a line is printed to the normal log output with the start, end, and duration 
of the interval in seconds.

Sample output:
```
[blackdetect @ 0x564caad3d380] black_start:0 black_end:3.625 black_duration:3.625
[blackdetect @ 0x564caad3d380] black_start:101.208 black_end:104.083 black_duration:2.875
[blackdetect @ 0x564caad3d380] black_start:146.542 black_end:150.583 black_duration:4.041
[blackdetect @ 0x564caad3d380] black_start:435.458 black_end:438 black_duration:2.542
[blackdetect @ 0x564caad3d380] black_start:676.792 black_end:680.708 black_duration:3.916
[blackdetect @ 0x564caad3d380] black_start:744.083 black_end:756.75 black_duration:12.667
[blackdetect @ 0x564caad3d380] black_start:756.833 black_end:774.708 black_duration:17.875
[blackdetect @ 0x564caad3d380] black_start:781.333 black_end:784.917 black_duration:3.584
```

### Usage

Refer to the blackdetect filter in the FFmpeg docs for more details on usage.  
https://ffmpeg.org/ffmpeg-all.html#blackdetect

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

A convenient bash-script in `bin/bframe.sh` can be used with the video input file as argument. This script redirects 
the output from FFmpeg into a file called `bframe_output.txt`, which can be parsed in a later stage. 

## Parsing

A Python script `bin/parse_bframe.py` parses the FFmpeg output and transforms it into Accurate.Video timespan format.

Here is an example for a single black frame interval. Each interval will result in many blocks of JSON like this.

FFmpeg output:
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

The default video ingest template from Accurate.Video is used, but three additional steps have been added which all
execute `SHELL` type tasks. 

The following tasks are run at the end of the template:

* `bframe.sh <file_name>` - runs FFmpeg on asset video file
* `parse_bframe.py` - parses FFmpeg output and converts into timespan format
* `import_timespans.sh <asset_id>` - ingests timespans onto asset

Note: there is no need to run the first and third tasks as bash scripts, the commands can be included directly in the 
template if so preferred. Using a custom script just makes it easier to manage and test.

Below are the three additional commands being added to the video ingest template. The full template can be found in
`partials/video_ingest.j2.json`.

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

## Configure timeline

The Accurate.Video timeline needs to be configured to show the black frame metadata. This is as simple as including
the following section in your configuration:

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

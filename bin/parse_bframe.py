#!/usr/bin/env python3

import re
import json

rx_dict = {
    'bframe': re.compile(
        '\[blackdetect @ .*\] black_start:(?P<start>.*) black_end:(?P<end>.*) black_duration:(?P<duration>.*)'),
}

BFRAME_OUTPUT_FILE = 'bframe_output.txt'
TIMESPANS_FILE = 'timespans.json'
AV_TYPE = 'Black_Frame'
AV_SUBTYPE = 'av:track:video:black_frame'


def parse_line(line):
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None


def create_metadata(key, value):
    obj = {'key': key, 'value': value}
    return obj


def create_bframe(start, end, duration, metadata):
    obj = {'type': AV_TYPE, 'startSeconds': start, 'endSeconds': end, 'metadata': metadata}
    return obj


def parse_file(filepath):
    metadata = []

    with open(filepath, 'r') as file_object:
        for line in file_object:
            key, match = parse_line(line)

            if key == 'bframe':
                start = match.group('start')
                end = match.group('end')
                duration = match.group('duration')

                name = create_metadata('name', 'Black frame')
                description = create_metadata('description', 'Duration: ' + duration + ' seconds')
                subtype = create_metadata('subtype', AV_SUBTYPE)
                bframe = create_bframe(start, end, duration, [name, description, subtype])
                metadata.append(bframe)

    return metadata


def write_json(file, json):
    with open(file, 'w') as file_object:
        file_object.write(json)


if __name__ == '__main__':
    data = parse_file(BFRAME_OUTPUT_FILE)
    json = json.dumps(data, indent=2)
    write_json(TIMESPANS_FILE, json)

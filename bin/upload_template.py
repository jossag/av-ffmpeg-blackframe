#!/usr/bin/env python3

import json
import sys
import requests
from requests.auth import HTTPBasicAuth

def create_template_body(name, filename):
    with open(filename) as f:
        content = f.read()

    escaped_file = json.dumps(content)

    obj = {
        'type': 'av_job_template',
        'metadata': [{
            'key': 'value',
            'value': name
        }],
        'blob': escaped_file
    }

    return obj


def post_template(url, body, user, password):
    response = requests.post(url + '/api/settings', data=body, headers={'Content-Type': 'application/json'},
                             auth=HTTPBasicAuth(user, "=k'E$FJm2k|;76_U"))
    print(response.status_code)
    print(response.json())
    print(response.text)


# ./upload_template.py 'partials/video_ingest' 'parse_bframe.py' 'https://av.jonas.cmtest.se' 'admin' 'uZJhUc6QW5bMBqK9'
if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('Syntax:', sys.argv[0], '<template name> <script name> <base api url> <user> <password>')
        exit(-1)

    template_name = sys.argv[1]
    script_name = sys.argv[2]
    url = sys.argv[3]
    user = sys.argv[4]
    password = sys.argv[5]

    template = create_template_body(template_name, script_name)
    json = json.dumps(template, indent=2)
    sys.stdout.write(json + '\n')
    post_template(url, json, user, password)

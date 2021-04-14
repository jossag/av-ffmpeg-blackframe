#!/usr/bin/env python3

import json
import sys
import requests
from requests.auth import HTTPBasicAuth

def create_template(type, name, filename):
    with open(filename) as f:
        content = f.read()

    escaped_file = json.dumps(content)

    obj = {
        'type': type,
        'metadata': [{
            'key': 'value',
            'value': name
        }],
        'blob': escaped_file
    }

    return obj


def post_template(url, body, user, password):
    response = requests.post(url + '/api/settings', data=body, headers={'Content-Type': 'application/json'},
                             auth=HTTPBasicAuth(user, password))
    print(response.status_code)
    print(response.json())
    print(response.text)

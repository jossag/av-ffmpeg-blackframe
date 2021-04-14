#!/usr/bin/env python3

import json
import sys
import requests
from requests.auth import HTTPBasicAuth
from upload_common import create_template, post_template

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Syntax:', sys.argv[0], '<script name> <base api url> <user> <password>')
        exit(-1)

    script_name = sys.argv[1]
    url = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]

    template = create_template('av_runner_script', script_name, script_name)
    json = json.dumps(template, indent=2)
    sys.stdout.write(json + '\n')
    post_template(url, json, user, password)

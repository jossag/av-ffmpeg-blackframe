#!/usr/bin/env python3

import json
import sys
import requests
from requests.auth import HTTPBasicAuth
from upload_common import create_template, post_template

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('Syntax:', sys.argv[0], '<template name> <template filename> <base api url> <user> <password>')
        exit(-1)

    template_name = sys.argv[1]
    template_file = sys.argv[2]
    url = sys.argv[3]
    user = sys.argv[4]
    password = sys.argv[5]

    template = create_template('av_job_template', template_name, template_file)
    json = json.dumps(template, indent=2)
    sys.stdout.write(json + '\n')
    post_template(url, json, user, password)

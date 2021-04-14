#!/bin/sh -e

echo "Importing black frame timespans for asset $1"
cat timespans.json
curl -X POST "${AP_ADAPTER_URL_MP_REST_URL}/asset/$1/timespan/bulk"  -u "${AP_ADAPTER_USERNAME}:${AP_ADAPTER_PASSWORD}"  -H 'Content-Type: application/json' -d @timespans.json

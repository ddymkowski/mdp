#!/bin/bash

DATA_PATH="$(pwd)/data.csv"
SCHEMA='{"comment": "String", "dob": "Date","sales": "Float32"}'
LOADER_KWARGS='{"separator":";"}'
FORMATTER='json'

plmdp --path "$DATA_PATH" --schema="$SCHEMA" --kwargs="$LOADER_KWARGS" --format="$FORMATTER"

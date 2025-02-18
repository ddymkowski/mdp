#!/bin/bash

# Define variables for better readability
DATA_PATH="$(pwd)/data.csv"
SCHEMA='{"comment": "String", "dob": "Date","sales": "Float32"}'
LOADER_KWARGS='{"separator":";"}'
FORMATTER='json'

# Run dq command with prettify option
dq --path "$DATA_PATH" --schema="$SCHEMA" --kwargs="$LOADER_KWARGS" --format="$FORMATTER"
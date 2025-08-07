#!/bin/bash

# Detect Python3 path; fallback to system python3
PYTHON=${PYTHON:-python3}

# Set working directory to the script's directory
cd "$(dirname "$0")"

# Run slashcode.py with Python 3
$PYTHON ./slashcode.py "$@"

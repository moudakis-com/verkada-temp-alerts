#!/bin/bash

docker build -t verkada-temp-alert .

docker run -d --name verkada-alert \
  -v "$(pwd)/.env:/app/.env:ro" \
  verkada-temp-alert
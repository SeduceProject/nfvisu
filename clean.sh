#!/bin/bash
if [ -z "$1" ]; then
  echo "Keep old JSON files"
  rm -rf  nfvisu/index.html nfvisu/tools \
    backend/index.html backend/json/*.json backend/tools/*.html backend/tools/json/*.json
else
  echo "Delete all files"
  rm -rf  nfvisu/index.html nfvisu/tools \
    backend/index.html backend/json/*.json backend/tools/*.html backend/tools/json/*.json \
    backend/old_json/*.json
fi

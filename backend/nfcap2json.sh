#!/bin/bash

NFCAP_DIR="/tmp/nfcap-data"
JSON_DIR="old_json"
JSON_NEW_DIR="json"

json_fix=""
# Read the nfcap files with nfdump
for f in $(find $NFCAP_DIR -type f ! -name "*current*"); do
  json_file=$(echo $f | tr -dc [0-9]).json
  if [ ! -e $JSON_DIR/$json_file ]; then
    json_fix=$f
    echo $f
    nfdump -r $f -o json > $json_file
  fi
done

if [ ! -z "$json_fix" ]; then
  # Fix the JSON files to be read by python
  for f in $(ls *.json); do
    head -n -6 $f | sed 's/}/},/' > $f.done
    echo "{\"nfdump\": [" > $JSON_NEW_DIR/$f
    cat $f.done >> $JSON_NEW_DIR/$f
    echo "}" >> $JSON_NEW_DIR/$f
    echo "] }" >> $JSON_NEW_DIR/$f
    rm $f*
  done
  cp $JSON_NEW_DIR/*.json $JSON_DIR
fi

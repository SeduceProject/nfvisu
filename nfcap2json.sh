#!/bin/bash

NFCAP_DIR="/tmp/nfcap-data"
JSON_DIR="json"
HTML_DIR="tools"
WWW_DIR="/var/www/html"
KEEP_NB=500

# Too many files, delete the oldest ones
if [ $(find $NFCAP_DIR -name "nfcapd.20*" | wc -l) -gt $(( $KEEP_NB + 50 )) ]; then
  # Delete old files to keep only $KEEP_NB files
  echo "Delete the oldest nfcapd files"
  find $NFCAP_DIR -maxdepth 1 -name "nfcapd.20*" | sort | head -n -$KEEP_NB | xargs -d '\n' -r rm --
  find $JSON_DIR -maxdepth 1 -name "*.json" | sort | head -n -$KEEP_NB | xargs -d '\n' -r rm --
  find $HTML_DIR -maxdepth 1 -name "20*" | sort | head -n -$KEEP_NB | xargs -d '\n' -r rm --
  find $WWW_DIR -maxdepth 1 -name "20*" | sort | head -n -$KEEP_NB | xargs -d '\n' -r rm -r --
fi

# Read the nfcap files with nfdump
json_fix=""
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
    if [ $(cat $f | wc -l) -gt 6 ]; then
      head -n -6 $f | sed 's/}/},/' > $f.done
      echo "{\"nfdump\": [" > $JSON_DIR/$f
      cat $f.done >> $JSON_DIR/$f
      echo "}" >> $JSON_DIR/$f
      echo "] }" >> $JSON_DIR/$f
      rm $f*
    else
      rm $NFCAP_DIR/nfcapd.$(basename $f .json)
    fi
  done
fi

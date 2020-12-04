#!/bin/bash

JSON_DIR="json"
HTML_DIR="tools"
WWW_DIR="/var/www/html/nfvisu"
WWW_USER="www-data"

# Generate the HTML page for the connection graph
for f in $(find $JSON_DIR -type f -name '*.json'); do
  number=$(echo $f | tr -dc [0-9])
  html_file="$HTML_DIR/graph-$number.html"
  cp graph.html $html_file
  sed -i "s:JSONDATA:json/connections-$number.json:" $html_file
done

cp index.html $WWW_DIR
cp -r $HTML_DIR $WWW_DIR
chown $WWW_USER.$WWW_USER -R $WWW_DIR
rm -f $JSON_DIR/*.json

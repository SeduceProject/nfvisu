#!/bin/bash

HTML_DIR="tools"
# WARNING: If you modify this variable, update the Javascript and CSS path in jinja2 templates
WWW_DIR="/var/www/html/"
WWW_USER="www-data"

# Create the web directory
if [ ! -d $WWW_DIR ]; then
  mkdir $WWW_DIR
fi

# Copy the history HTML page
cp $HTML_DIR/history.html $WWW_DIR

# Copy the Javascript files
if [ ! -d $WWW_DIR/js ]; then
  cp -r $HTML_DIR/js $WWW_DIR
fi

# Copy the CSS files
if [ ! -d $WWW_DIR/css ]; then
  cp -r $HTML_DIR/css $WWW_DIR
fi

for dir in $(find $HTML_DIR -maxdepth 1 -name "20*" | sort); do
  dirname=$(basename $dir)
  if [ ! -d $WWW_DIR/$dirname ]; then
    echo $dir
    cp -r $dir $WWW_DIR
  fi
done

# Copy the last index.html as the global index.html
cp $dir/index.html $WWW_DIR/
chown $WWW_USER.$WWW_USER -R $WWW_DIR

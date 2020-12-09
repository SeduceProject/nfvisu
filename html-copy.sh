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
mv $HTML_DIR/history.html $WWW_DIR/history.html

# Copy the Javascript files
if [ ! -d $WWW_DIR/js ]; then
  cp -r $HTML_DIR/js $WWW_DIR/js
fi

# Copy the CSS files
if [ ! -d $WWW_DIR/css ]; then
  cp -r $HTML_DIR/css $WWW_DIR/css
fi

for dir in $(find $HTML_DIR -maxdepth 1 -name "20*" | sort); do
  dirname=$(basename $dir)
  if [ ! -d $WWW_DIR/$dirname ]; then
    echo $dir
    mv $dir $WWW_DIR/$dirname
    # Create a file to tell python the directory has been processed
    touch $dir
  fi
done

# Copy the last index.html as the global index.html
cp $WWW_DIR/$dirname/index.html $WWW_DIR/index.html

sed -i '/REFRESH /a \    window.setInterval(refreshIndexHTML, 5000);' $WWW_DIR/index.html
chown $WWW_USER.$WWW_USER -R $WWW_DIR

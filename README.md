# nfvisu
Simple web interface to visualize NetFlow data

## Packages
The packages are installed on a Debian 10 AMD64.
```
apt install git lighttpd nfdump python3 python3-pip screen vim
pip3 install jinja2
```

## Capture the NefFlow data
* We put the NetFlow data in */tmp*. The files will be deleted on reboot.
```
mkdir /tmp/nfcap-data
screen
[enter]
nfcapd -w -E -t 180 -p 9001 -l /tmp/nfcap-data
[ctrl-a] then [ctrl-d]
# To attach to the screen session
screen -r
```

## Configure NFvisu
* Clone the repository
```
git clone http://github.com/remyimt/nfvisu
cd nfvisu
```
* Edit the file *nfcap2json.sh*
  * Set the *NFCAP_DIR* variable with the nfcapd output directory (the -l option)
* Edit the file *html-copy.sh*
  * Set the *WWW_USER* to your WWW user (default: *www-data*)
* Add the crontab rule: `crontab -e`
```
*/3 * * * * cd /root/nfvisu/; sleep 10; python3 site-generator.py
```
* As *nfcapd* generates one file every 3 minutes (180 s, the -t option),
  the *site-generator.py* script is run every 3 minutes.
* By default, NFvisu keeps the 500 most recent nfcapd files. With 3-minutes periods, the tools keeps 24 hours of data.
  * Adjust the number of files to keep in `nfcap2json.sh` by setting the *KEEP_NB* variable

## Move NFvisu to a specific directory
If you do not want to install the NFvisu interface in the root of your HTTP server, you have to specify the new path in
all scripts. In the following example, you install the NFvisu interface to */var/www/html/nfvisu/*.
* nfcap2json.sh
  * Set `WWW_DIR` to */var/www/html/nfvisu* (without the trailing slash)
* nfcap2json.sh
  * Set `WWW_DIR` to */var/www/html/nfvisu* (without the trailing slash)
* templates/host.jinja2.html
  * Set the path to `datatables.css` to */nfvisu/css/datatables.css*
  * Set the path to `jquery-3.5.1.min.js` to */nfvisu/js/jquery-3.5.1.min.js*
  * Set the path to `jquery.dataTables.js` to */nfvisu/js/jquery.dataTables.js*
* templates/summary.jinja2.html
  * Set the path to `datatables.css` to */nfvisu/css/datatables.css*
  * Set the path to `graph.css` to */nfvisu/css/graph.css*
  * Set the path to `history.html` to */nfvisu/history.html*
  * Set the path to the `host pages` to */nfvisu/%s/host/%s.html* instead of */%s/host/%s.html*
  * Set the path to `jquery-3.5.1.min.js` to */nfvisu/js/jquery-3.5.1.min.js*
  * Set the path to `jquery.dataTables.js` to */nfvisu/js/jquery.dataTables.js*
  * Set the path to `d3.v4.min.js` to */nfvisu/js/d3.v4.min.js*
  * Set the path to `graph.js` to */nfvisu/js/graph.js*
  * Set the path to `nfvisu.js` to */nfvisu/js/nfvisu.js*
  * Set the path to `graph.json` to */nfvisu/{{ date_nb }}/graph.json*

## Screenshots
For every monitoring period (3-minutes period in the default configuration), the main page shows a graph with the connection between hosts and summarizes the NetFlow data in a table with one row per host.
![main page for a specific period](screenshots/connection-graph.png =800x)
By clicking on the host, more information about its connections are presented in a table.
![detailed information about host connections](screenshots/detailed-connections.png =800x)

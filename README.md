# nfvisu
Simple script to visualize NetFlow data

## Packages
The packages are installed on a Debian 10 ADM64.
```
apt install nfdump nfcapd python3 screen vim lighttpd git
```

## Capture the NefFlow data
* We put the NetFlow data in */tmp*. The files will be deleted on reboot.
```
screen
[enter]
nfcapd -w -E -t 180 -p 9001 -l /tmp/nfcap-data
[ctrl-a] then [ctrl-d]
# To attach to the screen session
screen -r
```

## Configure NFvisu interface
* Copy the *nfvisu*  folder to */var/www/html*
```
git clone http://github.com/remyimt/nfvisu
cd nfvisu
cp -r nfvisu /var/www/html
```

## Configure NFvisu backend
* Edit the file *nfcap2json.sh*
  * Set the *NFCAP_DIR* variable with the nfcapd output directory (the -l option)
* Add the crontab rule: `crontab -e`
```
*/3 * * * * cd /root/nfvisu/nfvisu-backend; sleep 10; python3 site-generator.py
```
* As *nfcapd* generates one file every 3 minutes (180 s, the -t option),
  the *site-generator.py* script is run every 3 minutes.

from glob import glob
import json, os, subprocess, shutil, sys

# Functions
def proto(nb):
    if nb == 1:
        return "ICMP"
    if nb == 6:
        return "TCP"
    if nb == 17:
        return "UDP"
    return str(nb)


def tr_write(fd, data, prop):
    if prop in data:
        if prop == "proto":
            fd.write("    <td>%s</td>\n" % proto(data[prop]))
        else:
            fd.write("    <td>%s</td>\n" % data[prop])
    else:
        fd.write("    <td>-</td>\n")

# Constants
JSON_DIR="json"
OLD_JSON_DIR="old_json"
GRAPH_DIR="tools/json"
HTML_DIR="tools"
HEADER_HTML="header.html"
FOOTER_HTML="footer.html"
INDEX_HTML_ORG="index.html.org"
INDEX_HTML="index.html"
# HTML page for the tables
html_file=""

# main()
subprocess.call("./nfcap2json.sh")
# Initialize the index.html file
shutil.copy(INDEX_HTML_ORG, INDEX_HTML)
# Read nfdump JSON files
for json_file in glob("%s/*.json" % JSON_DIR):
    connections = {}
    print(json_file)
    with open(json_file, "r") as jsonfd:
        data = json.load(jsonfd)["nfdump"]
    html_file = os.path.basename(json_file).replace('json', 'html')
    html_file = "%s/table-%s" % (HTML_DIR, html_file)
    print(html_file)
    shutil.copy(HEADER_HTML, html_file)
    with open(html_file, "a") as htmltxt:
        for flow in data:
            if "src4_addr" in flow and "dst4_addr" in flow:
                # Generate the HTML table
                htmltxt.write("  <tr>\n")
                tr_write(htmltxt, flow, "src4_addr")
                tr_write(htmltxt, flow, "src_port")
                tr_write(htmltxt, flow, "dst4_addr")
                tr_write(htmltxt, flow, "dst_port")
                tr_write(htmltxt, flow, "proto")
                tr_write(htmltxt, flow, "in_bytes")
                htmltxt.write("  </tr>\n")
                if flow["src4_addr"] not in [ "0.0.0.0" ]:
                    # Generate the graph of connections
                    src_ip = flow["src4_addr"].replace('.', '_')
                    dst_ip = flow["dst4_addr"].replace('.', '_')
                    if src_ip not in connections:
                        connections[src_ip] = []
                    if dst_ip not in connections:
                        connections[dst_ip] = []
                    if dst_ip not in connections[src_ip] and src_ip not in connections[dst_ip]:
                        connections[src_ip].append(dst_ip)
        # Append the HTML footer
        with open(FOOTER_HTML, "r") as footer:
            htmltxt.write(footer.read())
    # Write the JSON file for the connections
    flare = []
    for node in connections:
        flare.append({ "name": node, "imports": connections[node]})
    with open("%s/connections-%s" % (GRAPH_DIR, os.path.basename(json_file)), "w") as flarefile:
        json.dump(flare, flarefile, indent=4)

if html_file:
    with open(INDEX_HTML, "a") as index:
        for json_file in sorted(glob("%s/*.json" % OLD_JSON_DIR), reverse=True):
            date_nb = os.path.basename(json_file).replace(".json", "")
            date_str = "%s-%s-%s %sh%s" % (date_nb[0:4], date_nb[4:6], date_nb[6:8], date_nb[8:10], date_nb[10:12])
            index.write("     <b>%s</b><br/>\n" % date_str)
            index.write("     <a href='%s'>table</a> / " % html_file)
            index.write("     <a href='%s'>graph</a><br/>\n" % html_file.replace("table", "graph"))
        index.write("  </body>\n")
        index.write("</html>")
    # Move the files to the WWW directory (HTTP server)
    subprocess.call("./last-step.sh")

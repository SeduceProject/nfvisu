from glob import glob
import jinja2, json, os, subprocess, shutil, sys

# Functions
def proto(nb):
    if nb == 1:
        return "ICMP"
    if nb == 6:
        return "TCP"
    if nb == 17:
        return "UDP"
    return str(nb)


# Jinja2 loader
templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
templateEnv = jinja2.Environment(loader=templateLoader)


# Constants
JSON_DIR="json"
OLD_JSON_DIR="old_json"
HTML_DIR="tools"


# main()
# Read nfcapd data with nfdump
subprocess.call("./nfcap2json.sh")
# Dates with different formats to generate the history.html file
date_fmt = []
# Read nfdump JSON files
json_files = glob("%s/*.json" % JSON_DIR)
for json_file in json_files:
    # Format the date of the data
    date_nb = os.path.basename(json_file).split('.')[0]
    date_str = "%s-%s-%s %sh%s" % (date_nb[0:4], date_nb[4:6], date_nb[6:8], date_nb[8:10], date_nb[10:12])
    date_fmt.append({ "nb": date_nb, "str": date_str })
    # Create the data directory
    data_dir = "%s/%s" % (HTML_DIR, date_nb)
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
        os.mkdir("%s/host" % data_dir)
        # Organize the NetFlow data
        connections = {}
        print(json_file)
        with open(json_file, "r") as jsonfd:
            data = json.load(jsonfd)["nfdump"]
        for flow in data:
            if "src4_addr" in flow and "dst4_addr" in flow:
                src = flow["src4_addr"]
                dst = flow["dst4_addr"]
                if "src_port" in flow:
                    src_port = flow["src_port"]
                else:
                    src_port = -1
                if "dst_port" in flow:
                    dst_port = flow["dst_port"]
                else:
                    dst_port = -1
                if src not in connections:
                    connections[src] = {
                        "out": [], "out_port": [], "out_ip": [],
                        "in": [], "in_port": [], "in_ip": [],
                        "transmitted": 0, "received": 0
                    }
                if dst not in connections:
                    connections[dst] = {
                        "out": [], "out_port": [], "out_ip": [],
                        "in": [], "in_port": [], "in_ip": [],
                        "transmitted": 0, "received": 0
                    }
                # Outcoming connections
                connections[src]["out"].append({ "src_port": src_port, "dst": dst, "dst_port": dst_port,
                    "proto": proto(flow["proto"]), "size": flow["in_bytes"]})
                if src_port not in connections[src]["out_port"]:
                    connections[src]["out_port"].append(src_port)
                if dst not in connections[src]["out_ip"]:
                    connections[src]["out_ip"].append(dst)
                connections[src]["transmitted"] += flow["in_bytes"]
                # Incoming connections
                connections[dst]["in"].append({ "src": src, "src_port": src_port, "dst_port": dst_port,
                    "proto": proto(flow["proto"]), "size": flow["in_bytes"]})
                connections[dst]["received"] += flow["in_bytes"]
                if dst_port not in connections[dst]["in_port"]:
                    connections[dst]["in_port"].append(dst_port)
                if src not in connections[dst]["in_ip"]:
                    connections[dst]["in_ip"].append(src)
        # JSON files to generate connection graphs
        flare = []
        for c in connections:
            flare.append({
                "name": c.replace('.', '_'), 
                "imports": [ip.replace('.', '_') for ip in connections[c]["out_ip"]]
            })
        with open("%s/graph.json" % data_dir, "w") as  flarefile:
            json.dump(flare, flarefile, indent=4)
        # Summary HTML pages
        summary_file = os.path.basename(json_file).replace('json', 'html')
        summary_file = "%s/summary-%s" % (data_dir, summary_file)
        template = templateEnv.get_template("summary.jinja2.html")
        outputText = template.render(
            date_str = date_str,
            date_nb = date_nb,
            summary = connections
        )
        with open("%s/index.html" % data_dir, "w") as summary:
            summary.write(outputText)
        # Host connection HTML pages
        template = templateEnv.get_template("host.jinja2.html")
        for conn in connections:
            # NetFlow data for this host
            outputText = template.render(
                hostip = conn,
                datenb = date_nb,
                outcoming = connections[conn]["out"],
                outports = [str(c) for c in sorted(connections[conn]["out_port"])],
                outips = [str(c) for c in sorted(connections[conn]["out_ip"])],
                incoming = connections[conn]["in"],
                inports = [str(c) for c in sorted(connections[conn]["in_port"])],
                inips = [str(c) for c in sorted(connections[conn]["in_ip"])],
            )
            with open("%s/host/%s.html" % (data_dir, conn.replace(".", "_")), "w") as host:
                host.write(outputText)
# Sort the dates
date_fmt = sorted(date_fmt, key = lambda d: d['nb'], reverse=True)
# History HTML page: one link per monitoring period
template = templateEnv.get_template("history.jinja2.html")
outputText = template.render(
        dates = date_fmt
)
with open("%s/history.html" % HTML_DIR, "w") as history:
    history.write(outputText)
# Move the files to the WWW directory (HTTP server)
subprocess.call("./last-step.sh")

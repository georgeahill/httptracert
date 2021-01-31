from flask import Flask, render_template, request, jsonify
import traceroute

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/paths")
def paths():
    ip_addr = request.args.get("ip")

    print(f"Requested {ip_addr}")

    hops = traceroute.run_traceroute(ip_addr)

    features = []

    j = 0

    for i in range(len(hops) - 1):
        hop = hops[i]
        next_hop = hops[i+1]
        if hop[0] == 'Not found' or next_hop[0] == 'Not found' or (next_hop[1] == hop[1] and next_hop[2] == hop[2]):
            continue
        j += 1
        coordinates = [[hop[1], hop[2]], [next_hop[1], next_hop[2]], [hop[1], hop[2]]]
        feature = {
            "type": "Feature",
            "properties": {
                "name": str(j)
            },
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates
            }
        }

        features.append(feature)

    return_obj = {"hops": len(hops), "type": "FeatureCollection", "features": features}

    return jsonify(return_obj)
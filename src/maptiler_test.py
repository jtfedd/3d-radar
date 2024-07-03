import sys

import requests

from lib.model.location import Location

print(sys.argv)

query = " ".join(sys.argv[1:])

HOST = "https://api.maptiler.com"
KEY = "9brhhxnhHsxtWEw4LSuI"

params = {
    "key": KEY,
    "autocomplete": "false",
    "country": "us",
    "fuzzyMatch": "false",
}

url = HOST + "/geocoding/" + query + ".json"

response = requests.get(
    url,
    params=params,
    timeout=10,
)
response.raise_for_status()

responseJson = response.json()
for location in responseJson["features"]:
    context = {}
    if "context" in location:
        for c in location["context"]:
            t = c["id"].split(".")[0]
            context[t] = c["text"]

    addressParts = []
    areaParts = []

    if "address" in location and "text" in location:
        addressParts.append(f"{location["address"]} {location["text"]}")
    elif "text" in location:
        addressParts.append(location["text"])
    if "municipality" in context:
        areaParts.append(context["municipality"])
    if "joint_municipality" in context:
        areaParts.append(context["joint_municipality"])
    if "region" in context:
        areaParts.append(context["region"])
    
    addr = ", ".join(addressParts)
    area = ", ".join(areaParts)

    if "postal_code" in context:
        area = " ".join([area, context["postal_code"]])

    loc = Location(
        addr,
        area,
        float(location["center"][1]),
        float(location["center"][0])
    )

    print(loc.getLabel())

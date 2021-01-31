import os
import requests
import icmplib


def get_ip_location(ip_addr: str) -> tuple:
    response = requests.get(f"https://geolocation-db.com/json/{ip_addr}")
    location_data = response.json()
    return location_data["IPv4"], location_data["longitude"], location_data["latitude"]


def run_traceroute(address: str) -> list:
    hops = icmplib.traceroute(address)

    return [get_ip_location(hop.address) for hop in hops]

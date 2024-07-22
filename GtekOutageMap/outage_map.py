from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
import requests
from GtekOutageMap.db import get_db
import os

bp = Blueprint('outage_map', __name__)

@bp.route('/')
def map():
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    return render_template('outage_map.html', google_maps_api_key=google_maps_api_key)

@bp.route('/find_outage', methods=['POST'])
def find_outage():
    data = request.get_json()
    if not data or 'placeId' not in data:
        return jsonify({"message": "Invalid request, placeId is required."}), 400

    place_id = data['placeId']
    
    # Get latitude and longitude of the placeId
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?place_id={place_id}&key=' + google_maps_api_key
    geocode_response = requests.get(geocode_url).json()
    
    if geocode_response['status'] != 'OK':
        return jsonify({"message": "Error geocoding placeId."}), 400
    
    location = geocode_response['results'][0]['geometry']['location']
    address_lat_lng = (location['lat'], location['lng'])
    
    db = get_db()
    towers = db.execute(
        'SELECT name, longitude, latitude, radius, status FROM towers'
    ).fetchall()

    an_offline_tower = None

    for tower in towers:
        if tower['status'] == 'offline':
            tower_lat_lng = (tower['latitude'], tower['longitude'])
            distance_to_tower = haversine_distance(address_lat_lng, tower_lat_lng)
            MAXTOWERDISTANCE = 24140 #15 miles, in meters
            if distance_to_tower <= MAXTOWERDISTANCE and distance_to_tower <= tower['radius'] * 1609.34:
                an_offline_tower = {
                    'name': tower['name'],
                    'distance': distance_to_tower
                }
                break
    
    if an_offline_tower:
        title = "Outage Reported"
        message = f"""You appear to be in an outage. Rest assured, our technicians are working hard to get all services back up and running as soon as possible.
        
        
        DEBUG An Offline Tower is in Radius: {an_offline_tower['name']}, Distance: {(an_offline_tower['distance']/1609.34):.2f} miles.
        """
    else:
        title = "No Outage Reported"
        message = "We aren't aware of any issues at your location. Try troubleshooting on your own [insert troubleshooting tips], or contact us at 361-777-1400."

    return jsonify({"title": title, "message": message, "markerPosition": location})

def haversine_distance(loc1, loc2):
    from math import radians, sin, cos, sqrt, atan2

    R = 6371.0  # Earth radius in kilometers

    lat1, lon1 = loc1
    lat2, lon2 = loc2

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c * 1000  # Convert to meters
    return distance

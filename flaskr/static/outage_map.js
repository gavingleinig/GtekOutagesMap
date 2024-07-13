let map;
let geocoder;
let gridPoints = [];
let marker;

document.addEventListener("DOMContentLoaded", async function () {
    await initMap();
    await loadTowers();
});

async function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 9,
        center: { lat: 28.090881958, lng:  -97.68847870 }, // Center of Gtek Service Area
        fullscreenControl: false,
        disableDefaultUI: true,
        zoomControl: true,
        mapTypeControl: false,
        scaleControl: true,
        streetViewControl: false,
        rotateControl: false,
        mapTypeId: 'terrain'
    });
    geocoder = new google.maps.Geocoder();

}

async function loadTowers() {
    const response = await fetch('/data');
    const data = await response.json();
    towers = data.towers;
}

async function findIfOutage() {
    const address = document.getElementById("address").value;
    const nearestPointElement = document.getElementById("nearest-point");

    // Function to get latitude and longitude of an address using Google Maps Geocoding API
    const geocodeAddress = async (address) => {
        const geocoder = new google.maps.Geocoder();
        return new Promise((resolve, reject) => {
            geocoder.geocode({ address: address }, (results, status) => {
                if (status === 'OK') {
                    resolve(results[0].geometry.location);
                } else {
                    reject(`Geocode was not successful for the following reason: ${status}`);
                }
            });
        });
    };

    try {
        const addressLocation = await geocodeAddress(address);
        const addressLatLng = new google.maps.LatLng(addressLocation.lat(), addressLocation.lng());

        // Center and zoom the map on the given address
        map.setCenter(addressLatLng);
        map.setZoom(12);

        if (marker) {
            marker.setMap(null);
        }

        marker = new google.maps.Marker({
            position: addressLatLng,
            map: map,
            title: 'Address Location'
        });

        let anOfflineTower = null;

        towers.forEach(tower => {
            if (tower.status == 'Offline') {
                const towerLatLng = new google.maps.LatLng(tower.latitude, tower.longitude);
                const distanceToTower = google.maps.geometry.spherical.computeDistanceBetween(addressLatLng, towerLatLng);

                if (distanceToTower <= 16093.4) { // 10 miles in meters
                    if (distanceToTower <= tower.radius*1609.34) {
                        
                            anOfflineTower = {
                                name: tower.name,
                                distance: distanceToTower
                            };
                        
                    }
                }
            }
        });

        if (anOfflineTower) {
            nearestPointElement.innerText = `An Offline Tower is in Radius: ${anOfflineTower.name}, Distance: ${(anOfflineTower.distance/1609.34).toFixed(2)} miles`;
        } else {
            nearestPointElement.innerText = "All systems are good to go.";
        }

    } catch (error) {
        console.error(error);
        nearestPointElement.innerText = "Error determining outage status.";
    }
}

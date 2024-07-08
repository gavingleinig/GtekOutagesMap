let map;
let geocoder;
let gridPoints = [];

document.addEventListener("DOMContentLoaded", async function () {
    await initMap();
    await loadPoints();
});

async function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 9,
        center: { lat: 28.090881958, lng:  -97.68847870 } // Center of the US
    });
    geocoder = new google.maps.Geocoder();

}

async function loadPoints() {
    const response = await fetch('/data');
    const data = await response.json();
    gridPoints = data.towers;
}

async function findNearestPoint() {
    const address = document.getElementById("address").value;
    geocoder.geocode({ address: address }, (results, status) => {
        if (status === "OK") {
            const location = results[0].geometry.location;
            map.setCenter(location);
            map.setZoom(10);

            const { nearestPoint, distance } = getNearestPoint(location);
            document.getElementById("nearest-point").innerText = `Nearest Point: ${nearestPoint.name}, Distance: ${distance.toFixed(2)} meters`;
            
            new google.maps.Marker({
                map: map,
                position: location,
                title: 'Given Address'
            });

            new google.maps.Marker({
                map: map,
                position: { lat: nearestPoint.lat, lng: nearestPoint.lng },
                title: nearestPoint.name
            });

        } else {
            alert("Geocode was not successful for the following reason: " + status);
        }
    });
}

function getNearestPoint(location) {
    let nearestPoint = null;
    let minDistance = Number.MAX_VALUE;
    let distance = 0;
    
    gridPoints.forEach(point => {
        const pointLocation = new google.maps.LatLng(point.latitude, point.longitude);
        const currentDistance = google.maps.geometry.spherical.computeDistanceBetween(location, pointLocation);
        if (currentDistance < minDistance) {
            minDistance = currentDistance;
            nearestPoint = point;
            distance = currentDistance;
        }
    });

    return { nearestPoint, distance };
}
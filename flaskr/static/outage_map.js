let map;
let geocoder;
let gridPoints = [];

document.addEventListener("DOMContentLoaded", async function () {
    await initMap();
    await loadTowers();
});

async function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 9,
        center: { lat: 28.090881958, lng:  -97.68847870 } // Center of the US
    });
    geocoder = new google.maps.Geocoder();

}

async function loadTowers() {
    const response = await fetch('/data');
    const data = await response.json();
    towers = data.towers;
}

function findNearestPoint() {
    const address = document.getElementById("address").value;
    geocoder.geocode({ address: address }, (results, status) => {
        if (status === "OK") {
            const location = results[0].geometry.location;
            map.setCenter(location);
            map.setZoom(12);

            const towersInRange = getTowersInRange(location);
            const offlineTowers = towersInRange.filter(tower => tower.status == "Offline");

            if (offlineTowers.length > 0) {
                const nearestOfflineTower = findNearestTower(location, offlineTowers);
                document.getElementById("nearest-point").innerText = `Nearest Offline Tower: ${nearestOfflineTower.name}, Distance: ${nearestOfflineTower.distance.toFixed(2)} meters`;
            } else {
                document.getElementById("nearest-point").innerText = "All systems are good to go.";
            }

            new google.maps.Marker({
                map: map,
                position: location,
                title: 'Given Address'
            });

            towersInRange.forEach(tower => {
                new google.maps.Marker({
                    map: map,
                    position: { lat: tower.latitude, lng: tower.longitude },
                    title: tower.name
                });
            });

        } else {
            alert("Geocode was not successful for the following reason: " + status);
        }
    });
}

function getTowersInRange(location) {
    return towers.filter(tower => {
        const towerLocation = new google.maps.LatLng(tower.latitude, tower.longitude);
        const distance = google.maps.geometry.spherical.computeDistanceBetween(location, towerLocation);
        return distance <= tower.radius*1609.34; //1609.34 meters in a mile
    });
}

function findNearestTower(location, towers) {
    let nearestTower = null;
    let minDistance = Number.MAX_VALUE;

    towers.forEach(tower => {
        const towerLocation = new google.maps.LatLng(tower.latitude, tower.longitude);
        const currentDistance = google.maps.geometry.spherical.computeDistanceBetween(location, towerLocation);
        if (currentDistance < minDistance) {
            minDistance = currentDistance;
            nearestTower = tower;
        }
    });

    return { name: nearestTower.name, distance: minDistance };
}
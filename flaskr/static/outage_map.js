let map;
let geocoder;
let gridPoints = [];
let marker;

document.addEventListener("DOMContentLoaded", async function () {
    await initMap();
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

async function findIfOutage() {
    const address = document.getElementById("address").value;
    const nearestPointElement = document.getElementById("nearest-point");

    try {
        const response = await fetch('/find_outage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ address: address })
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Error: ${response.status} - ${errorText}`);
        }

        const result = await response.json();

        nearestPointElement.innerText = result.message;

        if (result.markerPosition) {
            const addressLatLng = new google.maps.LatLng(result.markerPosition.lat, result.markerPosition.lng);
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
        }
    } catch (error) {
        console.error(error);
        nearestPointElement.innerText = "Error determining outage status.";
    }
}

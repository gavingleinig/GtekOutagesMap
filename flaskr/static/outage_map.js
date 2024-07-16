let map;
let marker;

document.addEventListener("DOMContentLoaded", async function () {
    await initMap();
    await initAutocomplete();
    await findIfOutage();
});

async function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 9,
        center: { lat: 28.090881958, lng: -97.68847870 }, // Center of Gtek Service Area
        fullscreenControl: false,
        disableDefaultUI: true,
        zoomControl: true,
        mapTypeControl: false,
        scaleControl: true,
        streetViewControl: false,
        rotateControl: false,
        mapTypeId: 'terrain',
        gestureHandling: "greedy"
    });
    marker = new google.maps.Marker({
        map,
        anchorPoint: new google.maps.Point(28, -97.68),
    });
    marker.setVisible(false);
}

async function initAutocomplete() {
    const defaultBounds = {
        north: 29.975,
        south: 26.925,
        east: -96.125,
        west: -98.925,
    };
    const options = {
        bounds: defaultBounds,
        componentRestrictions: { country: "us" },
        strictBounds: false,
    };
}

async function findIfOutage() {
    const autocompleteInput = document.getElementById("autocomplete");
    const nearestPointElement = document.getElementById("nearest-point");
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const autocomplete = new google.maps.places.Autocomplete(autocompleteInput, {});

    google.maps.event.addListener(autocomplete, 'place_changed', async function () {
        const place = autocomplete.getPlace();
        if (!place || !place.place_id) {
            nearestPointElement.innerText = "Please select a valid place from the suggestions.";
            return;
        }
        
        map.setCenter(place.geometry.location);
        map.setZoom(14);
        marker.setPosition(place.geometry.location);
        marker.setVisible(true);

        try {
            const response = await fetch('/find_outage', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ placeId: place.place_id })
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Error: ${response.status} - ${errorText}`);
            }

            const result = await response.json();
            nearestPointElement.innerText = result.message;
        } catch (error) {
            console.error(error);
            nearestPointElement.innerText = "Error determining outage status.";
        }
    });
}

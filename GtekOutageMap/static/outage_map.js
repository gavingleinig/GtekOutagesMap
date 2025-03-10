let map;
let marker;
let selectedPlace = null;

document.addEventListener("DOMContentLoaded", async function () {
    await initMap();
    await initAutocomplete();
});


async function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 8,
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
    const autocompleteInput = document.getElementById("autocomplete");
    const feedbackElement = document.getElementById("autocompleteFeedback");
    const autocomplete = new google.maps.places.Autocomplete(autocompleteInput, {
        bounds: {
            north: 29.975,
            south: 26.925,
            east: -96.125,
            west: -98.925,
        },
        componentRestrictions: { country: "us" },
        strictBounds: false,
    });

    google.maps.event.addListener(autocomplete, 'place_changed', function () {
        const place = autocomplete.getPlace();
        if (!place || !place.geometry) {
            autocompleteInput.classList.add("is-invalid");
            feedbackElement.style.display = "block";
            return;
        }

        autocompleteInput.classList.remove("is-invalid");
        feedbackElement.style.display = "none";

        selectedPlace = place;
        map.setCenter(place.geometry.location);
        map.setZoom(14);
        marker.setPosition(place.geometry.location);
        marker.setVisible(true);
    });
}




async function findIfOutage() {
    const responseMessage = document.getElementById("info-text");
    const responseTitle = document.getElementById("info-title");
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const autocompleteInput = document.getElementById("autocomplete");
    const feedbackElement = document.getElementById("autocompleteFeedback");

    // Reset validation state
    autocompleteInput.classList.remove("is-invalid");
    feedbackElement.style.display = "none";

    if (!selectedPlace || !selectedPlace.place_id) {
        autocompleteInput.classList.add("is-invalid");
        feedbackElement.style.display = "block";
        return;
    }

    try {
        const response = await fetch('/find_outage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ placeId: selectedPlace.place_id })
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Error: ${response.status} - ${errorText}`);
        }

        const result = await response.json();
        responseMessage.innerHTML = result.message;
        responseTitle.innerText = result.title;

    } catch (error) {
        console.error(error);
        responseMessage.innerText = "There was an issue determining outage status.";
    }

    document.getElementById("map").style.display = "none";
    document.getElementById("search-button").style.display = "none";
    document.getElementById("autocomplete").style.display = "none";
    responseTitle.style.display = "block";
}
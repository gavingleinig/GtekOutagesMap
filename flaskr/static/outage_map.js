let map;
let geocoder;
let gridPoints = [];
let marker;
var csrf_token = "{{ csrf_token() }}";

document.addEventListener("DOMContentLoaded", async function () {
    await initMap();
    await initAutocomplete();
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

async function initAutocomplete() {
    var autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('autocomplete'), {
        types: ['geocode']
      });
  
    autocomplete.addListener('place_changed', function() {
      var place = autocomplete.getPlace();
      if (!place.geometry) {
        window.alert("Autocomplete's returned place contains no geometry");
        return;
      }
  
      // If you need to use the selected place, you can access it here
      var address = place.formatted_address;
      console.log("Selected Address:", address);
    });
  }

  async function findIfOutage() {
    const autocompleteInput = document.getElementById("autocomplete");
    const nearestPointElement = document.getElementById("nearest-point");

    // Retrieve the CSRF token from the meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    try {
        // Create a new Places Autocomplete instance
        const autocomplete = new google.maps.places.Autocomplete(autocompleteInput, {
            types: ['geocode']  // Optional: Restrict autocomplete to addresses only
        });

        // Listen for the place_changed event on the Autocomplete instance
        google.maps.event.addListener(autocomplete, 'place_changed', async function() {
            const place = autocomplete.getPlace();  // Retrieve the selected place
            if (!place || !place.place_id) {
                throw new Error("Please select a valid place from the suggestions.");
            }

            const response = await fetch('/find_outage', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Include the CSRF token in the headers
                },
                body: JSON.stringify({ placeId: place.place_id })
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Error: ${response.status} - ${errorText}`);
            }

            const result = await response.json();

            nearestPointElement.innerText = result.message;

            // Optional: Update map and markers if necessary
            // ...

        });
    } catch (error) {
        console.error(error);
        nearestPointElement.innerText = "Error determining outage status.";
    }
}
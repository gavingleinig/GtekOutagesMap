let map;
let marker;
let selectedPlace = null;

document.addEventListener("DOMContentLoaded", async function () {
    await initMap();
});

async function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 7,
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
    var towerData = JSON.parse(document.getElementById("map").getAttribute("data-bs-towers"));

    for (var tower of towerData) {
        var stroke = '#af0500';
        var fill = '#fd0700';
        if (tower.status == 'online') {
            stroke = '#4ef30c';
            fill = '#2ea200';
        }

        if (tower.status == 'offline') {
            stroke = '#FFBE00';
            fill = '#FFDC00';
        }

        var contentString = '<div id="content">' +
        '<div id="siteNotice">' +
        '</div>' +
        '<h2 id="firstHeading" class="firstHeading">' +
        tower.name +
        '</h2>' +
        '<div id="bodyContent">' +
        '<p>' +
        'Location: (' + tower.latitude.toFixed(4) + ', ' + tower.longitude.toFixed(4) + ')' +
        '</p>' +
        '<p>' +
        'Radius: ' + (tower.radius).toFixed(2) + ' miles' 
        '</p>' +
        '<p>' +
        'Status: ' + tower.status +
        '</p>' +
        '</div>' +
        '</div>';

        (function (tower, stroke, fill, contentString) {
            var infowindow = new google.maps.InfoWindow({
                content: contentString
            });

            var cityCircle = new google.maps.Circle({
                strokeColor: stroke,
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: fill,
                fillOpacity: 0.35,
                map: map,
                center: { lat: tower.latitude, lng: tower.longitude },
                radius: tower.radius * 1609.34
            });

            cityCircle.addListener('click', function () {
                infowindow.setPosition(cityCircle.getCenter());
                infowindow.open(map);
            });
        })(tower, stroke, fill, contentString);
    }
}

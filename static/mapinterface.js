// Maths to make bearing arrows work, and maybe other cool stuff I haven't
// thought of yet, who knows?
function degreesToRadians (degrees) {
    return degrees * (Math.PI / 180);
}

function radiansToDegrees (radians) {
    return radians / (Math.PI / 180);
}

// Calculate the forward azimuth (great circle bearing) between two latlngs
function findBearing (latlng1, latlng2) {
    var p1 = degreesToRadians(latlng1.lat);
    var p2 = degreesToRadians(latlng2.lat);
    var l1 = degreesToRadians(latlng1.lng);
    var l2 = degreesToRadians(latlng2.lng);

    var y = Math.sin(l2 - l1) * Math.cos(p2);
    var x = Math.cos(p1) * Math.sin(p2) -
            Math.sin(p1) * Math.cos(p2) * Math.cos(l2 - l1);
    var bearing = Math.atan2(y, x);

    return radiansToDegrees(bearing);
}


function objectValues(obj) {
    var vals = Object.keys(obj).map(function(key) {
        return obj[key];
    });
    return vals;
}

// This is wrapped in a self-executing function which returns the actual
// function so I can have private scope to hold the previousMarker var.
var addMarker = (function() {

    // This is used to save a reference to the previous marker, so I can
    // set it back to its unhighlighted state.
    var previousMarker;

    // The unhighlighted appearance of the markers
    var defaultIcon = {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 4,
        strokeColor: 'red'
    }

    // The highlighted appearance of the markers
    var focusIcon = {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 6,
        strokeColor: 'yellow'
    }

    return function(map, id, latlng) {

        var marker = new google.maps.Marker({
            position: latlng,
            map: map,
            entry_id: id,
            icon: defaultIcon,

            setHighlight: function() {
                this.setIcon(focusIcon);
            },

            unsetHighlight: function() {
                this.setIcon(defaultIcon);
            }
        });

        // The URL to query server for the next 10 entries
        var url = '/entries/query/?count=10&eid=' + marker.entry_id;

        // Define the behaviour for when user clicks on a marker
        google.maps.event.addListener(marker, 'click', function() {
            // Unset the highlight on the previous marker, if there is a
            // previous marker
            if (previousMarker) {
                previousMarker.unsetHighlight();
            }
            // Change the colour of the marker to highlight it
            marker.setHighlight();
            $.get(url, function(response) {
                var viewer = $('#entry_box');
                viewer.empty();
                viewer.append(response);
                viewer.animate({scrollTop: 0});
            });
            previousMarker = marker;
        });
    };
})();

function initialise()
{
    var options = {
        // This should be centered on the first location marker
        center: { lat: -50.7, lng: 166.1},
        zoom: 6,
        mapTypeId: 'satellite'
    };

    var map = new google.maps.Map(document.getElementById('map_box'), options);

    $.getJSON('/all-positions', function(response) {
        // Center the map on the first entry received
        first = Object.keys(response)[0];
        map.setCenter(response[first]);
        // Create the location markers
        $.each(response, function(id, latlng) {
            addMarker(map, id, latlng);
        });
        // Draw a line between the markers
        var line = new google.maps.Polyline({
            path: objectValues(response),
            geodesic: true,
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 1
        });
        line.setMap(map);
    });
}

google.maps.event.addDomListener(window, 'load', initialise);

$(document).ready(function () {
    // Fill the entry viewer with the first ten entries
    var url = '/entries/query/?count=10';
    $.get(url, function(response) {
        $('#entry_box').append(response);
    });
    // Automatically load the next 10 entries when the user scrolls to the
    // bottom of the entry viewer
    $('#entry_box').scroll(function() {
        if ($(this).scrollTop() + $(this).innerHeight() >= this.scrollHeight) {
            // Get the ID of the last entry in the viewer
            // Consider making the ID a property in the div tag to avoid below
            var lastEntryDiv = $(this).children().last();
            var lastDate = lastEntryDiv.children('.date_field').text();
            var url = '/entries/query/?count=10&start_date=' + lastDate;
            $.get(url, function(response) {
                $('#entry_box').append(response);
                // Scroll back to the top
                $(this).scrollTop(0);
            });
        }
    });
});

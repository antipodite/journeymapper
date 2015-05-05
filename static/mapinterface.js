function objectValues(obj) {
    var vals = Object.keys(obj).map(function(key) {
        return obj[key];
    });
    return vals;
}

function addMarker(map, id, latlng) {
    var marker = new google.maps.Marker({
        position: latlng,
        map: map,
        entry_id: id,
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 5,
            strokeColor: 'red'
        }
    });
    google.maps.event.addListener(marker, 'click', function() {
        var url = '/entries/query/?count=10&eid=' + marker.entry_id;
        $.get(url, function(response) {
            $('#entry_box').empty();
            $('#entry_box').append(response);
            $('#entry_box').animate({
                scrollTop: 0
            });
        });
    });
}

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
    // bottom of the entry viewer (WIP)
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

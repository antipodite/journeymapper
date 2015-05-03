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
        var url = '/entry-text/' + marker.entry_id;
        $.getJSON(url, function(response) {
            $('#date_field').text(response.date);
            $('#lat_field').text(response.lat);
            $('#lng_field').text(response.lng);
            $('#entry_field').text(response.text);
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
    // Load the first 10 journal entry into the entry viewer when the page loads
    // Need to change the HTML so the entry viewer can handle multiple entries
    $.getJSON('/get-many-entries/10', function(response) {
        $.each(response, function(date, lat, lng, text) {
            $('#date_field').text(date);
            $('#lat_field').text(lat);
            $('#lng_field').text(lng);
            $('#entry_field').text(text);
        });
    });
    // Bind the `scroll` event handler to the entry viewer
    $('#entry_box').scroll(function() {
        console.log('Scroll event handler called');
    });
});

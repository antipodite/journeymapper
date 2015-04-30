function addMarker(map, id, latlng) {
    var marker = new google.maps.Marker({
        position: latlng,
        map: map,
        entry_id: id
    });
    google.maps.event.addListener(marker, 'click', function() {
        var url = '/entry-text/' + marker.entry_id;
        $('#entrybox').load(url);
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
    var map = new google.maps.Map(document.getElementById('mapbox'), options);

    // Request the entries from the JSON entries view and make loc markers
    $.getJSON('/all-positions', function(response) {
        var first = Object.keys(response)[0] // Deal with it nerds
        map.setCenter(response[first]);
        $.each(response, function(id, latlng) {
            if (latlng.lat && latlng.lng) {
                addMarker(map, id, latlng);
            }
        });
    });
}

google.maps.event.addDomListener(window, 'load', initialise);

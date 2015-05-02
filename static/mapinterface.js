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
            console.log(response);
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
    console.log(map);

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

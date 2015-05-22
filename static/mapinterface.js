/* Helper functions */
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

var MapViewer = (function () {

    var map;
    var markers = [];
    var minMarkerVisZoom = 5;
    var markersVisible = true;
    var entryViewer;

    var options = {
        center: { lat: -50.7, lng: 166.1},
        zoom: 6,
        mapTypeId: 'satellite',
        panControl: false,
        scaleControl: true,
        streetViewControl: false
    };

    var initialise = function (elem, entryViewerObj) {

        map = new google.maps.Map(elem, options);
        entryViewer = entryViewerObj;
        console.log(entryViewer);

        $.getJSON('/all-positions', function(response) {
            // Center the map on the first entry received
            first = Object.keys(response)[0];
            map.setCenter(response[first]);
            // Create the location markers
            $.each(response, function(id, latlng) {
                var m = addMarker(id, latlng);
                markers.push(m);
            });
            drawJourneyRoute(objectValues(response));
        });

        // Toggle marker visibility on zoom out
        google.maps.event.addListener(map, 'zoom_changed', toggleMarkerVisOnZoomChange);
    };

    var drawJourneyRoute = function (latlngs) {
        var line = new google.maps.Polyline({
            path: latlngs,
            geodesic: true,
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 1
        });
        line.setMap(map);
    };

    var addMarker = (function() {
        // Save previous clicked marker for unhighlight
        var previousClickedMarker;

        // Save previously created marker during initialisation for bearing
        var previousCreatedMarkerPos;

        // The unhighlighted appearance of the markers
        var defaultIcon = {
            path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
            scale: 4,
            strokeColor: 'red',
            strokeWeight: 1,

            setRotation: function (degrees) {
                this.rotation = degrees;
            }
        }

        // The highlighted appearance of the markers
        var focusIcon = {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 6,
            strokeColor: 'yellow',
            strokeWeight: 3,

            setRotation: function (degrees) {
                this.rotation = degrees;
            }
        }

        return function(id, latlng) {

            // Calculate the bearing _from_ the previous marker _to_ this marker
            // If no previous marker, circle instead of arrow?
            var bearing = 0;
            if (previousCreatedMarkerPos) {
                bearing = findBearing(previousCreatedMarkerPos, latlng);
            }

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
            marker.icon.setRotation(bearing);

            // Remember this marker for bearing calculation
            previousCreatedMarkerPos = latlng;

            // The URL to query server for the next 10 entries
            var url = '/entries/query/?count=10&eid=' + marker.entry_id;

            // Define the behaviour for when user clicks on a marker
            google.maps.event.addListener(marker, 'click', function() {
                // Unset the highlight on the previous marker, if there is a
                // previous marker
                if (previousClickedMarker) {
                    previousClickedMarker.unsetHighlight();
                }
                // Change the colour of the marker to highlight it
                marker.setHighlight();
                entryViewer.loadEntriesForLoc(marker.entry_id);
                previousClickedMarker = marker;
            });
            return marker;
        };
    })();

    var showMarkers = function () {
        $.each(markers, function (i, m) {
            m.setVisible(true);
        });
    };

    var hideMarkers = function () {
        $.each(markers, function (i, m) {
            m.setVisible(false);
        });
    };

    var toggleMarkerVisOnZoomChange = function () {
        var currentZoom = map.getZoom();
        console.log(currentZoom);
        if (currentZoom >= minMarkerVisZoom) {
            if (!markersVisible) {
                showMarkers();
                markersVisible = true;
            }
        } else if (markersVisible) {
            hideMarkers();
            markersVisible = false;
        }
    };

    // Public API
    return {
        initialise: initialise
    };
})();

var EntryViewer = (function () {

    var _domNode;

    var init = function (element) {
        _domNode = element;
        $(_domNode).scroll(loadOnScroll);
        console.log(_domNode);

        // Fill the entry viewer with the first ten entries
        var url = '/entries/query/?count=10';
        $.get(url, function(response) {
            $(_domNode).append(response);
        });
    };

    var loadOnScroll = function (numEntries) {
        if ($(_domNode).scrollTop() + $(_domNode).innerHeight() >= _domNode.scrollHeight) {
            var lastEntryNode = $(_domNode).children().last();
            var lastDate = lastEntryNode.children('.date_field').text();
            var url = '/entries/query/?count=10&start_date=' + lastDate;
            console.log(url);
            $.get(url, function(response) {
                $(_domNode).empty();
                $(_domNode).append(response);
                $(_domNode).scrollTop(0);
            });
        }
    };

    var loadEntriesForLoc = function (entryID) {
        var url = '/entries/query/?count=10&eid=' + entryID;
        $.get(url, function(response) {
            $(_domNode).empty();
            $(_domNode).append(response);
            $(_domNode).animate({scrollTop: 0});
        });
    };

    // Public api
    return {
        init: init,
        loadEntriesForLoc: loadEntriesForLoc
    };
})();

$(document).ready(function () {

    var entryViewer = EntryViewer;
    var entryViewerElem = document.getElementById('entry_box');
    entryViewer.init(entryViewerElem);

    var mapViewer = MapViewer;
    var mapViewerElem = document.getElementById('map_box');
    mapViewer.initialise(mapViewerElem, entryViewer);

//    // Fill the entry viewer with the first ten entries
//    var url = '/entries/query/?count=10';
//    $.get(url, function(response) {
//        $('#entry_box').append(response);
//    });
//    // Automatically load the next 10 entries when the user scrolls to the
//    // bottom of the entry viewer
//    $('#entry_box').scroll(function() {
//        if ($(this).scrollTop() + $(this).innerHeight() >= this.scrollHeight) {
//            // Get the ID of the last entry in the viewer
//            // Consider making the ID a property in the div tag to avoid below
//            var lastEntryDiv = $(this).children().last();
//            var lastDate = lastEntryDiv.children('.date_field').text();
//            var url = '/entries/query/?count=10&start_date=' + lastDate;
//            $.get(url, function(response) {
//                $('#entry_box').append(response);
//                // Scroll back to the top
//                $(this).scrollTop(0);
//            });
//        }
//    });
});

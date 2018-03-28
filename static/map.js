var viewer = new Cesium.Viewer('map', {
    baseLayerPicker : false,
    infoBox : true,
    timeline : false,
    animation : false,
    selectionIndicator : false
});

var pinBuilder = new Cesium.PinBuilder();

createJournalEntryMarkers(viewer, pinBuilder);

viewer.dataSources.add(Cesium.GeoJsonDataSource.load('/journals/1'));

var handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
handler.setInputAction(function(click) {
    var pickedMarker = viewer.scene.pick(click.position);
    if (Cesium.defined(pickedMarker)) {
        var url = '/entry-text/' + pickedMarker.id.name;
        $.getJSON(url, function(response) {
            pickedMarker.id.description = response.text;
        });
    }
}, Cesium.ScreenSpaceEventType.LEFT_CLICK);

function createJournalEntryMarkers(viewer, pinBuilder) {
    $.getJSON('/all-positions', function(response) {
        $.each(response, function(id, latlng) {
            viewer.entities.add({
                name : id,
                position : Cesium.Cartesian3.fromDegrees(latlng['lng'], latlng['lat']),
                    billboard : {
                        image : pinBuilder.fromColor(Cesium.Color.RED, 48),
                        verticalOrigin : Cesium.VerticalOrigin.BOTTOM,
                        scaleByDistance : new Cesium.NearFarScalar(2.0e2, 2.0, 8.0e6, 0.2)
                }
            })
        });
    });
}

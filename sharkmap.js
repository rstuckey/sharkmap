
L.mapbox.accessToken = ACCESSTOKEN;
var mapCluster = L.mapbox.map('map-cluster')
  .setView([-32.918, 151.80], 10)
  // .addLayer(L.mapbox.tileLayer('mapbox.streets'));
  .addLayer(L.mapbox.tileLayer(TILELAYER));

var featureLayer = L.mapbox.featureLayer()
  // .loadURL('/files/data/sharks_coords.geojson')
  .loadURL('sharks_coords.geojson')
  .on('ready', function(e) {
    var clusterGroup = new L.markerClusterGroup({
        iconCreateFunction: function (cluster) {
            var childCount = cluster.getChildCount();
            var c = ' marker-cluster-';
            if (childCount < 10) {
                c += 'small';
            } else if (childCount < 100) {
                c += 'medium';
            } else {
                c += 'large';
            }
            return new L.DivIcon({ html: '<div><span><b>' + childCount + '</b></span></div>', className: 'marker-cluster' + c, iconSize: new L.Point(40, 40) });
        }
    });

    e.target.eachLayer(function(layer) {
        clusterGroup.addLayer(layer);
    });
    mapCluster.addLayer(clusterGroup);
  });

// mapCluster.scrollWheelZoom.disable();

// Set a custom icon on each marker based on feature properties.
featureLayer.on('layeradd', function(e) {
    var marker = e.layer,
        feature = marker.feature;
    marker.setIcon(L.icon(feature.properties.icon));
});

// Add tooltips
featureLayer.on('mouseover', function(e) {
    e.layer.openPopup();
});
featureLayer.on('mouseout', function(e) {
    e.layer.closePopup();
});

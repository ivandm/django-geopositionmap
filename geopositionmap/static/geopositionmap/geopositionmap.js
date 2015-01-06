if (jQuery != undefined) {
    var django = {
        'jQuery': jQuery,
    }
}


(function($) {

    $(document).ready(function() {

        try {
            var _ = google;
        } catch (ReferenceError) {
            console.log('geoposition: "google" not defined.  You might not be connected to the internet.');
            return;
        }

        var mapDefaults = { // Google
            'mapTypeId': google.maps.MapTypeId.ROADMAP,
            'scrollwheel': false,
            'streetViewControl': false,
            'panControl': false
        };

        var markerDefaults = { //Google
            'draggable': true,
            'animation': google.maps.Animation.DROP
        };

        $('.geoposition-widget').each(function() {
            var $container = $(this),
                $mapsContainer = $('<div class="mapsContainer" />'),
                $googleMapTab = $(''),
                $osmMapTab = $(''),
                $mapContainer = $(''),
                $OSMmapContainer = $(''),
                $addressRow = $('<div class="geoposition-address" />'),
                $searchRow = $('<div class="geoposition-search" />'),
                $searchInput = $('<input>', {'type': 'search', 'placeholder': 'Start typing an address …'}),
                $latitudeField = $container.find('input.geoposition:eq(0)'),
                $longitudeField = $container.find('input.geoposition:eq(1)'),
                latitude = parseFloat($latitudeField.val()) || null,
                longitude = parseFloat($longitudeField.val()) || null,
                googleView = $container.data('google-view') || false,
                osmView = $container.data('osm-view') || false,
                map,
                mapLatLng,
                mapOptions,
                mapCustomOptions,
                markerOptions,
                markerCustomOptions,
                marker;
                
            mapCustomOptions = $container.data('map-options') || {};
            markerCustomOptions = $container.data('marker-options') || {};
            
            function doSearch() {
                var gc = new google.maps.Geocoder();
                $searchInput.parent().find('ul.geoposition-results').remove();
                gc.geocode({
                    'address': $searchInput.val()
                }, function(results, status) {
                    if (status == 'OK') {
                        var updatePosition = function(result) {                            
                            if (result.geometry.bounds) {
                                if (googleView){map.fitBounds(result.geometry.bounds)};
                                if (osmView){ 
                                    var ne = result.geometry.bounds.getNorthEast();
                                    var sw = result.geometry.bounds.getSouthWest();
                                    var bounds = [[ne.lat(),ne.lng()], 
                                                  [sw.lat(),sw.lng()]];
                                    osm_map.fitBounds(bounds);
                                };
                            } else {
                                if (googleView){
                                    map.panTo(result.geometry.location);
                                    //map.setZoom(18);
                                }
                                if (osmView){
                                    osm_map.panTo([result.geometry.location.lat(), 
                                                   result.geometry.location.lng()]);
                                    //osm_map.setZoom(18);
                                };
                            }
                            if (googleView){ // set Google marker
                                marker.setPosition(result.geometry.location);
                                google.maps.event.trigger(marker, 'dragend');
                            }
                            if (osmView){ /*TODO: osm */
                                osm_marker.setLatLng([result.geometry.location.lat(), 
                                                   result.geometry.location.lng()]);
                                osm_marker.update();
                            };
                        };
                        if (results.length == 1) {
                            updatePosition(results[0]);
                        } else {
                            var $ul = $('<ul />', {'class': 'geoposition-results'});
                            $.each(results, function(i, result) {
                                var $li = $('<li />');
                                $li.text(result.formatted_address);
                                $li.on('click', function() {
                                    updatePosition(result);
                                    $li.closest('ul').remove();
                                });
                                $li.appendTo($ul);
                            });
                            $searchInput.after($ul);
                        }
                    }
                });
            }

            function doGeocode(lat, lng) {
                var gc = new google.maps.Geocoder();
                var center = new google.maps.LatLng(lat, lng);
                gc.geocode({
                    'latLng': center //marker.position
                }, function(results, status) {
                    $addressRow.text('');
                    if (results && results[0]) {
                        $addressRow.text(results[0].formatted_address);
                    }
                });
            }

            if (googleView == true || osmView == true){
                var autoSuggestTimer = null;
                $searchInput.on('keydown', function(e) {
                    if (autoSuggestTimer) {
                        clearTimeout(autoSuggestTimer);
                        autoSuggestTimer = null;
                    }

                    // if ENTER keyboard button pushed, search immediately
                    if (e.keyCode == 13) {
                        e.preventDefault();
                        doSearch();
                    }
                    else {
                        // otherwise, search after a while after typing ends
                        autoSuggestTimer = setTimeout(function(){
                            doSearch();
                        }, 1000);
                    }
                }).on('abort', function() {
                    $(this).parent().find('ul.geoposition-results').remove();
                });
                $searchInput.appendTo($searchRow);
            }
            // Create google and osm container with their link tabs
            if (googleView == true ){
                $mapContainer = $('<div class="geoposition-map" />');
                $mapContainer.css('height', $container.data('map-widget-height') + 'px');
                $googleMapTab = $('<div class="googleMapTab">google</div>');
                $mapContainer.addClass('geoposition-activeMap');
            }
            if (osmView  == true ){
                $OSMmapContainer = $('<div id="osm-map" class="geoposition-osm-map" />');
                $OSMmapContainer.css('height', $container.data('map-widget-height') + 'px');            
                $osmMapTab = $('<div class="osmMapTab">osm</div>');
                $OSMmapContainer.addClass('geoposition-activeMap');
            }
            
            $mapsContainer.append(
                new $('<div class="geoposition-clear"\>'),
                googleView ? $googleMapTab : '',
                osmView ? $osmMapTab : '', 
                new $('<div class="geoposition-clear"\>'),
                googleView ? $mapContainer : '', 
                osmView ? $OSMmapContainer : '', 
                new $('<div class="geoposition-clear"\>'));
            $container.append($searchRow, $mapsContainer, $addressRow);

            // create Google Map object
            if (googleView == true ){
                // Google map options
                mapOptions = $.extend({}, mapDefaults, mapCustomOptions);
                
                // vreate new obj google map LatLng
                mapLatLng = new google.maps.LatLng(latitude, longitude);
                
                // exist Lat & Lng. Center on map
                if (!(latitude === null && longitude === null && mapOptions['center'])) {
                    mapOptions['center'] = mapLatLng;
                }

                // set up zoom
                if (!mapOptions['zoom']) {
                    mapOptions['zoom'] = latitude && longitude ? 15 : 1;
                }

                // create google map object and set up options
                map = new google.maps.Map($mapContainer.get(0), mapOptions);
                
                // create google map marker and set up itself into map
                markerOptions = $.extend({}, markerDefaults, markerCustomOptions, {
                    'map': map
                });

                if (!(latitude === null && longitude === null && markerOptions['position'])) {
                    markerOptions['position'] = mapLatLng;
                }

                marker = new google.maps.Marker(markerOptions);
                google.maps.event.addListener(marker, 'dragend', function() {
                    clickSetPosition(this.position.lat(), this.position.lng());
                    doGeocode(this.position.lat(), this.position.lng());
                });
                
                if ($latitudeField.val() && $longitudeField.val()) {
                    google.maps.event.trigger(marker, 'dragend');
                }
                $latitudeField.add($longitudeField).on('keyup', function(e) {
                    var latitude = parseFloat($latitudeField.val()) || 0;
                    var longitude = parseFloat($longitudeField.val()) || 0;
                    var center = new google.maps.LatLng(latitude, longitude);
                    map.setCenter(center);
                    map.setZoom(15);
                    marker.setPosition(center);
                    doGeocode(latitude, longitude);
                });
                
                // click event on map
                google.maps.event.addListener(map, 'click', function(evt) {
                    var center = evt.latLng;
                    clickSetPosition(center.lat(), center.lng());
                });
                
            };
            
            // create OSM Map object
            if (osmView == true ){
                // set up osm options
                osm_mapOptions = $.extend({}, mapDefaults, mapCustomOptions);               
                
                // exist Lat & Lng. Center on map
                osm_mapOptions['center'] = [0,0]; //leaflet setView map don't accept null
                if (!(latitude === null && longitude === null && osm_mapOptions['center'])) {
                    osm_mapOptions['center'] = [latitude, longitude];
                }
                
                // set up zoom
                if (!osm_mapOptions['zoom']) {
                    osm_mapOptions['zoom'] = latitude && longitude ? 15 : 1;
                }
                
                // create osm map object and set up options
                osm_map = L.map('osm-map').setView(osm_mapOptions['center'], osm_mapOptions['zoom']);
                // create Tile layer 
                // add an OpenStreetMap tile layer
                L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                }).addTo(osm_map);
                
                // create marker and options
                osm_markerOptions = $.extend({}, {
                    'draggable': true,
                });
                
                var osm_markerPosition = [0,0];
                if (!(latitude === null && longitude === null && osm_markerPosition)) {
                    osm_markerPosition = [latitude, longitude];
                }
                
                osm_marker = L.marker(osm_markerPosition, osm_markerOptions).addTo(osm_map)
                    .on('dragend', function(){
                    var position = this.getLatLng();
                    clickSetPosition(position.lat, position.lng);
                    doGeocode(position.lat, position.lng);
                });
                
                osm_map.on('click', function(evt) {
                    var center = evt.latlng;
                    clickSetPosition(center.lat, center.lng);
                });
            }
            
            // Insert link Tabs google and osm exists both
            if (googleView == true  && osmView  == true ){
                $mapContainer.addClass('geoposition-activeMap');
                $googleMapTab.on('click', function(e) {
                    $mapContainer.addClass('geoposition-activeMap');
                    $OSMmapContainer.removeClass('geoposition-activeMap');
                    });
                $osmMapTab.on('click', function(e) {
                    $mapContainer.removeClass('geoposition-activeMap');
                    $OSMmapContainer.addClass('geoposition-activeMap');
                    if (osmView == true ){
                        osm_map._onResize(); //trick hack
                    }
                    });
            }
            
            // trigger click on right map view
            if (googleView && osmView){
                $googleMapTab.trigger('click');
            }
            
            function clickSetPosition(lat, lng){
            //console.log(lat + ' ' + lng);
                $latitudeField.val(lat);
                $longitudeField.val(lng);
                if (googleView == true && typeof map !== "undefined" ){
                    var center = new google.maps.LatLng(lat, lng);
                    map.setCenter(center);
                    marker.setPosition(center);
                    //google.maps.event.trigger(marker, 'dragend');
                    };
                if (osmView == true && typeof osm_map !== "undefined" ){
                    osm_map.setView([lat, lng]);
                    osm_marker.setLatLng([lat, lng]);
                    osm_marker.update();
                    //osm_map._onResize(); //trick hack
                };
            }
        });
    });
})(django.jQuery);

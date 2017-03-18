var markers = [];
var map = null;

function init_map(map_options) {
  return new google.maps.Map(document.getElementById('map-canvas'));
}


function draw_marker(map, lat_lon, title, label, icon) {
  var point =  new google.maps.LatLng(lat_lon['lat'], lat_lon['lon']);
  console.log(lat_lon);
  var marker_args = {
      position: point,
      title: title,
      label: label,
      map: map
  };
  if (icon)
    marker_args['icon'] = icon;
  var marker = new google.maps.Marker(marker_args);
  markers.push(marker);
  return markers.length - 1;
}


function add_info_window_and_show_on_click(map, marker, window_content) {
  var info_window = new google.maps.InfoWindow({
    content: window_content
  });
  marker.addListener('click', function() {
    info_window.open(map, marker);
  });
}


function draw_route(map, start, end) {
  console.log(start);
  var start =  new google.maps.LatLng(start['lat'], start['lon']);
  console.log(end);
  var end =  new google.maps.LatLng(end['lat'], end['lon']);
  map.directions_service = new google.maps.DirectionsService();
  map.directions_display = new google.maps.DirectionsRenderer({map: map});
  map.directions_service.route({
        origin: start,
        destination: end,
        avoidTolls: true,
        avoidHighways: false,
        travelMode: google.maps.TravelMode.DRIVING
    }, function (response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            map.directions_display.setDirections(response);
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });
}


function remove_marker(marker_index) {
  markers.splice(marker_index, 1);
}


function init_map_widget(to_, from_) {
  map = init_map({
    zoom: 10,
    center: new google.maps.LatLng(from_.lat, from_.lon)
  });
  var from_marker_index = draw_marker(map, from_, 'Start', '', null);
  var to_marker_index = draw_marker(map, to_, 'Stop', '', null);
  draw_route(map, from_, to_);
}

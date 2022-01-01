$('document').ready(function() {
   function initMap() {} // initialize function in global to avoid callback issues
   datetimeInputPopulate();

 });

function datetimeInputPopulate() {
  var datetimeInput = $("#datetime-input");
  var datetimeList = [];
  var now = new Date();
  for(var i = 1; i <= 24; i++){
    var newDateObj = moment(now).add(15 * i, "minute").startOf("minute");
    var remainder = 15 - (newDateObj.minute() % 15);
    newDateObj = newDateObj.add(remainder, "minute")
    datetimeList.push(newDateObj);
  }
  $.each(datetimeList, function(index, value) {
    var date = value.toDate();
    var dateFormatted = value.format("YYYY-MM-DD HH:mm:SS UTC") // dirty but works in one given timezone
    var dateFormattedUI = value.format("h:mm a");
    if (date.getDay() > now.getDay()) {
      dateFormattedUI = "Tomorrow " + dateFormattedUI + " NYC time"
    } else {
      dateFormattedUI = "Today  " + dateFormattedUI + " NYC time"
    }
    datetimeInput.append($("<option></option>")
      .attr("value", dateFormatted).text(dateFormattedUI));
  });
}

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    mapTypeControl: false,
    center: { lat: 40.7128, lng: -74.006 },
    zoom: 11,
    streetViewControl: false,
    fullscreenControl: false
  });
  new AutocompleteDirectionsHandler(map);
}

/**
 * @constructor
 */
function AutocompleteDirectionsHandler(map) {
  this.map = map;
  this.originPlaceId = null;
  this.destinationPlaceId = null;
  originInput = document.getElementById('pickup-input');
  destinationInput = document.getElementById('dropoff-input');
  var inputRow = document.getElementById('input-row');
  this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(inputRow);
  this.directionsService = new google.maps.DirectionsService;
  this.directionsDisplay = new google.maps.DirectionsRenderer({preserveViewport: true});
  this.directionsDisplay.setMap(map);

  var nyBounds = new google.maps.LatLngBounds(
    new google.maps.LatLng(40.5, -74.3),
    new google.maps.LatLng(41.8, -72.9));
  var autocompleteOptions = {
    placeIdOnly: false,
    strictBounds: true,
    bounds: nyBounds,
    componentRestrictions: {country: 'us'}
  };
  originAutocomplete = new google.maps.places.Autocomplete(
    originInput, autocompleteOptions);
  destinationAutocomplete = new google.maps.places.Autocomplete(
    destinationInput, autocompleteOptions);

  this.setupPlaceChangedListener(originAutocomplete, 'ORIG');
  this.setupPlaceChangedListener(destinationAutocomplete, 'DEST');
}

AutocompleteDirectionsHandler.prototype.setupPlaceChangedListener = function(autocomplete, mode) {
  var me = this;
  autocomplete.bindTo('bounds', this.map);
  autocomplete.addListener('place_changed', function() {
    var place = autocomplete.getPlace();
    if (!place.place_id) {
      window.alert("Please select an option from the dropdown list.");
      return;
    }
    if (mode === 'ORIG') {
      me.originPlaceId = place.place_id;
    } else {
      me.destinationPlaceId = place.place_id;
    }
    me.route();
  }, {passive: true});
};

AutocompleteDirectionsHandler.prototype.route = function() {
  if (!this.originPlaceId || !this.destinationPlaceId) {
    return;
  }
  var me = this;

  this.directionsService.route({
    origin: { 'placeId': this.originPlaceId },
    destination: { 'placeId': this.destinationPlaceId },
    travelMode: "DRIVING"
  }, function(response, status) {
    if (status === 'OK') {
      me.directionsDisplay.setDirections(response);
      var bounds = new google.maps.LatLngBounds();
      bounds.union(response.routes[0].bounds);
      padding = $("#input-row").height() + 50
      me.map.fitBounds(bounds, {"top": padding, "right": 50, "left": 20});
    } else {
      window.alert('Directions request failed due to ' + status);
      //console.log('Directions request failed due to ' + status)
    }
  });
};

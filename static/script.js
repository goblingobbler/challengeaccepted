var geocoder;
var map;
var autocomplete = undefined;
var address = '';

//html5 geolocation
var LATITUDE = undefined;
var LONGITUDE = undefined;

var DATA = undefined;
var ADDRESS = undefined;
var WAITTIME = 1000;

var mapStyle= [{
"elementType": "labels.icon",
"stylers": [{ "saturation": -100 }
]},{
"elementType": "labels.text",
"stylers": [{ "saturation": -100 }
]},{
"featureType": "water",
"elementType": "geometry",
"stylers": [{ "color": "#959595" }
]},{
"featureType": "road",
"elementType": "geometry",
"stylers": [{ "color": "#ffffff" }
]},{
"featureType": "road.highway",
"elementType": "geometry",
"stylers": [{ "color": "#606060" }
]},{
"featureType": "landscape",
"elementType": "geometry",
"stylers": [{ "color": "#eeeeee" }
]},{
"featureType": "poi.park",
"elementType": "geometry",
"stylers": [{ "color": "#eeeeee" }
]},{
"featureType": "poi",
"elementType": "geometry",
"stylers": [{ "color": "#b7b7b7" }
]},
]


function initialize() {
	geocoder = new google.maps.Geocoder();
	if ( $('#map_canvas').length > 0 ){
		createMap();
	}
	
	var input = document.getElementById('textinput');
	if (input){
		var options = {};
		var autocomplete = new google.maps.places.Autocomplete(input, options);
		
		var s = new google.maps.LatLng(37.7749295,-122.41941550000001);
        var n = new google.maps.LatLng(37.7749295,-122.41941550000001);
        var boundary = new google.maps.LatLngBounds(s,n);
        autocomplete.setBounds(boundary);
        
		google.maps.event.addListener(autocomplete, 'place_changed', function () {
			var place = autocomplete.getPlace();
			
			LATITUDE = place.geometry.location.lat();
			LONGITUDE = place.geometry.location.lng();
			submitSearch();
	        console.log(LATITUDE + ' ' + LONGITUDE);
	    });
	}
}

function createMap(){
	var map = $('#map_canvas').gmap({'scrollwheel': false, 
		'zoomControl': true,
	    'zoomControlOptions': {
	        'style': google.maps.ZoomControlStyle.LARGE,
	        'position': google.maps.ControlPosition.RIGHT_CENTER
	    },
		'mapTypeId':google.maps.MapTypeId.ROADMAP, 
		'streetViewControl': false,
		'panControl': false,
		'callback': function() {}});
	
	var mapStyle2 = new google.maps.StyledMapType(mapStyle)
	$('#map_canvas').gmap('get','map').mapTypes.set('mapStyle', mapStyle2);
	$('#map_canvas').gmap('get','map').setMapTypeId('mapStyle');
	
}
function sizeMap(){
	if (600 > .8*$(window).height()){
		$('#map_canvas').height(.8*$(window).height());
	}
	else {
		$('#map_canvas').height(600);
	}
}

function loadPins(){
	codeHomeLatLng(parseFloat($('.map_data.lat').html()), lng = parseFloat($('.map_data.lng').html()));
	
	for (var i=0; i < res.length; i++){
		var content = '<div style="padding:5px;"><h4 style="border-bottom:2px solid #888;margin-top: 0px;padding-bottom:5px;">'+res[i]['title']+'</h4>';
		content += '<div style="max-height:150px;overflow:hidden;"><img src="'+res[i]['image']+'" style="padding-bottom:8px;margin-bottom:8px;border-bottom:2px solid #aaa;width:150px;" /></div>';
		content += '<img src="http://dmiller89.webfactional.com/django_static/curbmetrics/images/opentable-logo.gif" style="width:36px;" />';
		content += '<img src="http://dmiller89.webfactional.com/django_static/curbmetrics/images/yelp-logo.gif" style="width:36px;" />';
		content += '<img src="http://dmiller89.webfactional.com/django_static/curbmetrics/images/sfgate-logo.gif" style="width:36px;" />';
		content += '<img src="http://dmiller89.webfactional.com/django_static/curbmetrics/images/google-logo.gif" style="width:36px;" /></div>';
		codeLatLng(res[i]['lat'], res[i]['lng'],undefined,content);
	}
	
	setTimeout(function(){
		$('.smallmap .loading').remove();
		$('#map_canvas').appendTo($('.smallmap'));
	},500);
	
}


function codeHomeLatLng(lat, lng, icon, content) {
    var latlng = new google.maps.LatLng(lat, lng);
    
    var marker = { 'position': latlng}
    
    marker.icon = {
    		url: "http://dmiller89.webfactional.com/django_static/curbmetrics/images/map-pin.gif",
    	    // This marker is 20 pixels wide by 32 pixels tall.
    	    size: new google.maps.Size(100, 110),
        };
    
    geocoder.geocode({'latLng': latlng}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        if (results.length > 0) {
    	    var content = '<a href="http://maps.google.com/maps?q='+results[0].formatted_address.replace('&','%26')+'" target="_blank">'+results[0].formatted_address+'</a>';
    	    
        	$('#map_canvas').gmap('get','map').setZoom(17);
        	$('#map_canvas').gmap('get','map').setCenter(latlng);
        	$('#map_canvas').gmap('addMarker', marker ).click(function() {
                $('#map_canvas').gmap('openInfoWindow', {'content': content}, this);
            });	
      } else {
        console.log("Geocoder failed due to: " + status);
      }
    }});
}
function codeLatLng(lat, lng, icon, content) {
    var latlng = new google.maps.LatLng(lat, lng);
    
    var marker = { 'position': latlng}
    
    marker.icon = {
		url: "http://dmiller89.webfactional.com/django_static/curbmetrics/images/restaurant-map.gif",
	    // This marker is 20 pixels wide by 32 pixels tall.
	    size: new google.maps.Size(40, 40),
	    scaledSize: new google.maps.Size(40, 40),
    };
    
	$('#map_canvas').gmap('addMarker', marker ).click(function() {
        $('#map_canvas').gmap('openInfoWindow', {'content': content}, this);
    });	
}


function getAddressfromLatLng(lat, lng) {
    var latlng = new google.maps.LatLng(lat, lng);
    
	geocoder.geocode({'latLng': latlng}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			if (results.length > 0) {address = results[0].formatted_address;}
			else {console.log("Geocoder failed due to: " + status);}
			
			if (address == ''){
				address = $('input[name=textinput]').val();}
			else {
				$('input[name=textinput]').val(address);
			}
			submitSearch();
		}
	});
	
	return address;
}

function html5Geoloc(returnFunc){
	//Try W3C Geolocation (Preferred)
	if(navigator.geolocation) {
		browserSupportFlag = true;
		navigator.geolocation.getCurrentPosition(function(position) {
			LATITUDE = position.coords.latitude;
			LONGITUDE = position.coords.longitude;
			
			if (returnFunc){returnFunc(LATITUDE, LONGITUDE);}
			
		}, function (err) { 
			console.log('GEOLOCATION ERROR(' + err.code + '): ' + err.message);
			handleNoGeolocation(browserSupportFlag, returnFunc); 
		},
		{enableHighAccuracy: true, timeout:2000});
	}
	// Browser doesn't support Geolocation
	else {
		browserSupportFlag = false;
		handleNoGeolocation(browserSupportFlag, returnFunc);
	}
}
function handleNoGeolocation(errorFlag, returnFunc) {
	if (errorFlag) {
		console.log('Error: The Geolocation service failed.');
	}
	else {
		console.log('Error: Your browser doesn\'t support geolocation.');
		returnFunc();
	}
}


function ajaxWrapper(type, url, data, returnFunc){
	success = false;
	$.ajax({
		type: type,
        url: url,
        data: data,
        success: function (value) {
        	returnFunc(value);
        },
        error: function(xhr, status, error) {console.log(xhr.responseText);}
	});
}


function submitSearch(){
	address = $('input[name=textinput]').val();
	
	var data = {'lat':LATITUDE, 'lng':LONGITUDE, 'csrfmiddlewaretoken': CSRF};
	$('select option').each(function(){
		if (!$('select').val()){
			data[$(this).val().toLowerCase()] = 1;
		}
		else {
			if ($(this).val() in $('select').val()){
				data[$(this).val().toLowerCase()] = 2;
			}
			else {
				data[$(this).val().toLowerCase()] = 0;
			}
		}
		
	});
	
	$('.contentLoader').html('<div class="loading"><img src="http://dmiller89.webfactional.com/django_static/curbmetrics/images/loading.gif" /> <div>Loading Score .... </div></div>');
	setTimeout(function(){$('.contentLoader').height($('.contentLoader').children().first().height()+140)},10);
	
	DATA = data;
	ADDRESS = address;
	
	ajaxWrapper('post','/score/'+address+'/', data, loadContent);
	
}

function loadContent(value){
	if (value.indexOf('FAIL') != 0){
		shrinkSearch();
		
		$('.contentLoader').html(value);
		
		setTimeout(function(){
			$('.contentLoader').height($('.contentLoader').children().first().height());
			$('.score-number-primary').css('font-size',($('.score-number-primary').width()*.15) + 'px');
			
			setTimeout(function(){
				createCharts();
				$('.contentLoader').height('auto');
				
				setTimeout(function(){
					loadPins();
				},1200);
			},400);
		},150);
	}
	else {
		CSRF = value.split(' ')[1];
		DATA['csrfmiddlewaretoken'] = CSRF;
		setTimeout(function(){
			ajaxWrapper('post','/score/'+ADDRESS+'/', DATA, loadContent);
			console.log('Retrying address lookup');
			WAITTIME += 500;
		},WAITTIME);
	}
	
}

google.maps.event.addDomListener(window, 'load', initialize);




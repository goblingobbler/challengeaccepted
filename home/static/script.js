var geocoder;
var map;
var autocomplete = undefined;
var address = '';

//html5 geolocation
var LATITUDE = undefined;
var LONGITUDE = undefined;

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
"stylers": [{ "color": "#4c4c4c" }
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
	var map = $('#map_canvas').gmap({'scrollwheel': false,'disableDefaultUI':true, 'mapTypeId':google.maps.MapTypeId.ROADMAP, 'callback': function() {}});
	
	codeHomeLatLng(parseFloat($('.map_data.lat').html()), lng = parseFloat($('.map_data.lng').html()));
	
	setTimeout(function(){
		var mapStyle2 = new google.maps.StyledMapType(mapStyle)
		$('#map_canvas').gmap('get','map').mapTypes.set('mapStyle', mapStyle2);
		$('#map_canvas').gmap('get','map').setMapTypeId('mapStyle');
		$('#map_canvas').css('opacity',1);}
	,1000);
	
	for (var i=0; i < res.length; i++){
		var content = '<div style="padding:5px;"><h4 style="border-bottom:thin solid black;margin-top: 0px;padding-bottom:5px;">'+res[i]['title']+'</h4>';
		content += '<img src="'+res[i]['image']+'" style="padding-bottom:4px;border-bottom:thin solid black;width:150px;" />';
		content += '</div>';
		codeLatLng(res[i]['lat'], res[i]['lng'],undefined,content);
	}
}

function codeHomeLatLng(lat, lng, icon, content) {
    var latlng = new google.maps.LatLng(lat, lng);
    
    var marker = { 'position': latlng}
    if (icon){
    	marker.icon = icon;
    }
    
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
    if (icon){
    	marker.icon = icon;
    }
    
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
	
	$('.contentLoader').html('<div class="loading"><img src="http://curbmetrics.dmiller89.webfactional.com/django_static/curbmetrics/images/loading.gif" /> <div>Loading Score .... </div></div>');
	setTimeout(function(){$('.contentLoader').height($('.contentLoader').children().first().height()+140)},10);
	
	ajaxWrapper('post','/score/'+address+'/',data,loadContent);
}


function loadContent(value){
	shrinkSearch();
	
	$('.contentLoader').html(value);
	
	setTimeout(function(){
		$('.contentLoader').height($('.contentLoader').children().first().height());
		
		setTimeout(function(){
			createCharts();
			renderCharts();
			$('.contentLoader').height('auto');
			
			setTimeout(function(){
				createMap();
			},1200);
		},400);
	},150);
	
	
}

google.maps.event.addDomListener(window, 'load', initialize);




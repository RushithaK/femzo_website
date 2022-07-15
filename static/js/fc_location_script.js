// mapmyindia reverse geocoding data format
/*
example data for the api_link

{
    "responseCode": 200,
    "version": "270.191",
    "results": [
        {
            "houseNumber": "",
            "houseName": "",
            "poi": "Panchayat Headquarter",
            "poi_dist": "508",
            "street": "Unnamed Road",
            "street_dist": "7",
            "subSubLocality": "",
            "subLocality": "",
            "locality": "",
            "village": "Basopatti",
            "district": "Madhubani District",
            "subDistrict": "Basopatti",
            "city": "",
            "state": "Bihar",
            "pincode": "847225",
            "lat": "26.5645",
            "lng": "85.9914",
            "area": "India",
            "formatted_address": "Unnamed Road, Basopatti, Basopatti, Madhubani District, Bihar. 508 m from Panchayat Headquarter pin-847225 (India)"
        }
    ]
}

*/





function getLocation(){
    if(navigator.geolocation){
        document.getElementById("location").placeholder = "Allow to detect location";
        navigator.geolocation.getCurrentPosition(onSuccess, onError,{enableHighAccuracy:true});
    }else{
        document.getElementById("ip_location").placeholder = "Your browser not support";
    }
}

function onSuccess(position){
    var LAT = position.coords.latitude; 
    var LNG = position.coords.longitude;
    var key = '7eef4fe5ef9ed661b775afd23eb8608d';
    let api_link='https://apis.mapmyindia.com/advancedmaps/v1/'+key+'/rev_geocode?lat='+LAT+'&lng='+LNG;
    console.log(api_link)
    fetch(api_link)
    .then( function(response) {response.json();}).then(function(response){
        let allDetails = response.results[0];
        var area, pincode, city, district, locality, state, street, subDistrict, formatted_address;
        area = allDetails.area;
        pincode = allDetails.pincode;
        district = allDetails.district;
        city = allDetails.city;
        locality = allDetails.locality;
        state = allDetails.state;
        street = allDetails.street;
        subDistrict = allDetails.subDistrict;
        formatted_address = allDetails.formatted_address;
        document.getElementById("location").value = formatted_address;
    }).catch(function(){
        document.getElementById("location").placeholder = "Something went wrong";
    });
}

function onError(error){
    if(error.code == 1){
        document.getElementById("location").placeholder = "You denied the request";
    }else if(error.code == 2){
        document.getElementById("location").placeholder = "Location is unavailable";
    }else{
        document.getElementById("location").placeholder = "Something went wrong";
    }
}
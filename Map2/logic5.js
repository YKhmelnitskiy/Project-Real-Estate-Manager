// Function to determine marker size based on population

const formatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits:0
});

var link = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/cleveland.geojson";

// Define arrays to hold created city and state markers
var pending_arr = [];
var active_arr = [];
var sold_arr = [];

// var total = 0;
// Loop through locations and create city and state markers
for (var i = 0; i < sold_sales.length; i++) {
//   total = sold_sales[i].sale_price + total;
  // Setting the marker radius for the state by passing population into the markerSize function


  sold_arr.push( 
    L.circle(sold_sales[i].location, {
      fillOpacity: 0.75,
      color: "White",
      fillColor: "blue",
      radius: 755,
    })
    .bindPopup("<h5>" + sold_sales[i].street_1 +"<br>"+ sold_sales[i].city+", "+
                      sold_sales[i].state+" "+sold_sales[i].zip+"</h5> <hr> <h5>Sale Price: "+ formatter.format(sold_sales[i].sale_price) +"<br>"+"Closing Date: "+sold_sales[i].date+"</h5>")
  )}

for (var i = 0; i < active_sales.length; i++) {
 
  active_arr.push( 
    L.circle(active_sales[i].location, {
      fillOpacity: 0.75,
      color: "White",
      fillColor: "green",
      radius: 755,
    })
    .bindPopup("<h5>" + active_sales[i].street_1 +"<br>"+ active_sales[i].city+", "+
                      active_sales[i].state+" "+active_sales[i].zip+"</h5> <hr> <h5>Asking Price: "+ formatter.format(active_sales[i].sale_price) +"<br>"+"</h5>")
  )}

  for (var i = 0; i < pending_sales.length; i++) {
 
    pending_arr.push( 
      L.circle(pending_sales[i].location, {
        fillOpacity: 0.75,
        color: "White",
        fillColor: "yellow",
        radius: 755,
      })
      .bindPopup("<h5>" + pending_sales[i].street_1 +"<br>"+ pending_sales[i].city+", "+
                        pending_sales[i].state+" "+ pending_sales[i].zip+"</h5> <hr> <h5>Sale Price: "+ formatter.format(pending_sales[i].sale_price) +"<br>"+"</h5>")
    )}
  
// Define variables for our base layers
var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
});

var darkmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.dark",
  accessToken: API_KEY
});

var satellite = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.satellite",
  accessToken: API_KEY
});

var light = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.light",
  accessToken: API_KEY
});

// Create two separate layer groups: one for cities and one for states
var pending = L.layerGroup(pending_arr);
var active = L.layerGroup(active_arr);
var sold = L.layerGroup(sold_arr);

// Create a baseMaps object
var baseMaps = {
  "Street Map": streetmap,
  "Dark Map": darkmap,
  "Light Map": light,
  "Satellite": satellite,
  
};

// Create an overlay object
var overlayMaps = {
  "Closed": sold,
  "Active": active,
  "Pending": pending
};

// Define a map object
var myMap = L.map("map", {
  center: [41.2633560940593,-81.5724563598633],
  zoom: 10,
  layers: [light, active]
});

// Pass our map layers into our layer control
// Add the layer control to the map
L.control.layers(baseMaps, overlayMaps, {
  collapsed: false
}).addTo(myMap);

// console.log("$" + total);
// document.getElementById('output_tip').innerHTML = "$" + total;

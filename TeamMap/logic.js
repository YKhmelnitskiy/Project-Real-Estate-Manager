// Function to determine marker size based on population
function markerSize(population) {
  return population / 400;
}

const formatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits:0
});

var link = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/cleveland.geojson";

// Define arrays to hold created city and state markers
var sales_arr = [];
var makers_arr = [];
var listing_mark = [];
var listing_col = [];

var total = 0;
// Loop through locations and create city and state markers
for (var i = 0; i < home_sales.length; i++) {
  total = home_sales[i].sale_price + total;
  // Setting the marker radius for the state by passing population into the markerSize function
  var color = "";
  var radius= "";
  if (home_sales[i].sale_price > 300000) {
    color = "yellow";
    radius = 500;
  }
  else if (home_sales[i].sale_price > 200000) {
    color = "blue";
    radius = 400;
  }
  else if (home_sales[i].sale_price > 100000) {
    color = "green";
    radius = 300;
  }
  else {
    color = "red";
    radius = 200;
  }
  // Setting the marker radius for the city by passing population into the markerSize function
  makers_arr.push(
    L.marker(home_sales[i].location).bindPopup("<h5>" + home_sales[i].street_1 +"<br>"+ home_sales[i].city+", "+
                      home_sales[i].state+" "+home_sales[i].zip+"</h5> <hr> <h5>Sale Price: " + formatter.format(home_sales[i].sale_price) +"<br>"+"Closing Date: "+home_sales[i].date+"</h5>")
  );

  sales_arr.push( 
    L.circle(home_sales[i].location, {
      fillOpacity: 0.75,
      color: "White",
      fillColor: color,
      radius: markerSize(home_sales[i].sale_price),
    })
    .bindPopup("<h5>" + home_sales[i].street_1 +"<br>"+ home_sales[i].city+", "+
                      home_sales[i].state+" "+home_sales[i].zip+"</h5> <hr> <h5>Sale Price: "+ formatter.format(home_sales[i].sale_price) +"<br>"+"Closing Date: "+home_sales[i].date+"</h5>")
  )}

for (var i = 0; i < listing_sales.length; i++) {
  // Setting the marker radius for the state by passing population into the markerSize function
  var color = "";
  var radius= "";
  if (listing_sales[i].sale_price > 300000) {
    color = "yellow";
    radius = 500;
  }
  else if (listing_sales[i].sale_price > 200000) {
    color = "blue";
    radius = 400;
  }
  else if (listing_sales[i].sale_price > 100000) {
    color = "green";
    radius = 300;
  }
  else {
    color = "red";
    radius = 200;
  }
  // Setting the marker radius for the city by passing population into the markerSize function
  listing_mark.push(
    L.marker(listing_sales[i].location).bindPopup("<h5>" + listing_sales[i].street_1 +"<br>"+ listing_sales[i].city+", "+
                      listing_sales[i].state+" "+listing_sales[i].zip+"</h5> <hr> <h5>Asking Price: " + formatter.format(listing_sales[i].sale_price) +"<br>"+"</h5>")
  );

  listing_col.push( 
    L.circle(listing_sales[i].location, {
      fillOpacity: 0.75,
      color: "White",
      fillColor: color,
      radius: markerSize(listing_sales[i].sale_price),
    })
    .bindPopup("<h5>" + listing_sales[i].street_1 +"<br>"+ listing_sales[i].city+", "+
                      listing_sales[i].state+" "+listing_sales[i].zip+"</h5> <hr> <h5>Asking Price: "+ formatter.format(listing_sales[i].sale_price) +"<br>"+"</h5>")
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
var markers = L.layerGroup(makers_arr);
var sales_markers = L.layerGroup(sales_arr);
var listing_markers = L.layerGroup(listing_mark);
var listingCol = L.layerGroup(listing_col);

// Create a baseMaps object
var baseMaps = {
  "Street Map": streetmap,
  "Dark Map": darkmap,
  "Light Map": light,
  "Satellite": satellite,
  
};

// Create an overlay object
var overlayMaps = {
  "Sales by Price": sales_markers,
  "Sales Markers": markers,
  "Listings by Price": listingCol,
  "Listing Markers": listing_markers
};

// Define a map object
var myMap = L.map("map", {
  center: [41.2633560940593,-81.5724563598633],
  zoom: 10,
  layers: [streetmap, sales_markers]
});

// Pass our map layers into our layer control
// Add the layer control to the map
L.control.layers(baseMaps, overlayMaps, {
  collapsed: false
}).addTo(myMap);

console.log("$" + total);
document.getElementById('output_tip').innerHTML = "$" + total;




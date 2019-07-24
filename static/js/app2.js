// Define SVG area dimensions
var svgWidth = 850;
var svgHeight = 300;

// Define the chart's margins as an object
var chartMargin = {
    top: 30,
    right: 30,
    bottom: 30,
    left: 30
};

// Define dimensions of the chart area
var chartWidth = svgWidth - chartMargin.left - chartMargin.right;
var chartHeight = svgHeight - chartMargin.top - chartMargin.bottom;
// var chartHeight = .7 * chartWidth;

// Select body, append SVG area to it, and set the dimensions
var svg = d3
    .select("#personal_dashboard")
    .append("svg")
    .attr("height", '100%')
    .attr("width", '100%')
    .attr('viewBox', '300 300' + Math.min(chartWidth, chartHeight) + ' ' + Math.min(chartWidth, chartHeight))
    .attr('preserveAspectRatio', 'xMinYMin')
    .style('fill', '#8BC34A');

// Append a group to the SVG area and shift ('translate') it to the right and down to adhere
// to the margins set in the "chartMargin" object.
var chartGroup = svg.append("g")
    .attr("transform", `translate(${chartMargin.left}, ${chartMargin.top})`);

// Load data from hours-of-tv-watched.csv
d3.csv("/static/hours-of-tv-watched.csv", function(error, tvData) {

    // Log an error if one exists
    if (error) return console.warn(error);

    // Print the tvData
    console.log(tvData);

    // Cast the hours value to a number for each piece of tvData
    tvData.forEach(function(data) {
        data.hours = +data.hours;
    });

    // Configure a band scale for the horizontal axis with a padding of 0.1 (10%)
    var xBandScale = d3.scaleBand()
        .domain(tvData.map(d => d.name))
        .range([0, chartWidth])
        .padding(0.1);


    // Create a linear scale for the vertical axis.
    var yLinearScale = d3.scaleLinear()
        .domain([0, d3.max(tvData, d => d.hours)])
        .range([chartHeight, 0]);

    // Create two new functions passing our scales in as arguments
    // These will be used to create the chart's axes
    var bottomAxis = d3.axisBottom(xBandScale);
    var leftAxis = d3.axisLeft(yLinearScale).ticks(10);

    // Append two SVG group elements to the chartGroup area,
    // and create the bottom and left axes inside of them
    chartGroup.append("g")
        .call(leftAxis);

    chartGroup.append("g")
        .attr("transform", `translate(0, ${chartHeight})`)
        .call(bottomAxis);



    // Create one SVG rectangle per piece of tvData
    // Use the linear and band scales to position each rectangle within the chart
    chartGroup.selectAll(".bar")
        .data(tvData)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", d => xBandScale(d.name))
        .attr("y", d => yLinearScale(d.hours))
        .attr("width", xBandScale.bandwidth())
        .attr("height", d => chartHeight - yLinearScale(d.hours));


    //   // Step 1: Append tooltip div
    // var toolTip = d3.select("#chart_landing")
    // .append("div")
    // .classed("tooltip", true);

    //  // Step 2: Create "mouseover" event listener to display tooltip
    //  circlesGroup.on("mouseover", function(d) {
    //   toolTip.style("display", "block")
    //       .style("left", d3.event.pageX + "px")
    //       .style("top", d3.event.pageY + "px");
    // })
    //   // Step 3: Create "mouseout" event listener to hide tooltip
    //   .on("mouseout", function() {
    //     toolTip.style("display", "none");
    //   });


});





// When the browser loads, makeResponsive() is called.
// makeResponsive();

// When the browser window is resized, makeResponsive() is called.
// d3.select(window).on("resize", makeResponsive);
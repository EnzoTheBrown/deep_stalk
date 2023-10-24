var margin = {top: 10, right: 100, bottom: 30, left: 30},
    width = 1000 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

var svg = d3.select("#my_dataviz")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

const render = function(stock) {
    d3.json("/" + stock).then(data => {
        console.log(data)
        var allGroup = ["close", "mean_30", "neg_30", "2_pos_30", "2_neg_30", "pos_30"]

        var dataReady = allGroup.map( function(grpName) { // .map allows to do something for each element of the list
          return {
            name: grpName,
            values: data.map(function(d) {
              return {time: d.time, value: +d[grpName]};
            })
          };
        });
        var myColor = function (group){
            if (group === "close") {
                return d3.schemeSet1[2];
            }
            if (group === "mean"){
                return d3.schemeSet1[1];
            }
            if (group === "pos_30" || group === "neg_30") {
                return d3.schemeSet1[4];
            }
            return d3.schemeSet1[0];
        };
        var x = d3.scaleLinear()
          .domain([0,6000])
          .range([ 0, width ]);
        svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));

        var y = d3.scaleLinear()
          .domain( [0,1000])
          .range([ height, 0 ]);
        svg.append("g")
          .call(d3.axisLeft(y));

        var line = d3.line()
          .x(function(d) { return x(+d.time * 20) })
          .y(function(d) { return y(+d.value) })
        svg.selectAll("myLines")
          .data(dataReady)
          .enter()
          .append("path")
            .attr("d", function(d){ return line(d.values) } )
            .attr("stroke", function(d){ return myColor(d.name) })
            .style("stroke-width", 2)
            .style("fill", "none")

    })
}
render('lvmh')

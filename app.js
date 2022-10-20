var $ = require('jquery')
var d3 = require('d3')
//var university = 'uw'


   
    
    d3.select('#helloworld')
        .append('span')
        .html('Within University research collaboration graph grouped by area');

  

   

    function getKeyByValue(object, value) {
      return Object.keys(object).find(key => object[key] === value);
    }

    var allGroup = ["University of waterloo", "University of toronto", "University of british columbia"]

    // Initialize the button
    var dropdownButton = d3.select(".switch")
    .append('select')

    // add the options to the button
    dropdownButton // Add a button
      .selectAll('myOptions')
      .data(allGroup)
      .enter()
      .append('option')
      .text(function (d) { return d; }) // text showed in the menu
      .attr("value", function (d) { return d; })

      dropdownButton.on("change", function(d) {

        var selectedOption = d3.select(this).property("value")

        if (selectedOption == "University of waterloo")
        {
          processsData('uw')
        }
        else if (selectedOption == "University of toronto")
        {
          processsData('ut')
        }
        else if (selectedOption == "University of british columbia")
        {
          processsData('bc')
        }
     
    
        // run the updateChart function with this selected option
      
    })
   
    var colors = ["gold", "blue", "green", "yellow", "black", "grey", "darkgreen", "pink", "brown", "slateblue"];

    var myColor = d3.scaleOrdinal().domain(0.9)
    .range(colors)


 
    var legend_y_gap = 25
    var legend;

    var nodeloc = {}

    var simulation;

    
    var tooltip = d3.select("body")
    .append("div")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")
    .text("here is hidden div");

    var allGroup = ["before 2000", "before 2005", "before 2010", "nefore 2015","present"]

    

         


    
      
    function processsData(university)
    {
      d3.selectAll('g').remove();
      if(legend)
      {
        legend.selectAll('circle').remove();
        legend.selectAll('text').remove();
      }
        
      var nodes = []
      var links = []
      var areas = {}
      var unique_colors = []

      d3.csv('data/jean-complete-node_'+university+'.csv', function(d) {
        // convert to numerical values
        //console.log(d)
        return d
    }).then(function(data) {
        // Your d3 drawing code comes here
        // The below example draws a simple "scatterplot"


        let area_count = 0
        for(var i = 0; i < data.length; i++) {

            let obj = {
              id: '',
              title:'',
              description:'',
              area:'',
              group: 1
            }

            obj.id = data[i].Id;
            if (!(data[i].Area in areas))
            {
                areas[data[i].Area] = area_count
                area_count = area_count + 1
            }
            obj.group = areas[data[i].Area];
            obj.title = data[i].Label;
            obj.description = data[i].Description;
            obj.area = data[i].Area;
            nodeloc[data[i].Id] = i;
            nodes.push(obj);
        }

        unique_colors = generateColours({ quantity: area_count, shuffle: true });

         // Add legend dots
        legend = d3.select(".legend")
        legend.selectAll("empty")
        .data(unique_colors)
        .enter()
        .append("circle")
        .attr("cx", 100)
        .attr("cy", function(d,i){ return legend_y_gap + i*25}) 
        .attr("r", 7)
        .style("fill", function(d,i){ return d})
    
        
    
        // Add legend names
        legend.selectAll("empty")
        .data(unique_colors)
        .enter()
        .append("text")
        .attr("x", 120)
        .attr("y", function(d,i){ return legend_y_gap + i*25}) 
        .text(function(d,i){ return getKeyByValue(areas,i)})
        .attr("text-anchor", "left")
        .style("alignment-baseline", "middle")
    
        console.log(area_count)
    }) 

    

    d3.csv('data/jean-complete-edge_'+university+'.csv', function(d) {
        // convert to numerical values
        //console.log(d)
        return d
    }).then(function(data) {
        // Your d3 drawing code comes here
        // The below example draws a simple "scatterplot"

        for(var i = 0; i < data.length; i++) {
            let obj = {
                source: '',
                target: '',
                linkStrokeWidth: 1.5,
                linkStroke: "#fff",
                value: 10
            }
            obj.source = data[i].Source
            obj.target = data[i].Target
            obj.value = (data[i].Id)
            obj.linkStrokeWidth = data[i].Label*0.005
            links.push(obj);
        }
       
        
        transform(nodes, links, unique_colors)
    }) 
  }

    

    function transform(nodes, links, unique_colors)
    {
  
        const invalidation = new Promise((resolve, reject) => {
        });
        let data = {"nodes": nodes, "links": links}


      ForceGraph(data, {
          nodeId: d => d.id,
          nodeGroup: d => d.group,
          nodeTitle: d=> d.title,
          nodeRadius: d=> d.description*0.0016,
          linkStrokeWidth: l => l.linkStrokeWidth,
          colors: unique_colors,
    
          width: 3500,
          height: 3500,
          invalidation // a promise to stop the simulation when the cell is re-run
        })
           
      

    }


    const generateColours = ({ quantity = 1, shuffle = false, order = "0,360", offset = 0, saturation = 80, lightness = 50 }) => {
      let colours = [];
      for (let i = 0; i < quantity; i++) {
          let hue;
          if (order == "0,360") hue = ((360/quantity) * (quantity+i)) - 360;
          if (order == "360,0") hue = (360/quantity) * (quantity-i);
  
          hue += offset;
  
          colours.push(`hsl(${hue}, ${saturation}%, ${lightness}%)`);
      }
  
      if (shuffle) {
          // uses the Fisher-Yates Shuffle to shuffle the colours
          let currentIndex = colours.length, randomIndex;
  
          while (currentIndex != 0) {
              randomIndex = Math.floor(Math.random() * currentIndex);
              currentIndex--;
              [colours[currentIndex], colours[randomIndex]] = [colours[randomIndex], colours[currentIndex]];
          }
      }
  
      return colours;
  }



        // Copyright 2021 Observable, Inc.
// Released under the ISC license.
// https://observablehq.com/@d3/force-directed-graph
function ForceGraph({
  nodes, // an iterable of node objects (typically [{id}, …])
  links // an iterable of link objects (typically [{source, target}, …])
}, {
  nodeId = d => d.id, // given d in nodes, returns a unique identifier (string)
  nodeGroup, // given d in nodes, returns an (ordinal) value for color
  nodeGroups, // an array of ordinal values representing the node groups
  nodeTitle, // given d in nodes, a title string
  nodeFill = "currentColor", // node stroke fill (if not using a group color encoding)
  nodeStroke = "#fff", // node stroke color
  nodeStrokeWidth = 1.5, // node stroke width, in pixels
  nodeStrokeOpacity = 1, // node stroke opacity
  nodeRadius = 5, // node radius, in pixels
  nodeStrength,
  linkSource = ({source}) => source, // given d in links, returns a node identifier string
  linkTarget = ({target}) => target, // given d in links, returns a node identifier string
  linkStroke = "#999", // link stroke color
  linkStrokeOpacity = 0.6, // link stroke opacity
  linkStrokeWidth = 1.5, // given d in links, returns a stroke width in pixels
  linkStrokeLinecap = "round", // link stroke linecap
  linkStrength,
  colors = d3.schemeTableau10, // an array of color strings, for the node groups
  width = 800, // outer width, in pixels
  height = 800, // outer height, in pixels
  invalidation // when this promise resolves, stop the simulation
} = {}) {
  // Compute values.
  const N = d3.map(nodes, nodeId);
  const LS = d3.map(links, linkSource);
  const LT = d3.map(links, linkTarget);
  if (nodeTitle === undefined) nodeTitle = (_, i) => N[i];
  const T = nodeTitle == null ? null : d3.map(nodes, nodeTitle);
  const G = nodeGroup == null ? null : d3.map(nodes, nodeGroup);

  const W = typeof linkStrokeWidth !== "function" ? null : d3.map(links, linkStrokeWidth);
  const L = typeof linkStroke !== "function" ? null : d3.map(links, linkStroke);

  // Replace the input nodes and links with mutable objects for the simulation.
  //nodes = d3.map(nodes, (_, i) => ({id: N[i]}));
  //links = d3.map(links, (_, i) => ({source: LS[i], target: LT[i]}));

  // Compute default domains.
  if (G && nodeGroups === undefined) nodeGroups = G.keys();

  // Construct the scales.
  const color = nodeGroup == null ? null : d3.scaleOrdinal(nodeGroups, colors);

  // Construct the forces.
  const forceNode = d3.forceManyBody();
  const forceLink = d3.forceLink(links).id(l => l.id);
  if (nodeStrength !== undefined) forceNode.strength(nodeStrength);
  if (linkStrength !== undefined) forceLink.strength(linkStrength);

  simulation = d3.forceSimulation(nodes)
      .force("link", forceLink)
      .force("charge", forceNode)
      .force("center",  d3.forceCenter())
      .on("tick", ticked);

  const svg = d3.select(".canvas")
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [-width/2 , -height/2 , width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  const link = svg.append("g")
      .attr("stroke", typeof linkStroke !== "function" ? linkStroke : null)
      .attr("stroke-opacity", linkStrokeOpacity)
      .attr("stroke-width", typeof linkStrokeWidth !== "function" ? linkStrokeWidth : null)
      .attr("stroke-linecap", linkStrokeLinecap)
    .selectAll("line")
    .data(links)
    .join("line");

  const node = svg.append("g")
      .attr("fill", nodeFill)
      .attr("stroke", nodeStroke)
      .attr("stroke-opacity", nodeStrokeOpacity)
      .attr("stroke-width", nodeStrokeWidth)
    .selectAll("circle")
    .data(nodes)
    .join("circle")
      .attr("r", nodeRadius)
      .call(drag(simulation));
      
  if (W) link.attr("stroke-width", (d) => d.linkStrokeWidth);
  if (L) link.attr("stroke", ({index: i}) => L.get(i));
  if (G) node.attr("fill", (d) => color(d.group));
  node.append("title").text((d) => d.title);
  node.attr("class", "orig");

  node.on("mouseover", function(d){tooltip.text(d.title + " : "+ d.area + " : " + d.description); return tooltip.style("visibility", "visible");})
  node.on("mousemove", function(){return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");})
  node.on("mouseout", function(){return tooltip.style("visibility", "hidden");});



  if (invalidation != null) invalidation.then(() => simulation.stop());

  function intern(value) {
    return value !== null && typeof value === "object" ? value.valueOf() : value;
  }

  function ticked() {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    node
      .attr("cx", d => d.x)
      .attr("cy", d => d.y);
  }

  function drag(simulation) {

    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.x = d3.event.x
      event.y = d3.event.y
    }

    function dragged(event) {
      event.x = d3.event.x
      event.y = d3.event.y
  }
    
    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.x = d3.event.x
      event.y = d3.event.y
    }
    
    return d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
  }



  return Object.assign(svg.node(), {scales: {color}});
}

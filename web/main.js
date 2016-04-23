
var width = 1024;
var height = 600;

var formatNumber = d3.format(",.0f"),
    color = d3.scale.category20();

window.onload = function() {
  var factorio = d3.sankey()
  .size([width, height])
  .nodeWidth(15)
  .nodePadding(200)

  var svg = d3.select("#graph").append("svg")
  .attr("width", width)
  .attr("height", height)
  .append("g")
  .attr("transform", "translate(0, 0)");

  var path = factorio.link();

  //d3.json("data.json", function(data) {
    factorio
        .nodes(data.nodes)
        .links(data.links)
        .layout(32);

    var link = svg.append("g").selectAll(".link")
        .data(data.links)
      .enter().append("path")
        .attr("class", "link")
        .attr("d", path)
        .style("stroke-width", function(d) { return Math.max(1, d.dy / 8); })
        .style("stroke", function(d) { return d3.rgb(0, 0, 0); })
        .style("stroke-opacity", function(d) { return 0.4; })
        .style("fill", function(d) { return "none"; })
        .sort(function(a, b) { return b.dy - a.dy; });

    link.append("title")
        .text(function(d) { return d.value + " " + d.source.name; });

    // Find graphical center for a link
    centerForLink = function(link) {
      var x = (link.target.x - link.source.x) / 2;
      var y = ((link.source.y + link.sy) - (link.target.y + link.ty)) / 2;
      return { "x": x, "y": y };
    };

    var node = svg.append("g").selectAll(".node")
        .data(data.nodes)
      .enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
      .call(d3.behavior.drag()
        .origin(function(d) { return d; })
        .on("dragstart", function() { this.parentNode.appendChild(this); })
        .on("drag", dragmove));

    // Draw boxes for each node
    node.append("rect")
        .attr("height", function(d) { return d.dy; })
        .attr("width", factorio.nodeWidth())
        .style("fill", function(d) { return d.color = color(d.name.replace(/ .*/, "")); })
        .style("stroke", function(d) { return d3.rgb(d.color).darker(2); })
      .append("title")
        .text(function(d) { return d.name; });

    // Add text next to Building node
    // node.append("text")
    //     .attr("x", -6)
    //     .attr("y", function(d) { return d.dy / 2; })
    //     .attr("dy", ".35em")
    //     .attr("text-anchor", "end")
    //     .attr("transform", null)
    //     .text(function(d) { return d.name; })
    //   .filter(function(d) { return d.x < width / 2; })
    //     .attr("x", 6 + factorio.nodeWidth())
    //     .attr("text-anchor", "start");

    // Add link value annotations
    data.nodes.forEach(function(node) {
      svg_node = svg.selectAll(".node")
        .filter(function(node_d) { return node_d.name == node.name; });

      var addLinkAnnocation = function(offset, text_anchoring) {
        return function(link_d) {
          var offsets = offset(link_d);
          svg_node.append("text")
            .attr("x", offsets.x)
            .attr("y", offsets.y)
            .attr("dy", ".35em")
            .attr("text-anchor", text_anchoring)
            .text(link_d.value + " " + link_d.source.name)
            .attr("transform", null);
        };
      }
      var addSourceLinkAnnotation = addLinkAnnocation(function (link_d) {
        return { "x": 20 + factorio.nodeWidth(), "y": link_d.sy + link_d.dy / 2 };
      }, "start");
      var addTargetLinkAnnotation = addLinkAnnocation(function (link_d) {
        return { "x": -20, "y": link_d.ty + link_d.dy / 2 };
      }, "end");

      // Grab link-path SVG objects whose source is the node
      svg.selectAll(".link")
        .filter(function(link_d) { return link_d.source.name == node.name; })
        .each(addSourceLinkAnnotation);

      svg.selectAll(".link")
        .filter(function(link_d) { return link_d.target.name == node.name; })
        .each(addTargetLinkAnnotation);
    });

    function dragmove(d) {
      d3.select(this).attr("transform", "translate(" + d.x + "," + (d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))) + ")");
      factorio.relayout();
      link.attr("d", path);
    }
  //});
};

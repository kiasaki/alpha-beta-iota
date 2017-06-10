function chartComplex(target, name, url) {
  var margin = {top: 32, right: 50, bottom: 32, left: 50};
  var width = 896 - margin.left - margin.right;
  var height = 500 - margin.top - margin.bottom;
  var parseDate = d3.timeParse('%Y-%m-%d %H:%M:%S');

  var x = techan.scale.financetime().range([0, width]);
  var y = d3.scaleLinear().range([height, 0]);
  var yVolume = d3.scaleLinear().range([y(0), y(0.2)]);

  var candlestick = techan.plot.candlestick().xScale(x).yScale(y);

  var xAxis = d3.axisBottom(x);
  var xTopAxis = d3.axisTop(x);
  var yAxis = d3.axisLeft(y);
  var yRightAxis = d3.axisRight(y);

  var volumeAxis = d3.axisRight(yVolume)
    .ticks(3)
    .tickFormat(d3.format(",.3s"));

  var volume = techan.plot.volume()
    .accessor(candlestick.accessor())
    .xScale(x)
    .yScale(yVolume);

  var ohlcAnnotation = techan.plot.axisannotation()
    .axis(yAxis)
    .orient('left')
    .format(d3.format(',.4f'));

  var ohlcRightAnnotation = techan.plot.axisannotation()
    .axis(yRightAxis)
    .orient('right')
    .translate([width, 0]);

  var timeAnnotation = techan.plot.axisannotation()
    .axis(xAxis)
    .orient('bottom')
    .format(d3.timeFormat('%Y-%m-%d %H:%M'))
    .width(90)
    .translate([0, height]);

  var timeTopAnnotation = techan.plot.axisannotation()
    .axis(xTopAxis)
    .orient('top')
    .format(d3.timeFormat('%Y-%m-%d %H:%M'))
    .width(90);

  var volumeAnnotation = techan.plot.axisannotation()
    .axis(volumeAxis)
    .orient('right')
    .width(35);

  var crosshair = techan.plot.crosshair()
    .xScale(x)
    .yScale(y)
    .xAnnotation([timeAnnotation, timeTopAnnotation])
    .yAnnotation([ohlcAnnotation, ohlcRightAnnotation, volumeAnnotation])
    .on('enter', enter)
    .on('out', out)
    .on('move', move);

  d3.select(target).html(null);
  var svg = d3.select(target).append('svg')
    .classed('chart-complex', true)
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

  var coordsText = svg.append('text')
    .style('text-anchor', 'end')
    .attr('class', 'coords')
    .attr('x', width - 5)
    .attr('y', 15);

  d3.csv(url, function(error, data) {
    if (error) {
      throw error;
    }

    var accessor = candlestick.accessor();

    data = data.map(function(d) {
      return {
        date: parseDate(d.dt),
        open: +d.o,
        high: +d.h,
        low: +d.l,
        close: +d.c,
        volume: +d.vol
      };
    }).sort(function(a, b) {
      return d3.ascending(accessor.d(a), accessor.d(b));
    });

    x.domain(data.map(accessor.d));
    y.domain(techan.scale.plot.ohlc(data, accessor).domain());
    yVolume.domain(techan.scale.plot.volume(data).domain());

    svg.append('g')
      .attr('class', 'volume')
      .datum(data)
      .call(volume);

    svg.append('g')
      .attr('class', 'candlestick')
      .datum(data)
      .call(candlestick);

    svg.append('g')
      .attr('class', 'volume axis')
      .datum(data)
      .call(volumeAxis);

    svg.append('g')
      .attr('class', 'x axis')
      .call(xTopAxis);

    svg.append('g')
      .attr('class', 'x axis')
      .attr('transform', 'translate(0,' + height + ')')
      .call(xAxis);

    svg.append('g')
      .attr('class', 'y axis')
      .call(yAxis);

    svg.append('g')
      .attr('class', 'y axis')
      .attr('transform', 'translate(' + width + ',0)')
      .call(yRightAxis);

    svg.append('g')
      .attr('class', 'crosshair')
      .datum({ x: x.domain()[10], y: 1.104 })
      .call(crosshair)
      .each(function(d) { move(d); }); // Display the current data

    svg.append('text')
      .attr('x', 5)
      .attr('y', 15)
      .text(name);
  });

  function enter() {
    coordsText.style('display', 'inline');
  }

  function out() {
    coordsText.style('display', 'none');
  }

  function move(coords) {
    coordsText.text(
        timeAnnotation.format()(coords.x) + ', ' + ohlcAnnotation.format()(coords.y)
    );
  }
}

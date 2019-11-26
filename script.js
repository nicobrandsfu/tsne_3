
// ---------- TSNE.js --------------------

var opt = {}
opt.epsilon = 60; // epsilon is learning rate (10 = default) // 60
opt.perplexity = 6; // roughly how many neighbors each point influences (30 = default) // 8
opt.dim = 2; // dimensionality of the embedding (2 = default)

var tsne = new tsnejs.tSNE(opt); // create a tSNE instance
var Y;

// ---------- DATA ARRAYS --------------------
var sent = [];
var sent_values = [];
var sent_valuesAvr = [];
var sent_strings_1 = [];
var sent_strings = [];

var words_strings = [];
var words_strings_1 = [];

var sent_emotion = [];
var sent_sentiment = [];
var sent_emotionLabel_1 = [];
var sent_sentiLabel_1 = [];
var sent_sentiLabel_2 = [];

// Vector data and Sentiment & Emotion data combined (NOT USED)
var vecSentData = [];

// t-Sne Data
var all_data = [];


// ---------- HANDLES --------------------

var scale = 10;

var wCanvas = 1200;
var hCanvas = 600;

var wHalf = wCanvas / 2;
var hHalf = hCanvas / 2;


// ---------- UPDATE FUNCTION --------------------

function updateEmbedding() {
  var Y = tsne.getSolution();
  //console.log(Y);
  svg.selectAll('.sentences')
    .data(Y)
    .attr("transform", function(d, i) {
      return "translate(" +
        ((Y[i][0] * scale * ss + tx) + wHalf) + "," +
        ((Y[i][1] * scale * ss + ty) + hHalf) + ")";
    })
}


// ---------- DRAW WITH D3.JS --------------------

var svg;

function drawEmbedding() {

  $("#embed").empty();

  var div = d3.select("#embed");

  // function for wrapping text in D3 V3
  function wrap(text, width) {
    text.each(function() {
      var text = d3.select(this),
        words = text.text().split(/\s+/).reverse(),
        word,
        line = [],
        lineNumber = 3,
        lineHeight = 1.4, // ems
        y = text.attr("y"),
        dy = parseFloat(text.attr("dy")),
        tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
      while (word = words.pop()) {
        line.push(word);
        tspan.text(line.join(" "));
        if (tspan.node().getComputedTextLength() > width) {
          line.pop();
          tspan.text(line.join(" "));
          line = [word];
          tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", 16).text(word);
        }
      }
    });
  }

  var Y = tsne.Y;

  svg = div.append("svg") // svg is global
    .attr("width", wCanvas)
    .attr("height", hCanvas);

  var g = svg.selectAll(".b")
    .data(sent_values)
    .enter().append("g")
    .attr("class", "sentences");

  // Initialize colors for the three keys: Negative, neutral & positiv
  var colors = ['#EF684B', '#00A674', '#4D6CFF'];

  //Draw the Circle
  var circle = g.append("circle")
    .attr("fill", "#3F574A")
    .attr("opacity", "0.1")
    .attr("r", 18)
    .data(sent_sentiLabel_1)
    .attr('fill', function(d, i) {
      if (d == "negative")
        return colors[0];
      if (d == "neutral")
        return colors[2];
      if (d == "positive")
        return colors[1];
    });

  //Draw the Circle
  var circle = g.append("circle")
    .attr("fill", "#3F574A")
    .attr("opacity", "1")
    .attr("r", 3)
    .data(sent_sentiLabel_1)
    .attr('fill', function(d, i) {
      if (d == "negative")
        return colors[0];
      if (d == "neutral")
        return colors[2];
      if (d == "positive")
        return colors[1];
    });

  g.append("text")
    .data(sent_strings)
    .attr("text-anchor", "left")
    .attr("font-size", 14)
    .attr("fill", "333")
    .attr("opacity", "0")
    .text(function(d) {
      return d;
    })
    .call(wrap, 400)
    .on('mouseover', function(d, i) {
      d3.select(this).transition()
        .duration('50')
        .attr('opacity', '1');
    })
    .on('mouseout', function(d, i) {
      d3.select(this).transition()
        .duration('50')
        .attr('opacity', '0');
    });


  var zoomListener = d3.behavior.zoom()
    .scaleExtent([0.1, 100])
    .center([0, 0])
    .on("zoom", zoomHandler);
  zoomListener(svg);

}

// Zoom Variables are defined
var tx = 0,
  ty = 0;
var ss = 1;
function zoomHandler() {
  tx = d3.event.translate[0];
  ty = d3.event.translate[1];
  ss = d3.event.scale;
}

// calls the tsne.step to iterate
function step() {
  for (var k = 0; k < 1; k++) {
    tsne.step(); // do a few steps
  }
  updateEmbedding();
}

// ---------- EVERYTHING DYNAMIC GETS PROCESSED OR CALLED HERE --------------------

//JQUERY GET JSON
$(document).ready(function() {

  // ---------- ASYCHNRON JSON LODADING --------------------

  // TF-IDF Scores from JSON file & deactivate asynch
  $.ajax({
    async: false,
    url: "json/vector_colums.json",
    dataType: 'json',
    data: sent_values,
    success: function(json) {
      for (var i in json)
        sent.push(json[i]);
      for (var i in json)
        sent_values.push(Object.values(sent[i]));

      // calculates an overall TF-IDF score -> 1 Feature
      // for (var i = 0; i < copy_values.length; i++) {
      //     console.log(sent_values[i].reduce((a, b) => a + b, 0));
      // }
    }

  });
  // Get Sentences as Strings
  $.ajax({
    async: false,
    url: "json/P1_Sentences.json",
    dataType: 'json',
    data: sent_strings,
    success: function(json) {
      for (var i in json)
        sent_strings_1.push(Object.values(json[i]));
      sent_strings = sent_strings_1[0];
    }
  });

  $.ajax({
    async: false,
    url: "json/emotionObj_saved.json",
    dataType: 'json',
    data: sent_emotion,
    success: function(json) {
      for (var i in json)
        sent_emotion.push(Object.values(json[i]));
      sent_emotionLabel_1.push(Object.keys(json[i]));
    }
  });

  $.ajax({
    async: false,
    url: "json/sentimentObj_saved.json",
    dataType: 'json',
    data: sent_sentiment,
    success: function(json) {
      for (var i in json)
        sent_sentiment.push(Object.values(json[i]));
    }

  });

  // ---------- PRE PROCESS ARRAY & VALUES IN THE RIGHT FORMAT --------------------

  // Splices labels into Array of Sentence strings
  for (var i = 0; i < sent_sentiment.length; i++) {
    sent_sentiLabel_2[i] = sent_sentiment[i].splice(0, 1);
  }

  // slice emotion array for new all data array
  all_data = sent_emotion.slice();
  //console.log(all_data);

  // push sentiment values in all data
  for (var i = 0; i < sent_sentiment.length; i++) {
    all_data[i].push(sent_sentiment[i][0]);
    sent_sentiLabel_1.push(sent_sentiment[i][1]);
  }

  // TF-IDF Score + Sentiment values + Emotion Values
  for (var j = 0; j < 5; j++) {
    for (var i = 0; i < sent_sentiment.length; i++) {
      vecSentData.push(sent_values[i]);
      vecSentData[i].push(all_data[0][j]);
      // console.log(vecSentData);
    }
  }

  // ---------- TSNE GETS DATA AND MAIN FUNCTIONS GET CALLED --------------------

  //console.log(all_data);
  tsne.initDataRaw(all_data); // t-SNE gets values here!!!
  // tsne.initDataRaw(sent_values); // t-SNE gets values here!!!
  drawEmbedding();
  setInterval(step, 0);
  //updateEmbedding(); // updateEmbedding (normaly in step function)

});

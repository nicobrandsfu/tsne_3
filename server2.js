var http = require('http');
var fs = require('fs');


const PORT=8080;

fs.readFile('index.html', function (err, html) {

    if (err) throw err;

    http.createServer(function(request, response) {
        response.writeHeader(200, {"Content-Type": "text/html"});
        response.write(html);
        response.end();
    }).listen(PORT);
});

// fs.readFile('script.js', function (err, javascript) {
//
//     if (err) throw err;
//
//     http.createServer(function(request, response) {
//         response.writeHeader(200, {"Content-Type": "text/javascript"});
//         response.write(javascript);
//         response.end();
//     }).listen(PORT);
// });

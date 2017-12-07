const http = require('http')

const PORT = 8080
let responses = {}

function handle (request, response) {
  let msize = request.url.substr(1)
  if (!msize) {
    msize = 1024
  } else {
    msize = parseInt(msize, 10)
  }
  if (!responses[msize]) {
    responses[msize] = new Buffer(msize).fill('X')
  }
  response.end(responses[msize])
}

var server = http.createServer(handle);

server.listen(PORT, () => {
 console.log('Serving on ::' + PORT.toString())
})

const express = require('express')
const app = express()

const PORT = 8080
let responses = {}

app.get('/:size', (req, res) => {
  let msize = 1024

  if (req.params.size) {
    msize = parseInt(msize, 10)
  }

  if (!responses[msize]) {
    responses[msize] = new Buffer(msize).fill('X')
  }
  res.end(responses[msize])
})

app.listen(PORT, () => {
 console.log('Serving on ::' + PORT.toString())
})

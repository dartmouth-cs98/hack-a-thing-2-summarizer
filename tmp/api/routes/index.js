var express = require('express');
var router = express.Router();
var io = require('socket.io-client')
const socket = io("http://0.0.0.0:8080")

let hackFlag = false;
let currentResult = ""

socket.on("summary_result", (data) => {
    console.log("here")
    currentResult = data;
    hackFlag = true;
})

socket.on("connect", (data) => {
    // console.log(data);
})

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.post('/csv', function(req, res, next) {
  let fileName = req.body.path;
  let textFieldName = req.body.textFieldName
  var obj = {
    fileName,
    textFieldName,
  }
  socket.emit("summarize_csv", JSON.stringify(obj))

  while (hackFlag === false) {

  }

  hackFlag = false;
  let result = currentResult;
  currentResult = "";
  res.send(result);
})

module.exports = router;

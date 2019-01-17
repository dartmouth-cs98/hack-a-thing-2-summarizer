var express = require('express');
var router = express.Router();
var kue = require('kue');
var queue = kue.createQueue();


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/csv', function(req, res, next) {
  // let fileName = req.body.path;
  // let textFieldName = req.body.textFieldName
  var obj = {
    fileName: "./data/tennis_articles_v4.csv",
    textFieldName: "article_text",
  }

  const job = queue.create('text', {
    title: "summary",
    content: JSON.stringify(obj)
  })
    .removeOnComplete(true)
    .save((err) => {
      if (err) {
        console.log('INDEX JOB SAVE FAILED');
        // process.exit(0);
        return;
      }
      job.on('complete', (result) => {
        console.log('INDEX JOB COMPLETE');
        console.log(result);
        console.log(result[0])
        let summary = "Summary: <br />"

        for (x of result) {
          summary = summary + x.summary + '<br /> <br /> '
        }
        res.send(summary)
        // process.exit(0);
      });
      job.on('failed', (errorMessage) => {
        console.log('INDEX JOB FAILED');
        console.log(errorMessage);
        // process.exit(0);
      });
    });
})

module.exports = router;

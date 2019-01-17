var io = require('socket.io-client')
const socket = io("http://0.0.0.0:8080")

var kue = require('kue');
var jobs = kue.createQueue();

let job_ids = {}
let current_job_id = 0

jobs.process( 'text', 1, function ( job, done ) {
    let content = JSON.parse(job.data.content)
    
    // Store `done()` method for socket callback (hack until redis in python)
    job_ids[current_job_id] = done;
    var obj = {
        fileName: content.fileName,
        textFieldName: content.textFieldName,
        job: current_job_id,
    }
    current_job_id = current_job_id + 1;
    socket.emit("summarize_csv", JSON.stringify(obj))

    // test(done)
} );


// start the UI
kue.app.listen( 3000 );
console.log( 'UI started on port 3000' );

socket.on("summary_result", (data) => {
    
    // Unpack object
    let summaryObj = JSON.parse(data)
    let summaryResults = summaryObj.result

    // Sort by sentence index
    summaryResults.sort((x, y) => { return x.sentenceIndex - y.sentenceIndex })

    // Print each summary
    for (result of summaryResults) {
        console.log(result)
    }

    job_ids[summaryObj.jobId](null, summaryResults)
})

socket.on("connect", (data) => {
    // console.log(data);
})








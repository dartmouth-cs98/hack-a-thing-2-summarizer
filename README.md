# hack-a-thing-2-summarizer

Tyler Burnam

## Short description of what you attempted to build
I was inspired by Jon Kotz's hack project last week related to summarizing text - it's a problem I've often thought about. I found this tutorial https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/ and followed it in Python. Using cosine distance of word embeddings from the GLOVE data set, I was able to write an AI that summarizes text using an extraction method. Further, I interoped the Python compute process with Node using sockets and Redis, which allowed for seamless integration into Node services.

## What you learned
I learned about writing ML algorithms from scratch, albeit quite simple and from a tutorial. I also learned about Redis and Kue, which will certainly become a staple in my workflow.

## How does this hack-a-thing inspire you or relate to your possible project ideas?
Using Redis allows for really efficient and clean distributed computing for CPU intensive tasks. I would like to have a strong distributed element to my project and Redis will likely be key.

## What didn’t work
The original idea was to have Python work on a redis queue. So it would poll a piece of work (text) and then use the Summarizer instance to process it. There would be an independent Node server set up to create records in the redis queue (via API) and would have a callback on completion of the task. However, I had a hard time getting Redis interopting with my Node code. As such, I very hackily threw together an intermediate Node layer that communicates via sockets to the Python summarizer. Essentially, it reads work from a queue, passes the work to Python, and once Python finishes, the Node intermediate layer updates the Redis task as complete - triggering the independent Node server to invoke it's completion callback. In essence, the user story is the exact same, it's just hacky/unscalable right now.

I really wanted to get a POST route set up instead of the current solution (modifying the text field of a CSV file on the machine). However, it will be an easy addition at a later date

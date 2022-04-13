
Descriptions
============
**This repo provides the support code for one of my [blogs](https://medium.com/analytics-vidhya/optimize-your-code-with-python-generator-9498b6ea1fa4)**

This is a simple application to consume messages from aws sqs queue.

The program consumes the messages from SQS queue and dump certain stats into outputs file.

The below criteria has been taken into consideration

- [x] Assumptions of limited messages from queues. 
- [x] Only one test case to demonstrate that unit test is essential for code testing
- [x] Code packaging - by sdist and containerization
- [x] Standard logging - timerotating and console handlers. Reason for timerotating handler is to rotate long running jobs.
- [x] For the demo purpose it is limited to write stats into outputs folder.


sample data looks like - 

{'Messages': [{'MessageId': '762b5a79–29b2–72b8-f788–606ccf806629', 'ReceiptHandle': 'urgtrhwwtg', 'MD5OfBody': '91e9b5c6e0f9860130e56f575680744d', 'Body': '{"type": "pageview", "value": 2.5, "occurred_at": "2021–03–03 10:33:38"}', 'Attributes': {'SenderId': 'AIDAIT2UOQQY3AUEKVGXU', 'SentTimestamp': '1614764020782', 'ApproximateReceiveCount': '6', 'ApproximateFirstReceiveTimestamp': '1614784965208'}}],…… up to n messages}

And expected output should be 

{
"type": "pageview",
"count": 1,
"sum": 2.5,
...
}

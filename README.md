
Descriptions
============

This is a simple application to consume messages from aws sqs queue 
The program consumes the messages from sql queue and dump certain stats into outputs file.

The below criteria has been taken into consideration

- [x] Assumptions of limited messages from queues. 
- [x] Only one test case to demonstrate that unit test is essential for code testing
- [x] Code packaging - by sdist and containerization
- [x] Standard logging - timerotating and console handlers. Reason for timerotating handler is to rotate long running jobs.
- [x] For the demo purpose it is limited to write stats into outputs folder.


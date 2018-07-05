Example illustrates the concept of Direct Exchange and Round robin consumer in RabbitMQ.

Example use case that was chosen to implement the Round robin consumer using Direct exchange is, check and print the 
status code of top websites.

List of website address are captured in the file **top500.domains.05.18.csv**

**Brief about the implementation:**
<br>Producer will read the **top500.domains.05.18.csv** for list of website DNS names. Then send one message per website
 name to a RabbitMQ Direct Exchange. 
 
<br>Run the consumer, to consume the message from RabbitMQ and check the ttp status code for given website. You could 
chose to as many as consumer as you want. If you run more that one consumer, the load will be distributed to each 
consumer in round robin manner.


Example illustrates the concept of Fanout Exchange in RabbitMQ.

Example use case that was chosen to implement using fanout exchange is, 
1) Check and print the status code of top websites.
2) Read and print a website content
3) Read the website content and count the occurrence of a tag in given html content

List of website address are captured in the file **top500.domains.05.18.csv**

**Brief about the implementation:**
<br>Producer will read the **top500.domains.05.18.csv** for list of website DNS names. Then send one message per website
 name to a RabbitMQ Direct Exchange. 



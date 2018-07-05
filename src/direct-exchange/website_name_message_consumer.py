import sys
import pika
import urllib2
from constant import DEFAULT_RABBITMQ_URL, \
    WEBSITE_STATUS_CHECK_QUEUE_NAME, \
    WEBSITE_EXCHANGE_NAME, \
    WEBSITE_STATUS_CHECK_ROUTINGKEY


class RabbitMQWebsiteNameMessageConsumer:
    def __init__(self):
        self.rabbit_url = None
        if len(sys.argv) > 1:
            self.rabbit_url.argv[1]
        else:
            self.rabbit_url = DEFAULT_RABBITMQ_URL
        print 'Connecting to RabbitMQ @ ', self.rabbit_url

        self.rabbit_urlparam = pika.URLParameters(self.rabbit_url)
        self.rabbit_urlparam.socket_timeout = 5

        self.is_connected = False
        # Create the TCP Connection to the RabbitMQ Broker
        try:
            self.rabbit_connection = pika.BlockingConnection()

            # Create a channel, create the required queue and
            # close the channel.
            channel = self.rabbit_connection.channel()
            channel.queue_declare(queue=WEBSITE_STATUS_CHECK_QUEUE_NAME)

            # Bind the queue with exchange using the routing key
            channel.queue_bind(queue=WEBSITE_STATUS_CHECK_QUEUE_NAME,
                               exchange=WEBSITE_EXCHANGE_NAME,
                               routing_key=WEBSITE_STATUS_CHECK_ROUTINGKEY)

            channel.close()

            self.is_connected = True
        except Exception, e:
            print e

    def consume(self):
        channel = self.rabbit_connection.channel()
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.process_message,
                              queue=WEBSITE_STATUS_CHECK_QUEUE_NAME)
        channel.start_consuming()


    def process_message(self, channel, method, properties, website_name):
        print 'Received website name to check the status:', website_name

        if not website_name.startswith('http'):
            website_name = 'http://' + website_name

        try:
            response = urllib2.urlopen(website_name, timeout=1)
            print response.getcode()
        except Exception, e:
            print 'Unable to connect to website', website_name, 'Error message:', e

        channel.basic_ack(method.delivery_tag)


if __name__ == "__main__":
    producer = RabbitMQWebsiteNameMessageConsumer()
    producer.consume()

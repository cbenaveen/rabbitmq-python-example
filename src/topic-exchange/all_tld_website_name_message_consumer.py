import sys
import pika
import urllib2
from constant import DEFAULT_RABBITMQ_URL, \
    WEBSITE_TLD_EXCHANGE_NAME, \
    ALL_TLD_WEBSITE_NAME_QUEUE, \
    ALL_TLD_WEBSITE_NAME_ROUTINGKEY


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
            channel.queue_declare(queue=ALL_TLD_WEBSITE_NAME_QUEUE)

            # Bind the queue with exchange using the routing key
            channel.queue_bind(queue=ALL_TLD_WEBSITE_NAME_QUEUE,
                               exchange=WEBSITE_TLD_EXCHANGE_NAME,
                               routing_key=ALL_TLD_WEBSITE_NAME_ROUTINGKEY)

            channel.close()

            self.is_connected = True
        except Exception, e:
            print e

    def consume(self):
        channel = self.rabbit_connection.channel()

        # Basic QOS property decides the round robin behaviours.
        # Please check the Pika Libraries Channel API documentation for more
        # information about the behaviour.
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.process_message,
                              queue=ALL_TLD_WEBSITE_NAME_QUEUE)
        channel.start_consuming()

    def process_message(self, channel, method, properties, website_name):
        print 'Received website name to check the status:', website_name
        channel.basic_ack(method.delivery_tag)


if __name__ == "__main__":
    producer = RabbitMQWebsiteNameMessageConsumer()
    producer.consume()

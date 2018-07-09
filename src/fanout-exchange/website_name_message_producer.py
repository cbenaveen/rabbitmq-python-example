import sys
import pika
from constant import DEFAULT_RABBITMQ_URL, WEBSITE_EXCHANGE_NAME

#List of top 500 website names taken from https://moz.com/top500
WEBSITE_CSV_FILE_NAME = 'top500.domains.05.18.csv'


class RabbitMQWebsiteNameMessageProducer:

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

            # Create a channel, create the required exchange and
            # close the channel.
            channel = self.rabbit_connection.channel()
            channel.exchange_declare(exchange=WEBSITE_EXCHANGE_NAME,
                                     exchange_type='fanout')
            channel.close()

            self.is_connected = True
        except Exception, e:
            print e

    def produce(self, website_names):
        if not self.is_connected:
            print 'No TCP Connection to Broker ', \
                self.rabbit_url, \
                '; Message sent failed'
            return

        channel = self.rabbit_connection.channel()

        if type(website_names) == list:
            for website in website_names:
                self.__send(channel, website)
        elif type(website_names) == str:
            self.__send(channel, website_names)
        else:
            print 'Unable to find the type of messages to send'
        pass

    def __send(self, channel, website_name):
        print 'Sending website name', website_name

        # Since we are sending to a fanout exchange, no need to specify the
        # routing key as fanout exchange will not honour the routingkey
        # unfortunately, pika api enforce to specify a routing key.
        # Hence setting it to empty
        channel.basic_publish(exchange=WEBSITE_EXCHANGE_NAME,
                              routing_key='',
                              body=website_name)


if __name__ == "__main__":
    website_list = []

    with open(WEBSITE_CSV_FILE_NAME) as csv_file:
        for line in csv_file:
            line = line.strip().split(',')
            website_list.append(line[1])

    producer = RabbitMQWebsiteNameMessageProducer()
    producer.produce(website_list)


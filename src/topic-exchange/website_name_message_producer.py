import sys
import pika
from constant import DEFAULT_RABBITMQ_URL, WEBSITE_TLD_EXCHANGE_NAME, WEBSITE_TLD_ROUTINGKEY_PREFIX

WEBSITE_CSV_FILE_NAME = 'domain_names.csv'


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
            channel.exchange_declare(exchange=WEBSITE_TLD_EXCHANGE_NAME,
                                     exchange_type='topic')
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

    def __send(self, channel, website_details):
        website_details_split = website_details.strip().split(',')
        website_name = website_details_split[2]
        website_tld = website_details_split[3]
        print 'Sending website name:', website_name, 'TLD:', website_tld
        channel.basic_publish(WEBSITE_TLD_EXCHANGE_NAME,
                              WEBSITE_TLD_ROUTINGKEY_PREFIX.format(website_tld),
                              website_name)


if __name__ == "__main__":
    website_list = []

    with open(WEBSITE_CSV_FILE_NAME) as csv_file:
        for line in csv_file:
            website_list.append(line)

    producer = RabbitMQWebsiteNameMessageProducer()
    producer.produce(website_list)


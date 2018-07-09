DEFAULT_RABBITMQ_URL = 'amqp://guest:guest@127.0.0.1:5672/%2F'

WEBSITE_EXCHANGE_NAME = 'website.name.multicast.exchange'

WEBSITE_STATUS_CHECK_ROUTINGKEY = 'website.status.check.routing'
WEBSITE_CONTENT_READ_ROUTINGKEY = 'website.content.read.routing'
WEBSITE_HTML_TAG_COUNT_ROUTINGKEY = 'website.html.tag.count.routing'

WEBSITE_STATUS_CHECK_QUEUE_NAME = 'website.status.check.queue'
WEBSITE_CONTENT_READ_QUEUE_NAME = 'website.content.read.routing'
WEBSITE_HTML_TAG_COUNT_QUEUE_NAME = 'website.html.tag.count.routing'
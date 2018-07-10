DEFAULT_RABBITMQ_URL = 'amqp://guest:guest@127.0.0.1:5672/%2F'
WEBSITE_TLD_EXCHANGE_NAME = 'website.tld.exchange'
WEBSITE_TLD_ROUTINGKEY_PREFIX = 'website.name.tld.{}'

COM_TLD_WEBSITE_NAME_QUEUE = 'website.name.tld.com'
COM_TLD_WEBSITE_NAME_ROUTINGKEY = 'website.name.*.com'

EDU_TLD_WEBSITE_NAME_QUEUE = 'website.name.tld.edu'
EDU_TLD_WEBSITE_NAME_ROUTINGKEY = 'website.name.*.edu'

ORG_TLD_WEBSITE_NAME_QUEUE = 'website.name.tld.org'
ORG_TLD_WEBSITE_NAME_ROUTINGKEY = 'website.name.*.org'

NET_TLD_WEBSITE_NAME_QUEUE = 'website.name.tld.net'
NET_TLD_WEBSITE_NAME_ROUTINGKEY = 'website.name.*.net'

ALL_TLD_WEBSITE_NAME_QUEUE = 'website.name.tld.others'
ALL_TLD_WEBSITE_NAME_ROUTINGKEY = 'website.name.#'

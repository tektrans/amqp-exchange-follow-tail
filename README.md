# amqp-exchange-follow-tail
AMPQ exchange consumer, like tail --follow

## Usage
```shell
python amqp-exchange-follow-tail.py --help
```

```
usage: amqp-exchange-follow-tail.py [-h] -u AMQP_URL -e EXCHANGE

AMPQ exchange consumer

options:
  -h, --help            show this help message and exit
  -u AMQP_URL, --amqp-url AMQP_URL
                        AMQP url, can be set by AMQP_URL environment
  -e EXCHANGE, --exchange EXCHANGE
                        AMQP exchange name, , can be set by AMQP_EXCHANGE environment

Just like "tail --follow" on AMQP exchange. You can use it to monitor published log on AMQP. This progam obey ".env" file, so you can put
your environment variable on ".env" file.
```
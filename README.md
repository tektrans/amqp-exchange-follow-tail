# amqp-exchange-follow-tail
AMPQ exchange consumer, like tail --follow

## Usage
```shell
python amqp-exchange-follow-tail.py --help
```

```
usage: amqp-exchange-follow-tail.py [-h] [-u URL] [-e EXCHANGE] [-t TOPIC] [-s] [-j] [--json-single-line] [--only-body]
                                    [--decode-to-string] [-o OUTPUT_FILE] [--version]

AMPQ exchange consumer (https://github.com/tektrans/amqp-exchange-follow-tail)

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     AMQP url, can be set by AMQP_URL environment.
  -e EXCHANGE, --exchange EXCHANGE
                        AMQP exchange name, can be set by AMQP_EXCHANGE environment.
  -t TOPIC, --topic TOPIC
                        AMQP topic, can be set by AMQP_TOPIC environment.
  -s, --silent          Do it silently.
  -j, --json            JSON output.
  --json-single-line    Single line JSON output (without indentation).
  --only-body           Dump only message body.
  --decode-to-string    Decode body to utf-8 string.
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Output file, use "-" to use STDOUT as output file. Default: -
  --version             show program's version number and exit

Just like "tail --follow" on AMQP exchange.

You can use it to monitor published log on AMQP.

This progam obey ".env" file,
so you can put your environment variable on ".env" file.
```

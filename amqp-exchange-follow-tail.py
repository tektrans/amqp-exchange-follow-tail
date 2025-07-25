#!/usr/bin/env python3

import os
import sys
import json
import argparse
from dotenv import load_dotenv
import pika

load_dotenv()

VERSION="v1.0.0"

# init variables by environment values
amqp_url = os.environ.get('AMQP_URL', None)
amqp_exchange = os.environ.get('AMQP_EXCHANGE', None)
amqp_topic = os.environ.get('AMQP_TOPIC', None)

parser = argparse.ArgumentParser(
    description="AMPQ exchange consumer (https://github.com/tektrans/amqp-exchange-follow-tail)",
    epilog="""
Just like "tail --follow" on AMQP exchange.

You can use it to monitor published log on AMQP.

This progam obey ".env" file,
so you can put your environment variable on ".env" file.
    """.strip(),
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument(
    "-u",
    "--url",
    required=not amqp_url,
    default=amqp_url,
    help="AMQP url, can be set by AMQP_URL environment."
)

parser.add_argument(
    "-e",
    "--exchange",
    required=not amqp_exchange,
    default=amqp_exchange,
    help="AMQP exchange name, can be set by AMQP_EXCHANGE environment."
)

parser.add_argument(
    "-t",
    "--topic",
    required=not amqp_topic,
    default=amqp_topic,
    help="AMQP topic, can be set by AMQP_TOPIC environment."
)

parser.add_argument(
    "-s",
    "--silent",
    action="store_true",
    help="Do it silently."
)

parser.add_argument(
    "-j",
    "--json",
    action="store_true",
    help="JSON output."
)

parser.add_argument(
    "--json-single-line",
    action="store_true",
    help="Single line JSON output (without indentation)."
)

parser.add_argument(
    "--only-body",
    action="store_true",
    help="Dump only message body."
)

parser.add_argument(
    "--decode-to-string",
    action="store_true",
    help="Decode body to utf-8 string."
)

parser.add_argument(
    "-o",
    "--output-file",
    default="-",
    help='Output file, use "-" to use STDOUT as output file. Default: -'
)

parser.add_argument('--version', action='version', version=f"%(prog)s {VERSION}")

args = parser.parse_args()

# Resetting variables by args
amqp_url = args.url
amqp_exchange = args.exchange
amqp_topic = args.topic
silent = args.silent
json_output = args.json
json_single_line = args.json_single_line
only_body = args.only_body
decode_to_string = args.decode_to_string
output_file = args.output_file

if json_single_line:
    indent = None
else:
    indent = 4

if output_file == "-":
    if not silent:
        print(f'[*] Will write output to STDOUT', file=sys.stderr)

    output_file_handle = sys.stdout
else:
    if not silent:
        print(f'[*] Will write output to "{output_file}"', file=sys.stderr)

    output_file_handle = open(output_file, "w")

if not silent:
    print('[*] Connecting to AMQP server', file=sys.stderr)

connection = pika.BlockingConnection(
    pika.URLParameters(amqp_url)
)

channel = connection.channel()
channel.exchange_declare(exchange=amqp_exchange, exchange_type="topic", durable=True)
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(
    exchange=amqp_exchange, queue=queue_name, routing_key=amqp_topic
)

if not silent:
    print('[*] Waiting for messages. To exit press CTRL+C', file=sys.stderr)

def callback(ch, method, properties, body):
    if json_output or json_single_line:
        try:
            body = json.loads(body)
        except Exception:
            body = body.decode('utf-8')

        if only_body:
            data = body
        else:
            data = {
                "routing_key": method.routing_key,
                "body": body
            }

        print(json.dumps(data, indent=indent), file=output_file_handle)
    else:
        if decode_to_string:
            body = body.decode('utf-8')

        if only_body:
            print(body, file=output_file_handle)
        else:
            print(f" [x] {method.routing_key}:{body}", file=output_file_handle)

    output_file_handle.flush()

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

channel.start_consuming()

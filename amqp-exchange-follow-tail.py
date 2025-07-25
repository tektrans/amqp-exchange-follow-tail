#!/usr/bin/env python3

import os
import argparse
from dotenv import load_dotenv

load_dotenv()

VERSION="v0.0.1"

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
    '-u',
    '--amqp-url',
    required=not os.environ.get('AMQP_URL', None),
    help="AMQP url, can be set by AMQP_URL environment."
)

parser.add_argument(
    '-e',
    '--exchange',
    required=True,
    help="AMQP exchange name, can be set by AMQP_EXCHANGE environment."
)

parser.add_argument('--version', action='version', version=f"%(prog)s {VERSION}")


args = parser.parse_args()

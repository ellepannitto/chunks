"""Welcome to chunks.

This is the entry point of the application.
"""
import os

import argparse
import logging
import logging.config

import chunks.utils.config as cutils
import chunks.core.chunker as chunker


logging.config.dictConfig(
	cutils.load(
		os.path.join(os.path.dirname(__file__), 'logging', 'logging.yml')))

logger = logging.getLogger(__name__)


def _linear(args):
	chunker.linear(args.input)
	

def main():
	"""Launch structured-distributional-model."""
	parser = argparse.ArgumentParser(prog='chunks')
	subparsers = parser.add_subparsers()
	
	parser_linear = subparsers.add_parser(
		'linear', formatter_class=argparse.RawTextHelpFormatter,
		help='basic linear chunking')
	parser_linear.add_argument('-i', '--input', required=True, help='')
	parser_linear.set_defaults(func=_linear)

	args = parser.parse_args()
	args.func(args)

#!/usr/bin/env python3
#
#  __main__.py
"""
Creates a github-style badge showing the score of a football match.

For more information, run:

.. prompt:: bash

	python -m football_badges --help

"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Based on pybadges
#  https://github.com/google/pybadges
#  Copyright 2018 The pybadge Authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#


import argparse
import sys
import tempfile
import webbrowser

from domdf_python_tools import stderr_writer
from pybadges.version import __version__

from football_badges import football_badge



def main():
	parser = argparse.ArgumentParser(
			'pybadges',
			description='generate a football score badge.')

	parser.add_argument(
			'home_name',
			help='The 2- or 3-letter code representing the home team')
	parser.add_argument(
			'away_name',
			help='The 2- or 3-letter code representing the away team')
	parser.add_argument(
			'--home-score',
			type=int,
			help='the score of the home team.')
	parser.add_argument(
			'--away-score',
			type=int,
			help='the score of the away team.')
	parser.add_argument(
			'--home-color',
			default='#555',
			help='the background color for the home team.')
	parser.add_argument(
			'--away-color',
			default='#007ec6',
			help='the background color for the away team.')
	parser.add_argument(
			'--elapsed-time',
			type=str,
			help="the elapsed time in 'MM:SS' format.")
	parser.add_argument('--browser',
						action='store_true',
						default=False,
						help='display the badge in a browser tab')
	parser.add_argument(
			'--use-pil-text-measurer',
			action='store_true',
			default=False,
			help='use the PilMeasurer to measure the length of text (kerning may '
				 'be more precise for non-Western languages. ' +
				 '--deja-vu-sans-path must also be set.')
	parser.add_argument(
			'--deja-vu-sans-path',
			default=None,
			help='the path to the ttf font file containing DejaVu Sans. If not ' +
				 'present on your system, you can download it from ' +
				 'https://www.fontsquirrel.com/fonts/dejavu-sans')
	parser.add_argument(
			'--title',
			default=None,
			help='the title to associate with the badge. See '
				 'https://developer.mozilla.org/en-US/docs/Web/SVG/Element/title')
	parser.add_argument(
			'-v',
			'--version',
			action='version',
			version='%(prog)s {version}'.format(version=__version__))

	args = parser.parse_args()

	measurer = None

	if args.use_pil_text_measurer:
		if args.deja_vu_sans_path is None:
			stderr_writer('argument --use-pil-text-measurer: must also set --deja-vu-sans-path')
			sys.exit(1)
		else:
			from pybadges import pil_text_measurer
			measurer = pil_text_measurer.PilMeasurer(args.deja_vu_sans_path)

	badge = football_badge(
			home_name=args.home_name,
			away_name=args.away_name,
			home_score=args.home_score,
			away_score=args.away_score,
			elapsed_time=args.elapsed_time,
			home_color=args.home_color,
			away_color=args.away_color,
			measurer=measurer,
			title=args.title,
			)

	if args.browser:
		_, badge_path = tempfile.mkstemp(suffix='.svg')
		with open(badge_path, 'w') as f:
			f.write(badge)

		webbrowser.open_new_tab('file://' + badge_path)
	else:
		print(badge, end='')


if __name__ == '__main__':
	main()

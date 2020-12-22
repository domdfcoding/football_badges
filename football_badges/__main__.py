#!/usr/bin/env python3
#
#  __main__.py
"""
Creates a GitHub-style badge showing the score of a football match.

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

# stdlib
import argparse
import sys
import tempfile
import webbrowser
from textwrap import dedent

# 3rd party
from domdf_python_tools.utils import stderr_writer

# this package
from football_badges import __version__, football_badge

__all__ = ["main"]


def main():

	description = dedent(
			"""\
	Generate a football score badge.

	Each of 'home' and 'away' must comprise the following, separated by commas and without spaces:

	The 2- or 3-letter code representing the team;
	the team's score;
	the background colour for the team score.

	"""
			)

	parser = argparse.ArgumentParser("football-badges", description=description)

	parser.add_argument("home")
	parser.add_argument("away")
	parser.add_argument("--elapsed-time", type=str, help="The elapsed time in 'MM:SS' format.")
	parser.add_argument(
			"--browser", action="store_true", default=False, help="Display the badge in a browser tab."
			)
	parser.add_argument(
			"--use-pil-text-measurer",
			action="store_true",
			default=False,
			help=(
					'Use the PilMeasurer to measure the length of text. '
					'(kerning may be more precise for non-Western languages.) '
					"--deja-vu-sans-path must also be set."
					)
			)
	parser.add_argument(
			"--deja-vu-sans-path",
			default=None,
			help=(
					"The path to the ttf font file containing DejaVu Sans. "
					"If not present on your system, "
					"you can download it from https://www.fontsquirrel.com/fonts/dejavu-sans"
					)
			)
	parser.add_argument(
			"--title",
			default=None,
			help=(
					'The title to associate with the badge. '
					'See https://developer.mozilla.org/en-US/docs/Web/SVG/Element/title'
					)
			)
	parser.add_argument("-v", "--version", action="version", version=f'%(prog)s {__version__}')

	args = parser.parse_args()

	home_name, home_score, home_colour, *_ = args.home.split(',')
	home_score = int(home_score)

	away_name, away_score, away_colour, *_ = args.away.split(',')
	away_score = int(away_score)

	measurer = None

	if args.use_pil_text_measurer:
		if args.deja_vu_sans_path is None:
			stderr_writer("argument --use-pil-text-measurer: must also set --deja-vu-sans-path")
			sys.exit(1)
		else:

			# 3rd party
			from pybadges import pil_text_measurer

			measurer = pil_text_measurer.PilMeasurer(args.deja_vu_sans_path)

	badge = football_badge(
			home_name=home_name,
			away_name=away_name,
			home_score=home_score,
			away_score=away_score,
			elapsed_time=args.elapsed_time,
			home_colour=home_colour,
			away_colour=away_colour,
			measurer=measurer,
			title=args.title,
			)

	if args.browser:

		with tempfile.NamedTemporaryFile('w', encoding="UTF-8", newline='\n', suffix=".svg") as fp:
			fp.write(badge)
			fp.flush()

			webbrowser.open_new_tab("file://" + fp.name)
	else:
		print(badge)


if __name__ == "__main__":
	main()

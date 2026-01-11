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
import sys
from typing import IO, Optional, Union

# 3rd party
import click
from consolekit import click_command

# this package
from football_badges import __version__, football_badge

__all__ = ["main"]


@click.version_option(__version__)
@click.option(
		"--use-pil-text-measurer",
		is_flag=True,
		default=False,
		help=(
				'Use the PilMeasurer to measure the length of text. '
				'(kerning may be more precise for non-Western languages.) '
				"--deja-vu-sans-path must also be set."
				),
		)
@click.option(
		"--deja-vu-sans-path",
		type=click.STRING,
		default=None,
		help=(
				"The path to the ttf font file containing DejaVu Sans. "
				"If not present on your system, "
				"you can download it from https://www.fontsquirrel.com/fonts/dejavu-sans"
				),
		)
@click.option(
		"-b",
		"--browser",
		is_flag=True,
		default=False,
		help="Display the badge in a browser tab.",
		)
@click.option(
		"-f",
		"--file",
		type=click.File('w'),
		help="The file to write the SVG output to.",
		default='-',
		)
@click.option(
		"-t",
		"--title",
		type=click.STRING,
		help="The title to associate with the badge.",
		default="Football Score",
		)
@click.option(
		"-E",
		"--extra-time",
		type=click.STRING,
		help="The number of minutes of extra time.",
		default=None,
		)
@click.option(
		"-e",
		"--elapsed-time",
		type=click.STRING,
		help="The elapsed time in 'MM:SS' format.",
		default=None,
		)
@click.argument("away", type=click.STRING)
@click.argument("home", type=click.STRING)
@click_command()
def main(
		home: str,
		away: str,
		elapsed_time: Optional[str] = None,
		extra_time: Optional[str] = None,
		title: str = "Football Score",
		file: IO = sys.stdout,
		browser: bool = False,
		use_pil_text_measurer: bool = False,
		deja_vu_sans_path: Optional[str] = None,
		) -> None:
	"""
	Generate a football score badge.

	Each of 'home' and 'away' must comprise the following, separated by commas and without spaces:

	 * The 2- or 3-letter code representing the team;

	 * the team's score;

	 * the background colour for the team score.
	"""

	home_score: Union[str, int]
	home_name, home_score, home_colour, *_ = home.split(',')
	home_score = int(home_score)

	away_score: Union[str, int]
	away_name, away_score, away_colour, *_ = away.split(',')
	away_score = int(away_score)

	measurer = None

	if use_pil_text_measurer:  # pragma: no cover
		if deja_vu_sans_path is None:
			raise click.UsageError("--use-pil-text-measurer: must also set --deja-vu-sans-path")
		else:

			# 3rd party
			from pybadges import pil_text_measurer

			measurer = pil_text_measurer.PilMeasurer(deja_vu_sans_path)

	badge = football_badge(
			home_name=home_name,
			away_name=away_name,
			home_score=home_score,
			away_score=away_score,
			elapsed_time=elapsed_time,
			extra_time=extra_time,
			home_colour=home_colour,
			away_colour=away_colour,
			measurer=measurer,
			title=title,
			)

	if browser:

		# this package
		from football_badges.utils import open_in_browser

		open_in_browser(badge)

	else:
		click.echo(badge, file=file, nl=False)


if __name__ == "__main__":
	sys.exit(main())

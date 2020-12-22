#!/usr/bin/env python3
#
#  __init__.py
"""
Creates a GitHub-style badge showing the score of a football match.
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
from typing import Optional
from xml.dom import minidom

# 3rd party
import jinja2
from pybadges import _NAME_TO_COLOR, precalculated_text_measurer, text_measurer

__author__ = "Dominic Davis-Foster"
__copyright__ = "2020 Dominic Davis-Foster"
__license__ = "Apache Software License v2.0"
__version__ = "0.0.0"
__email__ = "dominic@davis-foster.co.uk"

__all__ = ["football_badge"]

_JINJA2_ENVIRONMENT = jinja2.Environment(
		trim_blocks=True,
		lstrip_blocks=True,
		loader=jinja2.PackageLoader("football_badges", '.'),
		autoescape=jinja2.select_autoescape(["svg"])
		)
_JINJA2_ENVIRONMENT.globals["len"] = len


def _remove_blanks(node):
	for x in node.childNodes:
		if x.nodeType == minidom.Node.TEXT_NODE:
			if x.nodeValue:
				x.nodeValue = x.nodeValue.strip()
		elif x.nodeType == minidom.Node.ELEMENT_NODE:
			_remove_blanks(x)


def football_badge(
		home_name: str,
		away_name: str,
		home_score: int,
		away_score: int,
		home_colour: str,
		away_colour: str,
		*,
		elapsed_time: Optional[str] = None,
		extra_time: Optional[str] = None,
		title: str = "Football Score",
		measurer: Optional[text_measurer.TextMeasurer] = None,
		) -> str:
	"""
	Creates a GitHub-style badge showing the score of a football match.

	:param home_name: The 2- or 3-letter code representing the home team,
		to be displayed on the left of the badge.
	:param away_name: The 2- or 3-letter code representing the away team,
		to be displayed on the right of the badge.
	:param home_score: The score of the home team.
	:param away_score: The score of the away team.
	:param home_colour: The background colour for the home team.
	:param away_colour: The background colour for the away team.
	:param elapsed_time: The elapsed time in the match.
	:param extra_time: The number of minutes of extra time.
	:param title: The title to set in the SVG file.
	:param measurer: A text_measurer.TextMeasurer that can be used to measure the
		width of left_text and right_text.
	"""

	if measurer is None:
		measurer = (precalculated_text_measurer.PrecalculatedTextMeasurer.default())

	score = f"{home_score} - {away_score}"
	template = _JINJA2_ENVIRONMENT.get_template("template.svg")

	if elapsed_time is not None:
		show_time = True
		elapsed_time = str(elapsed_time)
	else:
		show_time = False
		elapsed_time = "0:00"

	if extra_time is not None:
		show_extra_time = True
		extra_time = str(extra_time)
		extra_time_width = measurer.text_width(extra_time) / 8,
	else:
		show_extra_time = False
		extra_time_width = 0

	svg = template.render(
			left_text=home_name,
			right_text=away_name,
			left_color=_NAME_TO_COLOR.get(home_colour, home_colour),
			right_color=_NAME_TO_COLOR.get(away_colour, away_colour),
			score=score,
			time=elapsed_time,
			show_time=show_time,
			show_extra_time=show_extra_time,
			extra_time=extra_time,
			title=title,
			score_text_width=measurer.text_width(score) / 10.0,
			extra_time_width=extra_time_width,
			)

	xml = minidom.parseString(svg)
	_remove_blanks(xml)
	xml.normalize()

	return xml.documentElement.toxml()

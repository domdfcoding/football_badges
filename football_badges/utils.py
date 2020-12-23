#!/usr/bin/env python3
#
#  utils.py
"""
Utility functions.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import tempfile
import time
import webbrowser
from functools import lru_cache

# 3rd party
import jinja2

__all__ = ["open_in_browser"]


def open_in_browser(svg: str) -> None:
	"""
	Write the given svg to a temporary file, and open it in a web browser.

	:param svg:
	"""

	with tempfile.NamedTemporaryFile('w', encoding="UTF-8", newline='\n', suffix=".svg") as fp:
		fp.write(svg)
		fp.flush()

		webbrowser.open_new_tab("file://" + fp.name)
		time.sleep(1)


@lru_cache(1)
def _environment():
	environment = jinja2.Environment(
			trim_blocks=True,
			lstrip_blocks=True,
			loader=jinja2.PackageLoader("football_badges", '.'),
			autoescape=jinja2.select_autoescape(["svg"])
			)
	environment.globals["len"] = len
	return environment

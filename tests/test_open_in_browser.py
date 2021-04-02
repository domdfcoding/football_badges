# stdlib
import webbrowser
from urllib.parse import urlparse

# 3rd party
from coincidence.regressions import AdvancedFileRegressionFixture
from domdf_python_tools.paths import PathPlus

# this package
from football_badges.utils import open_in_browser


def test_open_in_browser(
		monkeypatch,
		advanced_file_regression: AdvancedFileRegressionFixture,
		):

	def open_new_tab(url):
		url = PathPlus(urlparse(url).path)
		assert url.is_file()
		assert url.read_text() == "Not actually an SVG"

	monkeypatch.setattr(webbrowser, "open_new_tab", open_new_tab)

	open_in_browser("Not actually an SVG")
# stdlib
import webbrowser

# 3rd party
from domdf_python_tools.paths import PathPlus

# this package
from football_badges.utils import open_in_browser


def test_open_in_browser(monkeypatch):

	def open_new_tab(url: str) -> None:
		path = PathPlus.from_uri(url)
		assert path.is_file()
		assert path.read_text() == "Not actually an SVG"

	monkeypatch.setattr(webbrowser, "open_new_tab", open_new_tab)

	open_in_browser("Not actually an SVG")

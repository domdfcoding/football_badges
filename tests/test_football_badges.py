# stdlib
import webbrowser
from typing import Tuple, Union

# 3rd party
import pytest
from coincidence.regressions import AdvancedFileRegressionFixture
from consolekit.testing import CliRunner, Result
from domdf_python_tools.iterative import permutations
from domdf_python_tools.paths import PathPlus

# this package
from football_badges import football_badge
from football_badges.__main__ import main

teams = [
		"ARS",  # Arsenal
		"AV",  # Aston Villa
		"BRH",  # Brighton & Hove Albion
		"CHE",  # Chelsea
		"EVE",  # Everton
		"FUL",  # Fulham
		"LEI",  # Leicester City
		"MCI",  # Manchester City
		"SHU",  # Sheffield United
		"SOU",  # Southampton
		"TOT",  # Tottenham Hotspur
		"WBA",  # West Bromwich Albion
		"BRS",  # Barnsley
		"BRC",  # Birmingham City
		"NTG",  # Nottingham Forest
		"RDG",  # Reading
		"STK",  # Stoke City
		"WAT",  # Watford
		"WYC",  # Wycombe Wanderers
		]

scores = pytest.mark.parametrize(
		"score",
		[
				pytest.param((9, 0), id="9_0"),
				pytest.param((0, 9), id="0_9"),
				pytest.param((5, 5), id="5_5"),
				pytest.param((10, 4), id="10_4"),
				pytest.param((5, 2), id="5_2"),
				],
		)

elapsed_times = pytest.mark.parametrize(
		"elapsed_time",
		[
				"0:05",
				"0:55",
				"4:30",
				"8:15",
				"12:00",
				"32:12",
				"45:00",
				"56:09",
				"74:39",
				"90:00",
				],
		)

elapsed_extra_times = pytest.mark.parametrize(
		"time",
		[
				pytest.param(("45:00", 5), id='a'),
				pytest.param(("45:00", '5'), id='b'),
				pytest.param(("45:00", '3'), id='c'),
				pytest.param(("45:00", '3'), id='d'),
				pytest.param(("45:00", "+3"), id='e'),
				pytest.param(("48:10", '3'), id='f'),
				pytest.param(("90:00", 5), id='g'),
				pytest.param(("90:00", '5'), id='h'),
				pytest.param(("90:00", '3'), id='i'),
				pytest.param(("90:00", '3'), id='j'),
				pytest.param(("93:10", '3'), id='k'),
				pytest.param(("93:10", "+3"), id='l'),
				pytest.param(("119:10", "30"), id='m'),
				pytest.param(("119:10", "+30"), id='n'),
				pytest.param(("119:10", 30), id='o'),
				],
		)

team_perms = pytest.mark.parametrize(
		"teams",
		[pytest.param(t, id=str(idx)) for idx, t in enumerate(permutations(teams, 2)[::3])],
		)


class TestLibrary:

	@team_perms
	@scores
	def test_teams_and_score(
			self,
			advanced_file_regression: AdvancedFileRegressionFixture,
			score: Tuple[int, int],
			teams: Tuple[str, str],
			):
		output = football_badge(
				home_name=teams[0],
				away_name=teams[1],
				home_colour="red",
				away_colour="green",
				home_score=score[0],
				away_score=score[1],
				)

		advanced_file_regression.check(output, extension=".svg")

	@elapsed_times
	def test_times(self, advanced_file_regression: AdvancedFileRegressionFixture, elapsed_time: str):
		output = football_badge(
				home_name="STK",
				away_name="WYC",
				home_colour="red",
				away_colour="green",
				home_score=5,
				away_score=2,
				elapsed_time=elapsed_time,
				)

		advanced_file_regression.check(output, extension=".svg")

	@elapsed_extra_times
	def test_extra_time(
			self,
			advanced_file_regression: AdvancedFileRegressionFixture,
			time: Tuple[str, Union[str, int]],
			):
		output = football_badge(
				home_name="STK",
				away_name="WYC",
				home_colour="red",
				away_colour="green",
				home_score=5,
				away_score=2,
				elapsed_time=time[0],
				extra_time=time[1],
				)

		advanced_file_regression.check(output, extension=".svg")


class TestCLI:

	@team_perms
	@scores
	def test_teams_and_score(
			self,
			advanced_file_regression: AdvancedFileRegressionFixture,
			score: Tuple[int, int],
			teams: Tuple[str, str],
			):
		runner = CliRunner()
		result: Result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[
						f"{teams[0]},{score[0]},red",
						f"{teams[1]},{score[1]},green",
						],
				)

		assert result.exit_code == 0
		result.check_stdout(advanced_file_regression, extension=".svg")

	@elapsed_times
	def test_times(self, advanced_file_regression: AdvancedFileRegressionFixture, elapsed_time: str):
		runner = CliRunner()
		result: Result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[
						"STK,5,red",
						"WYC,2,green",
						"--elapsed-time",
						elapsed_time,
						],
				)

		assert result.exit_code == 0
		result.check_stdout(advanced_file_regression, extension=".svg")

		runner = CliRunner()
		result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[
						"STK,5,red",
						"WYC,2,green",
						"-e",
						elapsed_time,
						],
				)

		assert result.exit_code == 0
		result.check_stdout(advanced_file_regression, extension=".svg")

	@elapsed_extra_times
	def test_extra_time(
			self,
			advanced_file_regression: AdvancedFileRegressionFixture,
			time: Tuple[str, Union[str, int]],
			):
		runner = CliRunner()
		result: Result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[
						"STK,5,red",
						"WYC,2,green",
						"--elapsed-time",
						str(time[0]),
						"--extra-time",
						str(time[1]),
						],
				)

		assert result.exit_code == 0
		result.check_stdout(advanced_file_regression, extension=".svg")

		result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[
						"STK,5,red",
						"WYC,2,green",
						"-e",
						str(time[0]),
						"-E",
						str(time[1]),
						],
				)

		assert result.exit_code == 0
		result.check_stdout(advanced_file_regression, extension=".svg")

	def test_to_file(
			self,
			advanced_file_regression: AdvancedFileRegressionFixture,
			tmp_pathplus: PathPlus,
			):
		filename = tmp_pathplus / "badge.svg"

		runner = CliRunner()
		result: Result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[
						"STK,5,red",
						"WYC,2,green",
						"--elapsed-time",
						"90:00",
						"--extra-time",
						'5',
						"--file",
						str(filename),
						],
				)

		assert result.exit_code == 0
		advanced_file_regression.check_file(filename)

		runner = CliRunner()
		result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[
						"STK,5,red",
						"WYC,2,green",
						"--elapsed-time",
						"90:00",
						"--extra-time",
						'5',
						"-f",
						str(filename),
						],
				)

		assert result.exit_code == 0
		advanced_file_regression.check_file(filename)

	def test_browser(
			self,
			monkeypatch,
			advanced_file_regression: AdvancedFileRegressionFixture,
			):

		def open_new_tab(url: str) -> None:
			path = PathPlus.from_uri(url)
			assert path.is_file()
			advanced_file_regression.check_file(path)

		monkeypatch.setattr(webbrowser, "open_new_tab", open_new_tab)

		runner = CliRunner()
		result: Result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[
						"STK,5,red",
						"WYC,2,green",
						"--elapsed-time",
						"90:00",
						"--extra-time",
						'5',
						"--browser",
						],
				)

		assert result.exit_code == 0


def test_injection(advanced_file_regression: AdvancedFileRegressionFixture):
	output = football_badge(
			home_name="STK</text><script>alert(1)</script><text>",
			away_name="WYC</text><script>alert(2)</script><text>",
			home_colour='red"/><script>alert(3)</script><text',
			away_colour='green"/><script>alert(4)</script><text',
			home_score="5</text><script>alert(5)</script><rect>",  # type: ignore[arg-type]
			away_score="3</text><script>alert(6)</script><rect>",  # type: ignore[arg-type]
			elapsed_time="12:34</text><script>alert(7)</script><text>",
			extra_time="+30</text><script>alert(8)</script><text>",
			title="My Title</title><script>alert(9)</script><title>",
			)

	advanced_file_regression.check(output, extension=".svg")

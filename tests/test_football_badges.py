# stdlib
from typing import Tuple

# 3rd party
import pytest
from click.testing import CliRunner, Result
from domdf_python_tools.iterative import permutations
from domdf_python_tools.testing import check_file_output, check_file_regression
from pytest_regressions.file_regression import FileRegressionFixture

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
				]
		)

elapsed_times = pytest.mark.parametrize(
		"elapsed_time", [
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
				]
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
				]
		)

team_perms = pytest.mark.parametrize(
		"teams", [pytest.param(t, id=str(idx)) for idx, t in enumerate(permutations(teams, 2)[::3])]
		)


class TestLibrary:

	@team_perms
	@scores
	def test_teams_and_score(
			self, file_regression: FileRegressionFixture, score: Tuple[int, int], teams: Tuple[str, str]
			):
		output = football_badge(
				home_name=teams[0],
				away_name=teams[1],
				home_colour="red",
				away_colour="green",
				home_score=score[0],
				away_score=score[1],
				)

		check_file_regression(output, file_regression, extension=".svg")

	@elapsed_times
	def test_times(self, file_regression: FileRegressionFixture, elapsed_time):
		output = football_badge(
				home_name="STK",
				away_name="WYC",
				home_colour="red",
				away_colour="green",
				home_score=5,
				away_score=2,
				elapsed_time=elapsed_time
				)

		check_file_regression(output, file_regression, extension=".svg")

	@elapsed_extra_times
	def test_extra_time(self, file_regression: FileRegressionFixture, time):
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

		check_file_regression(output, file_regression, extension=".svg")


class TestCLI:

	@team_perms
	@scores
	def test_teams_and_score(
			self, file_regression: FileRegressionFixture, score: Tuple[int, int], teams: Tuple[str, str]
			):
		runner = CliRunner()
		result: Result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[
						f"{teams[0]},{score[0]},red",
						f"{teams[1]},{score[1]},green",
						]
				)

		assert result.exit_code == 0
		check_file_regression(result.stdout.rstrip(), file_regression, extension=".svg")

	@elapsed_times
	def test_times(self, file_regression: FileRegressionFixture, elapsed_time):
		runner = CliRunner()
		result: Result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[
						f"STK,5,red",
						f"WYC,2,green",
						"--elapsed-time",
						elapsed_time,
						]
				)

		assert result.exit_code == 0
		check_file_regression(result.stdout.rstrip(), file_regression, extension=".svg")

		runner = CliRunner()
		result = runner.invoke(
				main, catch_exceptions=False, args=[
						f"STK,5,red",
						f"WYC,2,green",
						"-e",
						elapsed_time,
						]
				)

		assert result.exit_code == 0
		check_file_regression(result.stdout.rstrip(), file_regression, extension=".svg")

	@elapsed_extra_times
	def test_extra_time(self, file_regression: FileRegressionFixture, time):
		runner = CliRunner()
		result: Result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[
						f"STK,5,red",
						f"WYC,2,green",
						"--elapsed-time",
						str(time[0]),
						"--extra-time",
						str(time[1]),
						]
				)

		assert result.exit_code == 0
		check_file_regression(result.stdout.rstrip(), file_regression, extension=".svg")

		runner = CliRunner()
		result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[
						f"STK,5,red",
						f"WYC,2,green",
						"-e",
						str(time[0]),
						"-E",
						str(time[1]),
						]
				)

		assert result.exit_code == 0
		check_file_regression(result.stdout.rstrip(), file_regression, extension=".svg")

	def test_to_file(self, file_regression: FileRegressionFixture, tmp_pathplus):
		filename = tmp_pathplus / "badge.svg"

		runner = CliRunner()
		result: Result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[
						f"STK,5,red",
						f"WYC,2,green",
						"--elapsed-time",
						"90:00",
						"--extra-time",
						'5',
						"--file",
						str(filename)
						]
				)

		assert result.exit_code == 0
		check_file_output(filename, file_regression)

		runner = CliRunner()
		result = runner.invoke(
				main,
				catch_exceptions=False,
				args=[
						f"STK,5,red",
						f"WYC,2,green",
						"--elapsed-time",
						"90:00",
						"--extra-time",
						'5',
						"-f",
						str(filename)
						]
				)

		assert result.exit_code == 0
		check_file_output(filename, file_regression)
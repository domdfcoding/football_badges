#!/usr/bin/env python

# 3rd party
from bs4 import BeautifulSoup

# this package
from football_badges import football_badge

s = football_badge(
		home_name="BRE",
		away_name="PNE",
		home_colour="red",
		away_colour="green",
		home_score=9,
		away_score=0,
		elapsed_time="92:34",
		extra_time='5',
		)

with open("doc-source/football_score_demo.svg", 'w', encoding="UTF-8") as fp:
	fp.write(BeautifulSoup(s, "lxml-xml").prettify())

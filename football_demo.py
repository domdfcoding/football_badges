#! /usr/bin/env python
# stdlib
import time
from datetime import datetime, timedelta

# 3rd party
from bs4 import BeautifulSoup

# this package
# import cairosvg
from football_badges import football_badge

# from PIL import Image


def timerange(start, end):
	for n in range(int((end - start).seconds)):
		yield start + timedelta(seconds=n * 15)


start = datetime(2020, 8, 1, 15, 00)
ht = start + timedelta(minutes=45, seconds=1)

images = []

for t in timerange(start, ht):
	print(t)
	time.sleep(1)

	elapsed = t - start + timedelta(minutes=10)
	seconds = elapsed.seconds % 60
	minutes = elapsed.seconds // 60
	print(repr(str(minutes).rjust(2)))

	s = football_badge(
			home_name="BRE",
			away_name="PNE",
			home_colour="red",
			away_colour="green",
			# elapsed_time="12:34",
			elapsed_time="92:34",
			extra_time="+5",
			# elapsed_time="18:00",
			# elapsed_time=f"{str(minutes).rjust(2)}:{str(seconds).zfill(2)}",
			home_score=9,
			away_score=0,
			)

	with open("doc-source/football_score_demo.svg", 'w', encoding="UTF-8") as fp:
		fp.write(BeautifulSoup(s, "lxml-xml").prettify())
		fp.flush()

	exit()


def timerange(start, end):
	for n in range(int((end - start).seconds)):
		yield start + timedelta(seconds=n)


start = datetime(2020, 8, 1, 15, 00)
ht = start + timedelta(minutes=45, seconds=1)

images = []

for t in timerange(start, ht):
	print(t)
	time.sleep(0.001)

	elapsed = t - start
	seconds = elapsed.seconds % 60
	minutes = elapsed.seconds // 60
	print(repr(str(minutes).rjust(2)))

	s = football_score(
			home_name="WBA",
			away_name="AV",
			home_colour="red",
			away_colour="green",
			elapsed_time=f"{str(minutes).rjust(2)}:{str(seconds).zfill(2)}",
			)
	# s is a string that contains the badge data as an svg image.
	# print(s)  # => <svg height="20" width="191.0" xmlns="ht

	with open("doc-source/football_score_demo.svg", 'w', encoding="UTF-8") as fp:
		fp.write(BeautifulSoup(s, "lxml-xml").prettify())

	cairosvg.svg2png(url="football_score_demo.svg", write_to="football_score_demo.png", dpi=1200, scale=10)
	with open("football_score_demo.png", "rb") as fp:
		img = Image.open(fp)
		img.load()
		images.append(img)

	exit()

with open("football_score_demo.gif", "wb") as fp:
	images[0].save(fp, save_all=True, append_images=images[1:], optimize=False, duration=45, loop=0)

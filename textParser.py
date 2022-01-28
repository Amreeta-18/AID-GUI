# Extract all text from html

from bs4 import BeautifulSoup
import requests


def textParse(filename):
	with open(filename, "r") as f:
		soup = BeautifulSoup(f, "html.parser")

	# kill all script and style elements
	for script in soup(["script", "style"]):
	    script.extract()    # rip it out

	# get text
	text = soup.get_text()

	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)

	return text

def textParse2(filename):
	with open(filename, "r") as f:
		doc = BeautifulSoup(f, "html.parser")
	# Modify tags and save html
	tags = doc.find_all("input", type = "text")
	for tag in tags:
		tag['placeholder'] = "I changed You!"

	with open("Upload/changed.html", "w") as file:
		file.write(str(doc))
	return 'PASSED'



# Extract all text from html

from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import json
import re

def cleaner(text):
	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)
	return text

def getJS(soup):
	txt = ""
	links = []
	script = soup.find_all('script')
	if script:
		if len(script) > 2:

			for sc in script:
				scr = str(sc)
				# print(script)
				if scr.find("ENV") != -1:
					scr = scr[scr.find("ENV"):scr.find("</")]
					scr = scr[scr.find("{"):scr.find("};")+1]
					# print(scr)
					
					try:
						js = json.loads(scr)
						data = js["WIKI_PAGE"]["body"]

						sp = BeautifulSoup(data, "html.parser")

						# print(sp.prettify())
						txt = sp.get_text()
						links = sp.find_all("a")
						return [txt, links]
					except:
						pass
	# print(links)
	return [txt, links]

def tag_visible(element):
	if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
		return False
	if isinstance(element, Comment):
		return False
	if re.match(r"[\n]+",str(element)): return False
	return True

def getHTML(soup):
	texts = soup.findAll(text=True)
	visible_texts = filter(tag_visible, texts)  
	text = u"\n".join(t.strip() for t in visible_texts)
	text = text.lstrip().rstrip()
	text = text.split(',')
	clean_text = ''
	for sen in text:
		if sen:
			sen = sen.rstrip().lstrip()
			clean_text += sen+','

	clean_text = clean_text.lower()

	vis_text = [button.text for button in soup.select('button')]
	text = u"\n".join(t.strip() for t in vis_text)
	text = text.lstrip().rstrip()
	text = text.split(',')
	clean_text2 = ''
	for sen in text:
		if sen:
			sen = sen.rstrip().lstrip()
			clean_text2 += sen+','

	clean_text2 = clean_text2.lower()
	clean_text = clean_text + clean_text2

	return clean_text

def textParse(file):
	with open(file, "r") as f:
		soup = BeautifulSoup(f, "html.parser")

	# kill all style elements
	for style in soup(["style"]):
	    style.extract()    # rip it out

	# get text
	# text1 = soup.get_text()
	text1 = getHTML(soup)
	text2, links = getJS(soup)
	text = text1 + text2
	text = cleaner(text1) + "\n" + cleaner(text2)
	# print(f"These are texts:{text}\n")
	# print(f"These are embedded texts:{text2}\n")
	# print(f"These are embedded links: {links}\n")
	return [text, links]

def textParse2(filename):
	with open(filename, "r") as f:
		doc = BeautifulSoup(f, "html.parser")
	# Modify tags and save html
	tags = doc.find_all("input", type = "text")
	for tag in tags:
		tag['placeholder'] = "I changed You!"

	file = open("Upload/changed.html", "w", encoding="utf-8")
	file.write(str(doc))
	file.close()
	return 'PASSED'

def textParse3(filename):
	with open(filename, "r") as f:
		soup = BeautifulSoup(f, "html.parser")

	# kill all script and style elements
	for script in soup(["script", "style"]):
	    script.extract()    # rip it out

	# get text
	text = cleaner(soup.get_text())

	return text




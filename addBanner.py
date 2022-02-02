
from bs4 import BeautifulSoup

def readFile(file):
	f = open(file, "r")
	txt = f.read()
	f.close()
	return txt

def augment(doc, subgoal, action, violations):
	ref = readFile("templates/Banner/head.txt")
	body = readFile("templates/Banner/banner.txt")
	body = body.replace("{SUBGOAL}", subgoal)
	body = body.replace("{ACTION}", action)
	body = body.replace("{VIOLATIONS}", violations)

	x, y = doc.find("</head>"), doc.find("<body>")+ 6

	doc = doc[:x] + ref + "\n" + doc[x: y] + "\n" + body + doc[y:]

	return doc


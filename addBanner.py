
from bs4 import BeautifulSoup

def readFile(file):
	f = open(file, "r")
	doc = BeautifulSoup(f, "html.parser")
	f.close()
	return str(doc)

def augment(subgoal, action, violations, var):
	# ref = readFile("templates/Banner/head.txt")
	# body = readFile("templates/Banner/banner.txt")
	subgoal = subgoal.replace("\n", "<br>")
	action = action.replace("\n", "<br>")
	violations = violations.replace("\n", "<br>")

	body = readFile("templates/banner.html")
	body = body.replace("{SUBGOAL}", subgoal)
	body = body.replace("{ACTION}", action)
	body = body.replace("{VIOLATIONS}", violations)
	f = open(f"static/banner{var}.html", "w", encoding="utf-8")
	f.write(body)
	f.close()


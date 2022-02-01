from CheckRules import CheckRules
from gensim.summarization import keywords
import re
import spacy
from collections import Counter
import textParser
from bs4 import BeautifulSoup

# This file runs each of the rules for each URL in the input/output file

def LinkParser(file):
    if file:
        try:
            with open(file, "r") as f:
                doc = BeautifulSoup(f, "html.parser")
        except:
            return -1
    # Extract all links from page
    links = doc.find_all("a")
    doc2 = str(doc)
    style = ' STYLE="background-color: rgb(255,255,0)" '
    res = []
    # Parse Extracted Links
    regex = r"(?i)\b((?:http[s]?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    for l in range(len(links)):
        link = links[l]
        alias = link.string
        if alias:
            alias = alias.strip()

        if (alias and re.match(regex, alias)):
            x = str(link)
            aug_link = x[:2] + style + x[2:]
            doc2 = doc2.replace(x, aug_link)
            print(alias)
            res.append(link)
    file = open("templates/Highlight/changed.html", "w", encoding="utf-8")
    file.write(doc2)
    file.close()
    # print(doc2)
    return res

def MainProcess(usecase, subgoal, action, filename):
    report = ""

    #Loading the English model for spaCy
    nlp = spacy.load('en_core_web_sm')

    res = 0
    C = CheckRules()

    # List of DOM words to exclude from keywords
    DOM_words = ['window', 'document', 'header', 'form', 'link', 'field', 'tab', 'button', 'checkbox', 'icon', 'data', 'information']

    # Getting Keywords from subgoal and action by extracting nouns
    subgoals = nlp(subgoal)
    actions = nlp(action)
    keywords_S = []
    keywords_A = []
    txt = textParser.textParse(filename)

    for token in subgoals:
        if (token.pos_ == 'NOUN' or token.pos_ == 'ADJ') and (str(token) not in DOM_words): #or (token.pos_ == 'NOUN'):
            keywords_S.append(token.text)

    for token in actions:
        if (token.pos_ == 'NOUN' or token.pos_ == 'ADJ') and (str(token) not in DOM_words):
            keywords_A.append(token.text)

    report = f'\nURL of webpage evaluated: {filename[7:]}\nUse Case: {usecase}\nSubgoal: {subgoal}\nAction: {action}\n'
    
    # Rule 1 starts here - tokens present in the page or not
    # print the keywords S and A if violated
    result_1_S = C.checkRule1(keywords_S, txt)
    result_1_A = C.checkRule1(keywords_A, txt)
    if (result_1_S==1 and result_1_A==1) or (keywords_A == [] and keywords_S == []):
        report = report + "\nRule 1 not violated.\n"
    else:
        report = report + "\nRule 1 violated: Keywords not found on the webpage.\n"
        report = report + f"\nSubgoal keywords: {keywords_S}, Action Keywords: {keywords_A}\n"

    print("Rule 1")

    # #Rule 3 starts here - Link label exists or not
    # Highlight links which donot have label
    # Link labels will be checked
    result_3 = LinkParser(filename)
    if result_3 == -1:
        report = report + "No Links Found"
    elif len(result_3) > 0:
        report = report + "\nRule 3 violated: Link is not labelled. Click on Results to view highlighted errors\n"
    else:
        report= report + "\nRule 3 not violated. Results show the input html in this case.\n"
    print("Rule 3")
    return report


# LinkParser("current_html.html")

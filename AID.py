from CheckRules import CheckRules
from gensim.summarization import keywords
import re
import spacy
from collections import Counter
import textParser
from bs4 import BeautifulSoup

import addBanner

# Remove all tags in the region to finally get texts in the region
def processRegion(region):
    X = re.findall(r"\<.*?\>", region)
    for c in X:
        region = region.replace(c, "")
    region = region.strip()
    # print(f"This is the region: {region}, {len(region)}")
    return region

# Find the region using the text in the immediate parent
def findRegion(link):
    parent = link.parent
    s = str(parent)
    return processRegion(s)

# This file runs each of the rules for each URL in the input/output file

def LinkParser(file, emlinks):
    if file:
        try:
            with open(file, "r") as f:
                doc = BeautifulSoup(f, "html.parser")
        except:
            return ["", -1, ""]
    # Extract all links from page
    links = doc.find_all("a")
    # print(doc)
    doc2 = str(doc)
    style = ' STYLE="background-color: rgb(255,255,0)" '
    res = []
    res2 = []
    emres = ""
    # Parse Extracted Links
    regex = r"(?i)\b((?:http[s]?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    for l in range(len(links)):
        link = links[l]
        alias = link.string
        title = link.get("title")
        if alias:
            alias = alias.strip()
        if title:
            title = title.strip()
        if (alias and re.match(regex, alias)) or (title and re.match(regex, title)): 
            # print(f"This is alias: {alias}, {len(alias)}")
            # Rule 3 a: Link has no label and no region text
            # if len(findRegion(link)) <= len(alias):
            #     style = ' STYLE="background-color: rgb(255,0,0)" '
            # else:
            #     style = ' STYLE="background-color: rgb(255,255,0)" '
            x = str(link)
            aug_link = x[:2] + style + x[2:]
            doc2 = doc2.replace(x, aug_link)
            # print(alias)
            res.append(link)
    # print(doc2)

    if emlinks:
        # print("# Embedded Links ->", len(emlinks))
        # Embedded Links
        for l in range(len(emlinks)):
            link = emlinks[l]
            alias = link.string
            title = link.get("title")
            # print(title)
            if alias:
                alias = alias.strip()
            if title:
                title = title.strip()
                # print(title)
            if (alias and re.match(regex, alias)) or (title and re.match(regex, title)):
                res2.append(link.get("href"))
            if alias == "None" and title == "None":
                res2.append(link.get("href"))

        if res2:
            emres = "The following embedded links also violate Rule 3\n"
            for i in range(len(res2)):
                t = f"{i+1}. {res2[i]}\n"
                emres += t

    # res = res.extend(res2)
    return [doc2, res, emres]

def addColor(text, color):
    txt = f'<p style="color: {color}">{text}</p>'
    return txt

def MainProcess(usecase, subgoal, action, filename, var):
    report = ""
    flag = 0
    flags = []

    #Loading the English model for spaCy
    nlp = spacy.load('en_core_web_sm')

    res = 0
    C = CheckRules()

    # List of DOM words to exclude from keywords
    DOM_words = ['window', 'document', 'header', 'form', 'link', 'field', 'tab', 'button', 'checkbox', 'icon', 'data', 'information', 'webpage', 'page', 'website']

    # Getting Keywords from subgoal and action by extracting nouns
    subgoals = nlp(subgoal)
    actions = nlp(action)
    keywords_S = []
    keywords_A = []
    txt, emlinks = textParser.textParse(filename)

    for token in subgoals:
        if (token.pos_ == 'PROPN' or token.pos_=='NOUN' or token.pos_ == 'ADJ') and (str(token) not in DOM_words): #or (token.pos_ == 'NOUN'):
            keywords_S.append(token.text)

    for token in actions:
        if (token.pos_ == 'PROPN' or token.pos_=='NOUN' or token.pos_ == 'ADJ') and (str(token) not in DOM_words):
            keywords_A.append(token.text)

    # report = f'\nURL of webpage evaluated: {filename[7:]}\nUse Case: {usecase}\nSubgoal: {subgoal}\nAction: {action}\n'
    
    # Rule 1 starts here - tokens present in the page or not
    # print the keywords S and A if violated
    result_1_S = C.checkRule1(keywords_S, txt)
    result_1_A = C.checkRule1(keywords_A, txt)


    if (result_1_S==1 and result_1_A==1) or (keywords_A == [] and keywords_S == []):
        flags.append("Not Violated")
        report = report + addColor("\nRule 1 not violated.\n", "green")
    else:
        flag = 1
        flags.append("Violated")
        report = report + addColor("\nRule 1 is violated: Some keywords Abi was looking for, were not found on the webpage.\n", "orange")
        report = report + f"The subgoal keywords for this instance were: {keywords_S}, and the action keywords were: {keywords_A}.\n"

    print("Rule 1")

    if (var==2):
        result_2 = C.checkRule2(filename, keywords_A)
        if result_2==1:
            flag = 1
            flags.append("Violated")
            report = report + addColor("\n Rule 2 is violated: Keywords from the previous link-label is not present on the current page.", "orange")
        else:
            flags.append("Not Violated")
            report = report + addColor("\n Rule 2 not violated.", "green")
    else:
        flags.append("Not Applicable")
        report = report + addColor("\n Rule 2 not applicable since it is a before-action webpage.", "green")

    # #Rule 3 starts here - Link label exists or not
    # Highlight links which donot have label
    # Link labels will be checked
    document, result_3, emres = LinkParser(filename, emlinks)
    # print(filename)
    print("Rule 2")
    
    if result_3 == -1:
        flags.append("No Links on page")
        report = report + "\nNo Links Found on the webpage.\n"
    elif len(result_3) > 0:
        flag = 1
        flags.append("Violated")
        report = report + addColor("\nRule 3 violated: Links are not labelled. Please refer to the right side to see the highlighted links (in yellow).\n", "orange")
        if emres:
            report = report + addColor(emres, "orange")
    else:
        flags.append("Not Violated")
        report= report + addColor("\nRule 3 not violated. Results show the input html in this case.\n", "green")
    print("Rule 3")
    
    report = report + "\n\nRead below for descriptions of each rule: \n\nRule 1: Keywords from subgoals and associated actions should be present on the webpage. \nThe wording of the subgoal serves as the information that Abi seeks, and the words from actions serve as cues to direct Abi to a UI action. Without such cues, Abi would face difficulty finding all the information they need. \n"
    report = report+"\nRule 2: Linked pages should contain keywords from link labels. \n On clicking a link, the destination page should offer cues to help Abi’s understand that they have reached the right place. If a project page fails to use words similar to what a link label hinted at, Abi could get confused. \n"
    report = report + "\nRule 3: Links should be labeled with a keyword or phrase. Abi clicks on a link only after gathering enough information and planning their next step. Labeled links provide Abi with information about the webpage they are supposed to visit.\n"
    f = open(f"static/changed{var}.html", "w", encoding="utf-8")
    # printcheck = "CHANGED!!!"
    # file.write(printcheck)

    addBanner.augment(subgoal, action, report, var)
    f.write(document)
    f.close()

    return report, flag, flags

# MainProcess("usecase", "subgoal", "action", "a.html")

# LinkParser("a.html")

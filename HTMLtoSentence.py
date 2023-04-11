import os
import openpyxl
from bs4 import BeautifulSoup
import csv
import re

def tag_visible(self, element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    if re.match(r"[\n]+",str(element)): return False
    return True

# # Get all HTML files in a directory
html_files = ["/Users/chattera/Downloads/HTMLfiles/CanvasHTMLoutput4.html", "/Users/chattera/Downloads/HTMLfiles/CanvasHTMLoutput5.html", "/Users/chattera/Downloads/HTMLfiles/CanvasHTMLoutput6.html", "/Users/chattera/Downloads/HTMLfiles/CanvasHTMLoutput7.html", "/Users/chattera/Downloads/HTMLfiles/CanvasHTMLoutput8.html", "/Users/chattera/Downloads/HTMLfiles/CanvasHTMLoutput9.html"]
output_file = "sentences.csv"

# Open the CSV file for writing
with open(output_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)

    for pathname in html_files:
        print(f"Extracting sentences from {pathname}...")

        # Load the HTML file
        with open(pathname, "r", encoding="utf-8") as html_file:
            soup = BeautifulSoup(html_file, "html.parser")

            # Extract all visible sentences from the HTML file
            visible_sentences = []
            for sentence in soup.get_text().split("."):
                print(sentence)
                sentence = sentence.strip()
                # if sentence and sentence[0].isalpha() and sentence[-1] in [".", "?", "!"]:
                if sentence not in visible_sentences and sentence not in ["[Loading...]", "(click to view)"]:
                    visible_sentences.append(sentence)

                # Write the sentences to the CSV file
            for sentence in visible_sentences:
                writer.writerow([sentence])
                print(sentence)

f.close()

print(f"Sentences saved.")

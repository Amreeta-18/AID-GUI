# Import Libraries
from bs4 import BeautifulSoup
import requests
import re

# Remove all tags in the region to finally get texts in the region
def processRegion(region):
	X = re.findall(r"\<.*?\>", region)
	for c in X:
		region = region.replace(c, "")
	return region

# Find the region using the text in the immediate parent
def findRegion(link):
	parent = link.parent
	s = str(parent)
	return processRegion(s)

# Utility Function
def cleaner(s):
	s = s.replace("\n", "")
	s = s.replace(" ", "")
	return s

def parseLink(url = None, file= None):

	# Read HTML from URL or from downloaded file
	# Include dead end checker here - for links outside domain
	if url:
		try:
			result = requests.get(url).text

			doc = BeautifulSoup(result, "html.parser")
		except:
			return {}

	elif file:
		try:
			with open(file, "r") as f:
				doc = BeautifulSoup(f, "html.parser")
		except:
			return {}
	else:
		return {}

	# Extract all links from page
	links = doc.find_all("a")

	# Snip the html part
	doc = doc.find("html")

	# Convert HTML structure to string
	doc2 = str(doc)

	# Remove Head tag
	while doc2.find("<head>")!= -1:
		s1, s2 = doc2.find("<head>"), doc2.find("</head>")
		doc2 = doc2[s2+7:]

	# Remove images
	while doc2.find("<img") != -1:
		s = doc2.find("<img")
		for i in range(s, len(doc2)):
			if doc2[i] == ">":
				break
		doc2 = doc2[:s] + doc2[i+1:]
		
	# Remove JavaScript		
	while doc2.find("<script") != -1:
		s1, s2 = doc2.find("<script"), doc2.find("</script>")

		doc2 = doc2[:s1] + doc2[s2+9:]

	# Find the preceeding text info for a link
	def findPrev(link, head):
		# Find the index of the link in the document
		ind = doc2.find(link)
		# Extract the region between head and obtained index
		# Append the link at the end
		region = doc2[head:ind] + link
		# Process the region to get rid of the tags
		region = processRegion(region)
		# Point the Head after the a tag corresponding to the present link
		for i in range(ind,len(doc2)-3):
			if doc2[i] == "<" and doc2[i+1] == "/" and doc2[i+2] == "a":
				break
		head = i+4
		# Return the region and the head
		return region, head

	# Nodes of the page
	nodes = {}
	# Head pointer pointing to the start of the document
	head = 0

	# Parse Extracted Links
	for l in range(len(links)):
		link = links[l]
		# If no alias then this is None
		alias = link.string

		# Find the text preceeding the link and update the head
		prev, head = findPrev(str(link), head)
		# Find the region in the link area
		reg = findRegion(link)
		# If link is a list item, fetch the prev region from the first list item
		if link.parent.name == "li" and links[l-1].parent.name == "li" and cleaner(prev) == cleaner(reg):
			k = str(l) + " " + str(links[l-1]['href'])
			prev = nodes[k]['prev']

		# Generate key for the graph - Has a counter attached to deal with multiple occurances of same link
		key = str(l+1) + " " + str(link['href'])
		# Store the alias, preceeding region, and current area as values of the node
		values = {'alias':alias, 'prev':prev, 'region':reg}
		# Add node
		if key not in nodes:
			nodes[key] = values

	return nodes

def txtForm(url = None, file= None):
	if url and file:
		return ""
	if url:
		nodes = parseLink(url = url)
	elif file:
		nodes = parseLink(file=file)
	else:
		print("Empty Parameters")
		return ""
	f = open("Links.txt", "w")
	f.write("------Source------\n")
	f.write(f"Link: {file}\n")
	f.write("-----Destinations-------\n")
	cnt = 1
	for n in nodes:
		f.write("\n------------\n")
		f.write(f"Destination {cnt}:\n")
		cnt += 1
		f.write(f"\nKey: {n}")
		f.write(f"\nLink Label: {nodes[n]['alias']}")
		f.write(f"\nPreceeding Text: {nodes[n]['prev']}")
		f.write(f"\nRegion: {nodes[n]['region']}")
		f.write("\n------------\n")

	f.close()
	return f"PASSED"

def csvForm(url = None, file = None):
	if url and file:
		return ""
	if url:
		nodes = parseLink(url = url)
	elif file:
		nodes = parseLink(file=file)
	else:
		print("Empty Parameters")
		return ""
	f = open("Links.csv", "w")
	f.write("S.No, Link, Link Label, Preceeding, Region\n")
	cnt = 1
	for n in nodes:
		link = n[n.find(" ") + 1:]
		alias = nodes[n]['alias']
		prev =  nodes[n]['prev']
		region = nodes[n]['region']
		if alias:
			alias = alias.replace("\n", " ")
			alias = alias.replace(",", " ")
		if prev:
			prev = prev.replace("\n", " ")
			prev = prev.replace(",", " ")
		if region:
			region = region.replace("\n", " ")
			region = region.replace(",", " ")
		f.write(f"{cnt}, {link}, {alias}, {prev}, {region}\n")
		f.write("\n")
		cnt += 1
	f.close()

if __name__ == "__main__":
	src_file = "Upload/index3.html"
	src_url = ""
	# txtForm(file = src_file)
	# csvForm(file = src_file)
	# print("Done")
	nodes = parseLink(file = src_file)
	x = list(nodes.keys())
	print(nodes[x[0]])

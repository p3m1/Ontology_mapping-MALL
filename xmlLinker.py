import xml.etree.ElementTree as ET
import unicodedata

#Open the xml file
raw_xml = open('homemade_v2.xml',  'r')

#parse the raw xml
tree = ET.parse(raw_xml)
#get the root element, thus, the tree
root = tree.getroot()

#For now, this is only an example of what we can do
print (root.tag)
for child in root: 
	print child.tag, child.attrib
	for subchild in child: 
		text = subchild.text
		#this part of the code garantees that all the information is in string format
		if (isinstance(text,unicode)):
			#this way, we don't lose any information 
			unicodedata.normalize('NFKD', text)
		else:
			text = str(text)
		print (subchild.tag).encode('utf-8'), ":", subchild.text
import unicodedata
import xmltodict
from lxml import etree

#Open the xml file
raw_xml = open('homemade_v2.xml',  'r')

#Converts the xml to a dict 
ontology = xmltodict.parse(raw_xml)

related = {}


#Exemplo de uso que pode ser util para nos
for relation in ontology['Ontology']['Relation']:
	aux = []
	found = False
	for relation2 in ontology['Ontology']['Relation']:
		if (relation['relationName'] == relation2['generalizations'] and relation['relationName'] != 'relatedTo'):
			aux.append(int(relation2['@id']))
			found = True
			#print "'", relation2['relationName'], relation2['@id'], "'","can be generalized as","'",relation['relationName'], relation['@id'], "'"
	if (found):
		related[int(relation['@id'])] = aux


print related 
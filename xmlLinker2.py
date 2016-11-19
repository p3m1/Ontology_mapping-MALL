import unicodedata
import xmltodict

#Open the xml file
raw_xml = open('homemade_v2.xml',  'r')

#Converts the xml to a dict 
ontology = xmltodict.parse(raw_xml)

#Exemplo de uso que pode ser util para nos
for relation in ontology['Ontology']['Relation']:
	for relation2 in ontology['Ontology']['Relation']:
		if (relation['relationName'] == relation2['generalizations'] and relation['relationName'] != 'relatedTo'):
			print "'", relation2['relationName'], relation2['@id'], "'","can be generalized as","'",relation['relationName'], relation['@id'], "'"
	
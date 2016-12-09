import unicodedata
import xmltodict
from lxml import etree
import xml.etree.ElementTree as ET

#Open the xml file
raw_xml = open('homemade_v2.xml',  'r')

#Converts the xml to a dict 
ontology = xmltodict.parse(raw_xml)

raw_xml.close()
raw_xml = open('homemade_v2.xml',  'r')

tree = ET.parse(raw_xml)
root = tree.getroot()

related = {} # chave eh generalizacao de elementos na lista


#Exemplo de uso que pode ser util para nos
for relation in ontology['Ontology']['Relation']:
	aux = []
	found = False
	for relation2 in ontology['Ontology']['Relation']:
		for gen in str(relation2['generalizations']).split():
			if (relation['relationName'] == gen and relation['relationName'] != 'relatedTo'):
				aux.append(int(relation2['@id']))
				found = True
				#print "'", relation2['relationName'], relation2['@id'], "'","can be generalized as","'",relation['relationName'], relation['@id'], "'"
		if (found):
			related[int(relation['@id'])] = aux


for generalization, especializations in related.items():	# coloca um relationRef onde tem uma generalizacao que eh relationName
	for relation in root: 
		for especialization in especializations: 
			if (relation.attrib['id'] == str(especialization)):		# ele eh uma especializacao
				aux = ET.SubElement(relation[4], 'relationRef', {'id':str(generalization)})

outFile = open('homemade_linked.xml', 'w')
tree.write(outFile)


		

#print related 

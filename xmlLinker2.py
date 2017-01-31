#!/usr/bin/env

import unicodedata
import xmltodict
from lxml import etree
import xml.etree.ElementTree as ET

#Open the xml file
raw_xml = open('ontology.xml',  'r')

#Converts the xml to a dict 
ontology = xmltodict.parse(raw_xml)

raw_xml.close()
raw_xml = open('ontology.xml',  'r')

tree = ET.parse(raw_xml)
root = tree.getroot()

generalizations = {} # chave eh generalizacao de elementos na lista
mutex = {}
inverse = {}
rel_index = -1

#Exemplo de uso que pode ser util para nos
for relation in ontology['Ontology']['Relations']['Relation']:
	rel_index += 1
	auxg = []
	auxm = []
	auxinv = []
	foundgen = False
	foundmut = False
	foundinverse = False


	for relation2 in ontology['Ontology']['Relations']['Relation']:
		for gen in str(relation2['generalizations']).split(): 	#looking for generalizations
			if (relation['relationName'] == gen and relation['relationName'] != 'relatedTo'):
				auxg.append(int(relation2['@id']))
				foundgen = True

		for mut in str(relation2['mutexExceptions']).split():
			if (relation['relationName'] == mut): 	#looking for mutexExceptions
				auxm.append(int(relation2['@id']))
				foundmut = True

		for inv in str(relation2['inverse']).split():
			if (relation['relationName'] == inv):	#looking for inverses
				auxinv.append(int(relation2['@id']))
				foundinverse = True
				
		if (foundgen):
			generalizations[int(relation['@id'])] = auxg

		if (foundmut): 
			mutex[int(relation['@id'])] = auxm

		if (foundinverse):
			inverse[int(relation['@id'])] = auxinv

	for category in ontology['Ontology']['Categories']['Category']: 	#looking for the categories in the category xls
		if (category['categoryName'] == relation['domain']): 
			aux = ET.SubElement(root[0][rel_index][5], 'categoryRef', {'id':category['@id']})
		if (category['categoryName'] == relation['range']): 
			aux = ET.SubElement(root[0][rel_index][6], 'categoryRef', {'id':category['@id']})



for generalization, especializations in generalizations.items():	# coloca um relationRef onde tem uma generalizacao que eh relationName
	for relation in root[0]: 
		for especialization in especializations: 
			if (relation.attrib['id'] == str(especialization)):		# ele eh uma especializacao
				aux = ET.SubElement(relation[4], 'relationRef', {'id':str(generalization)})


for origin, mutexExceptions in mutex.items(): 
	for relation in root[0]: 
		for mutexException in mutexExceptions:
			if (relation.attrib['id'] == str(mutexException)): 
				aux = ET.SubElement(relation[11], 'relationRef', {'id':str(origin)})

for origin, inverses in inverse.items(): 
	for relation in root[0]: 
		for inversex in inverses:
			if (relation.attrib['id'] == str(inversex)): 
				aux = ET.SubElement(relation[13], 'relationRef', {'id':str(origin)})


outFile = open('homemade_linked.xml', 'w')
tree.write(outFile)


		

#print related 
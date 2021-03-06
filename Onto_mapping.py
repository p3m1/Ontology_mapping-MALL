#!/usr/bin/env

import unicodedata
import xmltodict
from lxml import etree
import xml.etree.ElementTree as ET
from xlrd import open_workbook,XL_CELL_TEXT
import xlwt 
from collections import OrderedDict

def create_xml(rel_path ='./data/relations.xls', cat_path = './data/categories.xls' ): 

	# Opens the xls file
	relations = open_workbook(rel_path)
	categories = open_workbook(cat_path)

	# selects the correct sheet
	sheet = relations.sheet_by_index(0)
	sheetcat = categories.sheet_by_index(0)


	# Define the root element of the xml file
	root = etree.Element('Ontology')
	relation = etree.SubElement(root, 'Relations')
	category = etree.SubElement(root, 'Categories')


	# Creating all the fields of the ontology
	# walks through the rows
	for j in range(1,sheet.nrows): 
		rel = etree.SubElement(relation, 'Relation')
		rel.set('id', str(j))
		# walks through the columns 
		for i in range(sheet.ncols):
			child = sheet.cell_value(0,i) # create the fields 
			child = etree.SubElement(rel, child)
			value = sheet.cell(j,i).value
			if (isinstance(value, int) or isinstance(value,float)): 
				# converts all data to string
				value = int(value)
				value = str(value)
			else:
				# using the right encoding
				value.encode('utf8')
			child.text = value 
			# fill all the fields 

	for j in range(1,sheetcat.nrows): 
		rel = etree.SubElement(category, 'Category')
		rel.set('id', str(j))
		for i in range(sheetcat.ncols):
			child = sheetcat.cell_value(0,i) # create the fields
			child = etree.SubElement(rel, child)
			value = sheetcat.cell(j,i).value
			if (isinstance(value, int) or isinstance(value,float)): 
				# converts all data to string
				value = int(value)
				value = str(value)
			else:
				value.encode('utf8')
			child.text = value 			
			

	# creates the root element of the xml tree
	root_tree = etree.ElementTree(root)

	# saves the output file
	outFile = open('./data/ontology.xml', 'w')
	root_tree.write(outFile)




def linker(filename = './data/ontology.xml'): 	# create the references in the xml file

	#Open the xml file
	raw_xml = open(filename,  'r')

	#Converts the xml to a dict 
	ontology = xmltodict.parse(raw_xml)

	raw_xml.close()
	raw_xml = open(filename,  'r')

	tree = ET.parse(raw_xml)
	root = tree.getroot()

	generalizations = {} 	# keep the generalizations IDs
	mutex = {}				# keep the mutexExceptions IDs
	inverse = {}			# keep the inverse IDs
	rel_index = -1
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


		# creates all the categories references
		for category in ontology['Ontology']['Categories']['Category']: 	
			if (category['categoryName'] == relation['domain']): 
				aux = ET.SubElement(root[0][rel_index][5], 'categoryRef', {'id':category['@id']})
			if (category['categoryName'] == relation['range']): 
				aux = ET.SubElement(root[0][rel_index][6], 'categoryRef', {'id':category['@id']})



	# this part of the code creates all the relation references

	for generalization, especializations in generalizations.items():	
		for relation in root[0]: 
			for especialization in especializations: 
				if (relation.attrib['id'] == str(especialization)):		
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



	outFile = open('./data/ontology_linked.xml', 'w')
	tree.write(outFile)


def create_xls(input_file='./data/ontology.xml'):

	# open the xml file 
	linked_xml = open(input_file, 'r')

	# create the workbooks
	relations_file = xlwt.Workbook()
	categories_file = xlwt.Workbook()

	# parse the xml
	ontology = xmltodict.parse(linked_xml)


	# create a sheet in the workbook
	relations_xls = relations_file.add_sheet('relations_tsv _ Table 1')
	categories_xls = categories_file.add_sheet('categories_tsv _ Table 1')


	# creating the relations.xls file 
	# create the header cells
	i = 0
	for info in ontology['Ontology']['Relations']['Relation'][1].keys() : # total de colunas do relations.xls
		if (info != '@id'): 
			relations_xls.write(0, i, info)
			i += 1

	# fill the xls file

	relr_index = 1
	relc_index = -1
	for relation in ontology['Ontology']['Relations']['Relation']: # walks through the rows
		relations_xls.write(relr_index, relc_index+1, relation['relationName'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['humanFormat'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['populate'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['visible'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['generalizations'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['domain'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['range'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['domainWithinRange'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['rangeWithinDomain'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['antireflexive'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['antisymmetric'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['mutexExceptions'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['knownNegatives'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['inverse'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['seedInstances'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['seedExtractionPatterns'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['nrOfValues'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['nrOfInverseValues'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['requiredForDomain'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['requiredForRange'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['queryString'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['editDate'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['author'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['curator'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['description'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['freebaseID'])
		relc_index+=1
		relations_xls.write(relr_index, relc_index+1, relation['comment'])

		relc_index=-1
		relr_index+=1

	# creating the output file 
	out_xls = open('./data/made_relations.xls', 'w')
	# saving the relations.xls file
	relations_file.save(out_xls)
	out_xls.close()
	# relations.xls complete


	# creating the categories.xls file
	# create the header cells
	i = 0
	for info in ontology['Ontology']['Categories']['Category'][1].keys() : # total de colunas do relations.xls
		if (info != '@id'): 
			categories_xls.write(0, i, info)
			i += 1

	# fill the xls file

	catr_index = 1
	catc_index = 0
	for category in ontology['Ontology']['Categories']['Category']: # walks through the rows
		categories_xls.write(catr_index, catc_index, category['categoryName'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['englishName'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['humanFormat'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['populate'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['visible'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['generalizations'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['mutexExceptions'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['knownNegatives'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['instanceType'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['seedInstances'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['seedExtractionPatterns'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['conceptSynonyms'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['queryString'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['editDate'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['author'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['curator'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['description'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['freebaseID'])
		catc_index+=1
		categories_xls.write(catr_index, catc_index, category['comment'])
		catc_index = 0
		catr_index += 1
		
		

	# creating the output file 
	out_xls = open('./data/made_categories.xls', 'w')
	# saving the relations.xls file
	categories_file.save(out_xls)
	out_xls.close()


def main():
	create_xml()
	linker()
	create_xls()


if __name__ == '__main__':
	main()

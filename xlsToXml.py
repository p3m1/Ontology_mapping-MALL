from xlrd import open_workbook,XL_CELL_TEXT
from lxml import etree

#Abre a leitura do arquivo xls
relations = open_workbook('relations.xls')
categories = open_workbook('categories.xls')
#Seleciona o sheet desejado desse arquivo
sheet = relations.sheet_by_index(0)
sheetcat = categories.sheet_by_index(0)


#Define o root do arquivo xml
root = etree.Element('Ontology')
relation = etree.SubElement(root, 'Relations')
category = etree.SubElement(root, 'Categories')
#Comentario no xml
comment1 = etree.Comment('Teste de criacao do XML')
root.append(comment1)

#Adicionando as childs ou SubElementos do root
#for mais externo percorre as linhas 
#O for mais interno percorre todas as colunas adicionando cada celula como child do root do xml
for j in range(1,sheet.nrows): 
	rel = etree.SubElement(relation, 'Relation')
	rel.set('id', str(j))
	for i in range(sheet.ncols):
		child = sheet.cell_value(0,i) #Fixo em 0 para criar as tags
		child = etree.SubElement(rel, child)
		value = sheet.cell(j,i).value
		if (isinstance(value, int) or isinstance(value,float)): 
			#se for int ou float, basta converter para string
			value = str(value)
		else:
			#em outro caso, eu indico qual codificacao
			value.encode('utf8')
		child.text = value 
		#WARNING: temos um problema na codificacao de caracteres
		#Percorre as linhas diferentes de zero, adicionando como informacao para cada tag previamente criada. 

for j in range(1,sheetcat.nrows): 
	rel = etree.SubElement(category, 'Category')
	rel.set('id', str(j))
	for i in range(sheetcat.ncols):
		child = sheetcat.cell_value(0,i) #Fixo em 0 para criar as tags
		child = etree.SubElement(rel, child)
		value = sheetcat.cell(j,i).value
		if (isinstance(value, int) or isinstance(value,float)): 
			#se for int ou float, basta converter para string
			value = str(value)
		else:
			#em outro caso, eu indico qual codificacao
			value.encode('utf8')
		child.text = value 			
		

#Coloca o root na arvore
root_tree = etree.ElementTree(root)




#Salva o arquivo xml
outFile = open('ontology.xml', 'w')
root_tree.write(outFile)

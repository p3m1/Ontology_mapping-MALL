from xlrd import open_workbook,XL_CELL_TEXT
from lxml import etree

#Abre a leitura do arquivo xls
relations = open_workbook('relations.xls')
#Seleciona o sheet desejado desse arquivo
sheet = relations.sheet_by_index(0)

#Define o root do arquivo xml
root = etree.Element('Relation')
#Comentario no xml
comment1 = etree.Comment('Teste de criacao do XML')
root.append(comment1)

#Adicionando as childs ou SubElementos do root
#O for percorre todas as colunas da primeira linha adicionando cada celula como child do root do xml
for j in range(sheet.nrows):
	for i in range(sheet.ncols):
		child = sheet.cell_value(0,i)
		child = etree.SubElement(root, child)
		if (j+1 < sheet.nrows):
			child.text = repr(sheet.cell(j+1,i).value)
		

#Coloca o root na arvore
root_tree = etree.ElementTree(root)


#Ainda nao faz merda nenhuma
for i in range(sheet.nrows):
	for j in range(sheet.ncols):
		 sheet.cell_value(i,j)


#Salva o arquivo xml
outFile = open('homemade_v2.xml', 'w')
root_tree.write(outFile)

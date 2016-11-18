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
#for mais externo percorre as linhas 
#O for mais interno percorre todas as colunas adicionando cada celula como child do root do xml
for j in range(sheet.nrows):
	for i in range(sheet.ncols):
		if (j+1 < sheet.nrows):
			child = sheet.cell_value(0,i) #Fixo em 0 para criar as tags
			child = etree.SubElement(root, child)
			value = sheet.cell(j+1,i).value
			if (isinstance(value, int) or isinstance(value,float)): 
				#se for int ou float, basta converter para string
				value = str(value)
			else:
				#em outro caso, eu indico qual codificacao
				value.encode('utf8')
			child.text = value 
			#WARNING: temos um problema na codificacao de caracteres
			#Percorre as linhas diferentes de zero, adicionando como informacao para cada tag previamente criada. 
			
		

#Coloca o root na arvore
root_tree = etree.ElementTree(root)




#Salva o arquivo xml
outFile = open('homemade_v2.xml', 'w')
root_tree.write(outFile)

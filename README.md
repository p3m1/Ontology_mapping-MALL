# Ontology_mapping-MALL
A aplicação em desenvolvimento tem como objetivo mapear a ontologia utilizado pela NELL.

Listagem do repositório:
  - xlsToXml.py: script que converte tabelas xls em arquivos xml
  - xmlLinker2.py: script que faz as referências dentro do xml
  - Onto_mapping.py: script que reúne as funcionalidades acima e cria um novo arquivo xls a partir do xml
  - data: pasta que contem os arquivos necessários para o funcionamento
     - relations.xls: arquivo que contem as relações da ontologia
     - categories.xls: arquivo que contem as categorias da ontologia
     - ontology.xml: arquivo que contem a ontologia mapeada em um xml
     - ontology_linked.xml: arquivo que contem a ontologia já com as relações
     - made_relations.xls: arquivo de saída (gerado a partir do xml)
     - made_categories.xls: arquivo de saída (gerado a partir do xml)


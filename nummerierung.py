import codecs
from lxml import etree

# XML file to open 
source = "Armer_Heinrich/Digital/DAH_Edition_TEI.xml"

#New numbered File
new_file = "DAH_Edition_TEI_nummeriert.xml"

#Adds TEI-namespace to tag names
def tei(tag):
    return "{http://www.tei-c.org/ns/1.0}%s" % tag

def transform_xml_id_to_numbers(verse_xml_id):
	#Transforms the xml:id attribute to a list with three elements representing folio, side and column, each with a number
	sig,fol,ver,line_str,line = verse_xml_id.split('_')
	fol = fol.split('.')[0]
	folio, column = fol.split('-')
	folio = folio.replace('r','0')
	folio = folio.replace('v','1')
	column = column.replace('a','0')
	column = column.replace('b','1')
	column = column.replace('c','2')
	if "cont" in line:
		line = line.replace('cont','1')
	elif "a" in line: #for two strange veres in Myller
		line = line.replace('a','1')
	else:
		line = line + '0'
	verse_als_integer = [int(folio), int(column), int(line)]
	return verse_als_integer

def get_verses_numbers(witness, full_tree):
#Creates a list with all the verses (encoded in numbers) in their correct order
	verses = []
	signatur = witness.attrib['{http://www.w3.org/XML/1998/namespace}id']
	for rdg in full_tree.iter(tei('rdg')):
		if rdg.attrib['wit'] == '#' + str(signatur):
			if '{http://www.w3.org/XML/1998/namespace}id' in rdg.attrib:
				verse_xml_id = rdg.attrib['{http://www.w3.org/XML/1998/namespace}id']
				verse_als_integer = transform_xml_id_to_numbers(verse_xml_id)
				verses.append(verse_als_integer)
	verses.sort(key=lambda x: (x[0],x[1],x[2]))
	return verses

with codecs.open(source, 'r', 'utf-8') as f:
    full_tree = etree.parse(f)

all_verses_dict = {}
index = 0
for witness in full_tree.iter(tei('witness')):
	#Create a list with all the verses of all witnesses ordered
	all_verses_dict[witness.attrib['{http://www.w3.org/XML/1998/namespace}id']] = get_verses_numbers(witness, full_tree)
	index = index + 1
	
for witness in full_tree.iter(tei('witness')):
	signatur = witness.attrib['{http://www.w3.org/XML/1998/namespace}id']
	for rdg in full_tree.iter(tei('rdg')):
		if rdg.attrib['wit'] == '#' + str(signatur):
			if '{http://www.w3.org/XML/1998/namespace}id' in rdg.attrib:
				verse_xml_id = rdg.attrib['{http://www.w3.org/XML/1998/namespace}id']
				#Get the verse number in the number codes to be able to compare with the ordered lines, and assign as number
				coded_verse_number = transform_xml_id_to_numbers(verse_xml_id)
				for item in all_verses_dict[signatur]:
					if item == coded_verse_number:
						rdg.set('n', str(all_verses_dict[signatur].index(item)))


full_tree.write(new_file, encoding="UTF-8")
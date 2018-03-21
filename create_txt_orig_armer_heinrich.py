from lxml import etree
import re
import codecs

'''
THIS SCRIPT STRIPS THE XML ELEMENTS FROM THE SYNOPTIC TRANSCRIPTION AND RETURNS A .TXT FOR WACH WITNESS.
EACH VERSE IN A DIFFERENT LINE.
IT SELECTS THE EXPANDED VERSION AND WITHOUT MOST PALEOGRAPHICAL DIFFERENCES
'''

source = "/Users/gusriva/Dropbox/armer_heinrich/Digital/DAH_Edition_TEI.xml"
text_name = "armer_heinrich"
destination = "/Users/gusriva/Dropbox/armer_heinrich/Digital/plain_text/"


with codecs.open(source, "r", 'utf-8') as f:
    full_tree = etree.parse(f)


def tei(tag):
    return "{http://www.tei-c.org/ns/1.0}%s" % tag

def dive(elem):
    text = ""
    if elem.text:
        text = text + elem.text
    for child in elem:
        if child.tag == tei("choice") or child.tag == tei("expan") or child.tag == tei("ex") or child.tag == tei("hi") or child.tag == tei("corr") or child.tag == tei("reg"):
            text = text + dive(child)
    if elem.tail:
        text = text + elem.tail
    return text

def create_txt(full_tree):
    '''
    Creates txt files of all the witnesses in a TEI file. 
    Those files names are "text_witness" on the same location as this python script
    '''
    for wit in full_tree.iter(tei('witness')):
        witness = '#'+wit.attrib["{http://www.w3.org/XML/1998/namespace}id"]
        #Run the XSL to order the witness
        xslt = etree.parse("/Applications/XAMPP/xamppfiles/htdocs/konrad/XSLT/isolate_witness.xsl")
        transform = etree.XSLT(xslt)
        newdom = transform(full_tree, manuscript = etree.XSLT.strparam(witness))
        #Create the new file
        writing = ""
        for rdg in newdom.iter(tei('rdg')):
            if rdg.text:
                writing = writing + rdg.text
            for child in rdg:
                writing = writing + dive(child)
            if rdg.tail:
                writing = writing + rdg.tail
        #When the variable writing has the whole text, the following lines remove all the superfluos whitespaces and empty lines
        lines = re.findall(".+", writing)
        clean_lines = []
        for line in lines:
            clean_line = re.findall("\w+\s*",line)
            clean_line = "".join(clean_line)
            #regularisation
            clean_line = clean_line.replace("ſ","s")
            if len(clean_line) > 1:
                clean_lines.append(clean_line)
        final_text = "\n".join(clean_lines)


        #Created the file and writes the text. CHECK THE DIRECTORY TO WRITE IN!!
        with codecs.open(destination + text_name + "_" + witness + ".txt", "w", "utf-8") as new_file:
            new_file.write(final_text)

create_txt(full_tree)

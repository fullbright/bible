#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import re
import csv

class AbreviationConverter:
    class __AbreviationConverter:
        mydict = None
        longnamedict = None
        sectiondict = None
        # Write a constructor
        def __init__(self, arg):
            self.val = arg
            self.mydict = {}
            self.longnamedict = {}
            self.sectiondict = {}
            # Fill in the content of the csv file in arg
            with open(arg, mode='r') as infile:
                # Load the book abreviation, shortname in a dictionary
                reader = csv.reader(infile)
                self.mydict = dict((rows[11],rows[6]) for rows in reader)

            with open(arg, mode='r') as infile:
                # Load also the book abreviation, description in a dictionary
                reader = csv.reader(infile)
                self.longnamedict = dict((rows[11],rows[8]) for rows in reader)

            with open(arg, mode='r') as infile:
                # Load also the book abreviation, description in a dictionary
                reader = csv.reader(infile)
                self.sectiondict = dict((rows[11],rows[12]) for rows in reader)


        def __str__(self):
            return repr(self) + self.val
        def get_shortname(self,name):
            return self.mydict.get(name, "unknown")

        def get_longname(self,name):
            return self.longnamedict.get(name, "unknown")

        def get_section(self,name):
            return self.sectiondict.get(name, "unknown")


    instance = None

    def __init__(self, arg):
         if not AbreviationConverter.instance:
                AbreviationConverter.instance = AbreviationConverter.__AbreviationConverter(arg)
         else:
            AbreviationConverter.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def get_shortname(self, name):
        return AbreviationConverter.instance.get_shortname(name)

    def get_longname(self, name):
        return AbreviationConverter.instance.get_longname(name)

    def get_section(self, name):
        return AbreviationConverter.instance.get_section(name)


class ConcordancesConverter:
    class __ConcordancesConverter:
        versesdict = None
        votesdict = None
	chapter_concordances = None
        # Write a constructor
        def __init__(self, arg):
            self.val = arg
            self.votesdict = {}
            self.versesdict = {}
            self.chapter_concordances = {}

            # Load the verse id and the concordance into a dict
            with open(arg, mode='r') as infile:
                reader = csv.reader(infile, delimiter='\t')
                #self.versesdict = dict((rows[0].lower(),rows[1]) for rows in reader)
		for rows in reader:
			verseid = rows[0].lower()

			# Fill the concordances
			verseconcordances = self.versesdict.get(verseid, [])
			verseconcordances.append(rows[1])
			self.versesdict.update({verseid : verseconcordances})

			# Fill the votes
			versevotes = self.votesdict.get(verseid, [])
			versevotes.append(rows[2])
			self.votesdict.update({verseid : versevotes})

			# Fill the chapter concordances
			chapterid = verseid[:-(len(verseid) - verseid.rfind('.'))]
			chapterconcordances = self.chapter_concordances.get(chapterid, {})
			chapter_verse_concordances = chapterconcordances.get(verseid, [])
			chapter_verse_concordances.append(rows[1])
			chapterconcordances.update({verseid: chapter_verse_concordances})
			self.chapter_concordances.update({chapterid : chapterconcordances})


            # Load the verse id and the number of votes
            #with open(arg, mode='r') as infile:
            #    # Load the book abreviation, shortname in a dictionary
            #    reader = csv.reader(infile, delimiter='\t')
            #    self.votesdict = dict((rows[0].lower(),rows[2]) for rows in reader)



        def __str__(self):
            return repr(self) + self.val
        def get_shortname(self,name):
            return self.mydict.get(name, "unknown")


    instance = None

    def __init__(self, arg):
         if not ConcordancesConverter.instance:
                ConcordancesConverter.instance = ConcordancesConverter.__ConcordancesConverter(arg)
         else:
            ConcordancesConverter.instance.val = arg

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def get_chapter_concordances(self, name):
        #return ConcordancesConverter.instance.versesdict.get(name)
	#return [key.startswith(name) for key in ConcordancesConverter.instance.versesdict]
	return ConcordancesConverter.instance.chapter_concordances.get(name, [])

    def get_verse_concordances(self, name):
        return ConcordancesConverter.instance.versesdict.get(name, [])


    def get_votes(self, name):
        return ConcordancesConverter.instance.votesdict.get(name, [])


def bookId2Name(id):
    #regex = ""
    #m = re.search(regex, id)
    #if m:
    #    return m.group(1)
    return id.split('.')[1]


tree = etree.parse("resources/others/French.xml")
books = tree.xpath("/cesDoc/text/body/div")

abrev = AbreviationConverter("resources/others/abreviations_fr_eng.csv")
concordances = ConcordancesConverter("resources/others/cross_references.txt")

i = 1
for book in books:

    bookId = book.get('id')
    bookname = bookId2Name(bookId)
    bookshortname = abrev.get_shortname(bookname)
    booklongname = abrev.get_longname(bookname)
    booksection = abrev.get_section(bookname)

    # Create a new file named after the book
    bookfilename = "%s/%1.2d_%s.tex" % (booksection.lower(), i, bookname)
    f = open(bookfilename, "w+")

    # Generate the file header
    bookheader = "\\book[" + booklongname + "]{"+ bookshortname +"}"
    print bookheader
    f.write(bookheader + "\r\n\r\n")

    chapters = book.xpath("div")
    for chapter in chapters:
        chapid = chapter.get("id")
        print "\\chapter " + chapid
        #f.write("\r\n\\blankpage\r\n")
        f.write("\r\n\\chapter["+ booklongname +"]\r\n")
        f.write("\r\n\\chaptermark{"+ booklongname +"}{}\r\n")

        # Get the concordances for this chapter
	#chapterid_key = chapid.replace('b.', '').lower()
        #chapter_concordances = concordances.get_chapter_concordances(chapterid_key)
	#print chapterid_key, chapter_concordances
        ## Generate a table to print the concordances
        #f.write("\\begin{table}\r\n")
        #f.write("\\centering\r\n")
        #f.write("\\footnotesize\r\n")
        #f.write("\\fontfamily{ppl}\selectfont\r\n")
	#f.write("\\begin{center}\r\n")
	#f.write("\\begin{tabular}{ cl }\r\n")

        #f.write("\\toprule\r\n")
	#f.write("Verset & Concordance\\\\\r\n")
        #f.write("\\midrule\r\n")
	#for key in chapter_concordances.keys():
	#	#verseandconcordance = "%s & %s\\\\\r\n" % (key[0], key[1])
	#	listofconcordances = chapter_concordances.get(key)

	#	modulo = 1
	#	joined_concordances = ""
	#	for x in listofconcordances:
	#		joined_concordances += str(x)
	#		if (modulo % 5 == 0):
	#			joined_concordances += "\\\\"
	#		else:
	#			joined_concordances += ", "
	#		modulo += 1

	#	#joined_concordances = ' \\\\'.join(str(x) for x in listofconcordances)
	#	verseandconcordance = "%s & %s\\\\\r\n" % (key, joined_concordances)
        #	f.write(verseandconcordance)
        #	#f.write("\\hline\r\n")
        #f.write("\\bottomrule\r\n")
        #f.write("\\end{tabular}\r\n")
        #f.write("\\end{center}\r\n")
        #f.write("\\caption{Concordances pour le chapitre " + chapterid_key + "}\r\n")
	#f.write("\\end{table}\r\n")


        segments = chapter.xpath("seg")
        for segment in segments:
            # Write the sidenotes
            segmentid = segment.get('id').replace("b.", "").lower()
            verseconcordances = concordances.get_verse_concordances(segmentid)
            versevotes = concordances.get_votes(segmentid)

            f.write("\\verse %s \r\n" % segment.text.encode('utf8').strip())

            if(verseconcordances is not None and len(verseconcordances) > 0):
                sidenotes = "\\defi{ \\\\ \\textcolor{blue}{ %s :} \\textcolor{gray}{%s} }\r\n" % (segmentid, ", ".join(verseconcordances))
                print sidenotes
                f.write(sidenotes)

    print "This book is finished. closing the %s file." % bookfilename
    # Close the book file
    f.close()

    i = i + 1

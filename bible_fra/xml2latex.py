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
        # Write a constructor
        def __init__(self, arg):
            self.val = arg
            self.votesdict = {}
            self.versesdict = {}

            # Load the verse id and the concordance into a dict
            with open(arg, mode='r') as infile:
                reader = csv.reader(infile, delimiter='\t')
                self.versesdict = dict((rows[0].lower(),rows[1]) for rows in reader)

            # Load the verse id and the number of votes
            with open(arg, mode='r') as infile:
                # Load the book abreviation, shortname in a dictionary
                reader = csv.reader(infile, delimiter='\t')
                self.votesdict = dict((rows[0].lower(),rows[2]) for rows in reader)



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

    def get_concordances(self, name):
        return ConcordancesConverter.instance.versesdict.get(name)

    def get_votes(self, name):
        return ConcordancesConverter.instance.votesdict.get(name)


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
        f.write("\r\n\\chapter\r\n")

        segments = chapter.xpath("seg")
        for segment in segments:
            # Write the sidenotes
            segmentid = segment.get('id').replace("b.", "").lower()
            verseconcordances = concordances.get_concordances(segmentid)
            versevotes = concordances.get_votes(segmentid)

            if(verseconcordances is not None):
                sidenotes = "\\defi{ Concordance : %s (%s votes) }\r\n" % (verseconcordances, versevotes)
                print sidenotes
                f.write(sidenotes)

            f.write("\\verse %s \r\n" % segment.text.encode('utf8').strip())

    print "This book is finished. closing the %s file." % bookfilename
    # Close the book file
    f.close()

    i = i + 1

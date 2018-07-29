#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import re

def bookId2Name(id):
    #regex = ""
    #m = re.search(regex, id)
    #if m:
    #    return m.group(1)
    return id.split('.')[1]


tree = etree.parse("French.xml")
books = tree.xpath("/cesDoc/text/body/div")

for book in books:

    bookId = book.get('id')
    bookname = bookId2Name(bookId)
    # Create a new file named after the book
    f = open(bookname+".tex", "w+")
    # Generate the file header

    bookheader = "\\book[" + bookId + "]{"+ bookId.lower() +"}"
    print bookheader
    f.write(bookheader + "\r\n\r\n")

    chapters = book.xpath("div")
    for chapter in chapters:
        chapid = chapter.get("id")
        print "\\chapter " + chapid
        f.write("\r\n\\chapter\r\n")

        segments = chapter.xpath("seg")
        for segment in segments:
            f.write("\\verse %s \r\n" % segment.text.encode('utf8').strip())

    print "This book is finished. closing the file."
    # Close the book file
    f.close()

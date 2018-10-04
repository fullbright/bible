#!/usr/bin/env python
# -*- coding: utf-8 -*-

def merge_margin_notes():

    tree = etree.parse("resources/others/French.xml")
    books = tree.xpath("/cesDoc/text/body/div")


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


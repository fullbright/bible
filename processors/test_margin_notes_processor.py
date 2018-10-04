import unittest
import margin_notes_processor
import os

BIBLE_FILE = os.path.join(os.path.dirname(__file__), '../corpus/French.xml')

class Test_margin_notes_processor(unittest.TestCase):

    def setUp():
       # Load the french xml bible file
        self.bibledata = open(BIBLE_FILE).read()

    def test_merge_notes():
        # Test if notes are merged correctly

    def test_split_chapters():
        # Test that two chapters in the xml flow are splitted correctly



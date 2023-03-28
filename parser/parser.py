'''
This Python script is separate from the rest of the Django app (i.e. it is not 
required to run Theologos).

Call the appropriate class' `.createFixtureFromCsv()` method from the Python shell
in order to create fixtures for the Bible models.

For example, run
`Book.createFixtureFromCsv("data/books.csv")`
to create a new file called "bible/fixtures/books.json" that contains the fixture.

Note: This would overwrite any existing content in the books.json file.
'''

import csv
import json

'''
The Book class takes in a CSV with these columns: symbol, full_title, testament, length.

The .createFixtureFromCsv() method will write the Chapter fixture in addition to
the Book fixture, based on the 'length' field of each book.
'''
class Book:
    def __init__(self, fields):
        self.length = int(fields["length"])
        fields.pop("length")
        self.fields = fields

    def getFixtureInstance(self):
        fixture = dict()
        fixture["model"] = "bible.book"
        fixture["fields"] = self.fields
        return fixture
    
    class Chapter:
        def __init__(self, bookSymbol, number):
            self.book = bookSymbol
            self.number = number
            fields = dict()
            fields["id"] = self.generate_id()
            fields["book"] = bookSymbol
            fields["number"] = number
            self.fields = fields

        def generate_id(self):
            book = self.book
            num = str(self.number) 
            # num should be 3 digits long
            num = "0" * (3-len(num)) + num
            return f"{book}-{num}"

        def getFixtureInstance(self):
            fixture = dict()
            fixture["model"] = "bible.chapter"
            fixture["fields"] = self.fields
            return fixture
    
    def getChapterFixtures(self):
        fixtures = []
        for number in range(1, self.length+1):
            c = Book.Chapter(self.fields['symbol'], number)
            fixtures.append(c.getFixtureInstance())
        return fixtures
    
    def createFixtureFromCsv(filepath):
        # read from CSV
        books = []
        chapters = []
        with open(filepath, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            number = 1
            for line in reader: # line is a dictionary
                line["number"] = number
                number += 1

                b = Book(line)
                books.append(b.getFixtureInstance())
                chapters.extend(b.getChapterFixtures())

        # write a JSON file
        books_json_object = json.dumps(books, indent=2)
        chapters_json_object = json.dumps(chapters, indent=2)

        with open("./bible/fixtures/books.json", "w") as out_file:
            out_file.write(books_json_object)

        with open("./bible/fixtures/chapters.json", "w") as out_file:
            out_file.write(chapters_json_object)

class Verse:
    
    def __init__(self, fields):
        self.fields = fields
        self.book = fields["book"]
        fields.pop("book")
        self.chapter_number = fields["chapter"]
        fields["chapter"] = self.generate_chapter_id()
        self.number = fields["number"]
        fields["id"] = self.generate_id()
        fields["original_text"] = fields["text"]
        fields.pop("text")
        fields["number"] = self.number

    def generate_chapter_id(self):
        book = self.book
        chap_num = str(self.chapter_number)
        # chap_num should be 3 digits long
        chap_num = "0" * (3-len(chap_num)) + chap_num
        return f"{book}-{chap_num}"

    def generate_id(self):
        chap_id = self.fields["chapter"]
        num = str(self.number) 
        # num should be 3 digits long
        num = "0" * (3-len(num)) + num
        return f"{chap_id}-{num}"

    def getFixtureInstance(self):
        fixture = dict()
        fixture["model"] = "bible.verse"
        fixture["fields"] = self.fields
        return fixture
    
    def createFixtureFromCsv(filepath):
        # read from CSV
        verses = []
        with open(filepath, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            prev_book = None
            prev_chap_num = None
            for line in reader: # line is a dictionary
                # reset verse number for new chapters (relies on CSV being written in order)
                if line["chapter"] == prev_chap_num and line["book"] == prev_book:
                    number += 1
                else:
                    number = 1
                    prev_chap_num = line["chapter"]
                    prev_book = line["book"]
                line["number"] = number
                print(line["book"], prev_book, line["chapter"], prev_chap_num, number)

                v = Verse(line)
                verses.append(v.getFixtureInstance())

        # write a JSON file
        verses_json_object = json.dumps(verses, indent=2)

        with open("./bible/fixtures/verses.json", "w") as out_file:
            out_file.write(verses_json_object)
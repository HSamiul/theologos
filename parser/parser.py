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
        self.fields = fields.copy()
        self.fields.pop("length")

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
            for line in reader: # line is a dictionary
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
        fields = fields.copy() # make sure to not mutate the original fields dictionary

        book = fields["book"]
        chapter_num = fields["chapter"]
        fields["chapter"] = Verse.generate_chapter_id(book, chapter_num) # need the chapter id as a foreign key in Postgres
        self.chapter = fields["chapter"]

        self.number = fields["number"]
        fields["id"] = self.generate_id()
        fields["original_text"] = fields["text"]
        fields["number"] = self.number
        fields.pop("book") # don't need these fields from the original CSV file
        fields.pop("text")
        self.fields = fields

    @staticmethod
    def generate_chapter_id(book, chapter_num):
        chapter_num = str(chapter_num)
        # chapter_num should be 3 digits long. add leading zeros if necessary
        chapter_num = "0" * (3-len(chapter_num)) + chapter_num
        return f"{book}-{chapter_num}"

    def generate_id(self):
        chapter_id = self.chapter
        num = str(self.number)
        # num should be 3 digits long
        num = "0" * (3-len(num)) + num
        return f"{chapter_id}-{num}"

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
            for line in reader: # line is a dictionary
                v = Verse(line)
                verses.append(v.getFixtureInstance())

        # write a JSON file
        verses_json_object = json.dumps(verses, indent=2)

        with open("./bible/fixtures/verses.json", "w") as out_file:
            out_file.write(verses_json_object)
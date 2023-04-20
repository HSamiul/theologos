from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

# TODO determine if the methods have camel or snake case

class Book(models.Model):

    # [PK] The abbreviated book title (e.g. gen)
    # Note: Abbreviations taken from https://www.logos.com/bible-book-abbreviations
    symbol = models.CharField(max_length=7, primary_key=True)

    # The book number (e.g. 1 for Genesis)
    number = models.IntegerField(unique=True, null=False)

    # The full English title of the book (e.g. "Genesis")
    full_title = models.CharField(max_length=15, unique=True, blank=False, null=False)

    # The language ID of the original title (e.g. 'en' for English)
    #original_lang_id = models.CharField(default='en', max_length=10)

    # Enumeration of testaments
    TESTAMENTS = (
        ('old', 'Old Testament'),
        ('new', 'New Testament'),
    )

    # The testament the book belongs to
    testament = models.CharField(max_length=3, choices=TESTAMENTS, blank=False)

    def __str__(self):
        return self.full_title
    
    def get_chapters(self):
        return self.chapter_set.order_by("number")


class Chapter(models.Model):

    # TODO make this ID autogenerated
    # [PK] The chapter ID (e.g. "gen-001")
    id = models.CharField(max_length=11, primary_key=True)

    # [FK] The book the chapter belongs to
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    # TODO make sure validators for this actually work.
    # The chapter number (e.g. 012)
    number = models.IntegerField(validators=[MinLengthValidator(3), MaxLengthValidator(3)])

    def get_id(self): # format: "<book_symbol>-<number>"
        number = str(self.number)
        number = "0" * (3-len(number)) + number
        return f'{self.book.symbol}-{number}'
    
    def __str__(self):
        return f'{self.book.full_title} {self.number}'
    
    def get_verses(self):
        return self.verse_set.order_by("number")


class Verse(models.Model):

    # TODO make this ID autogenerated
    # [PK] The verse ID (e.g. "gen-001-001")
    id = models.CharField(max_length=14, primary_key=True)

    # [FK] The chapter the verse belongs to
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    # TODO make sure validators for this actually work.
    # The verse number (e.g. 012)
    number = models.IntegerField(validators=[MinLengthValidator(3), MaxLengthValidator(3)])

    # The text of the verse in English
    original_text = models.CharField(max_length=500)

    # The language ID of the original text (e.g. 'en' for English)
    #original_lang_id = models.CharField(default='en', max_length=10)

    def get_id(self): # format: "<book_symbol>-<chapter_number>-<number>"
        number = str(self.number)
        number = "0" * (3-len(number)) + number
        return f'{self.chapter.get_id()}-{number}'
    
    def __str__(self):
        return f'{self.chapter}:{self.number}'
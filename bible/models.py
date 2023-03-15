from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Book(models.Model):

    # [Primary key] The book number (e.g. 01)
    number = models.IntegerField(default='01', primary_key=True, validators=[MinLengthValidator(2), MaxLengthValidator(2)])

    class BookTitle(models.TextChoices):
        '''
        An enumeration type that defines the titles for the books of the Bible 
        (in English).

        Note: Abbreviations taken from https://www.logos.com/bible-book-abbreviations
        '''

        # TODO complete the rest of the books

        # OLD TESTAMENT
        GENESIS = 'gen', 'Genesis'
        EXODUS = 'ex', 'Exodus'
        LEVITICUS = 'lev', 'Leviticus'
        
        # NEW TESTAMENT
        PHILIPPIANS = 'phil', 'Philippians'


    # The title of the book (e.g. "Genesis")
    original_title = models.CharField(max_length=7, choices=BookTitle.choices)

    # The language ID of the original title (e.g. 'en' for English)
    #original_lang_id = models.CharField(default='en', max_length=10)

    # Enumeration of testaments
    TESTAMENTS = (
        ('old', 'Old Testament'),
        ('new', 'New Testament'),
    )

    # The testament the book belongs to
    testament = models.CharField(max_length=3, choices=TESTAMENTS)

    def getFullTitle(self):
        return self.BookTitle(self.original_title).label


class Chapter(models.Model):

    # The book the chapter belongs to
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    # The chapter number (e.g. 012)
    number = models.IntegerField(validators=[MinLengthValidator(3), MaxLengthValidator(3)])


class Verse(models.Model):

    # The chapter the verse belongs to
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    # The verse number (e.g. 012)
    number = models.IntegerField(validators=[MinLengthValidator(3), MaxLengthValidator(3)])

    # The text of the verse
    original_text = models.CharField(max_length=500)

    # The language ID of the original text (e.g. 'en' for English)
    #original_lang_id = models.CharField(default='en', max_length=10)
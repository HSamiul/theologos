from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

# TODO determine if the methods have camel or snake case

class Book(models.Model):
    '''
    This model stores data about a Bible book.
    '''

    # [PK] The abbreviated book title (e.g. gen)
    # Note: Abbreviations taken from https://www.logos.com/bible-book-abbreviations
    symbol = models.CharField(max_length=7, primary_key=True)

    # The book number (e.g. 1 for Genesis)
    number = models.IntegerField(unique=True, null=False)

    # The full English title of the book (e.g. "Genesis")
    full_title = models.CharField(max_length=15, unique=True, blank=False, null=False)

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
        '''
        Return all chapters of this Bible ordered by number.
        '''
        return self.chapter_set.order_by("number")
    
    @staticmethod
    def get_all_books():
        '''
        Return all books of the Bible ordered by number.
        '''
        return Book.objects.all().order_by("number")


class Chapter(models.Model):
    '''
    This model stores data about a chapter of a book in the Bible.
    '''

    # [PK] The chapter ID (e.g. "gen-001")
    id = models.CharField(max_length=11, primary_key=True)

    # [FK] The book the chapter belongs to
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    # The chapter number (e.g. 012)
    number = models.IntegerField(validators=[MinLengthValidator(3), MaxLengthValidator(3)])

    def get_id(self):
        '''
        Return the id associated with a chapter. The format of the id will
        follow the following format: <book_symbol>-<number>
        '''
        number = str(self.number)
        number = "0" * (3-len(number)) + number
        return f'{self.book.symbol}-{number}'
    
    def __str__(self):
        return f'{self.book.full_title} {self.number}'
    
    def get_verses(self):
        '''
        Return all verses of this chapter ordered by number.
        '''
        return self.verse_set.order_by("number")


class Verse(models.Model):
    '''
    This model stores data about a verse in a chapter of a book in the Bible.
    '''

    # [PK] The verse ID (e.g. "gen-001-001")
    id = models.CharField(max_length=14, primary_key=True)

    # [FK] The chapter the verse belongs to
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    # The verse number (e.g. 012)
    number = models.IntegerField(validators=[MinLengthValidator(3), MaxLengthValidator(3)])

    # The text of the verse in English
    original_text = models.CharField(max_length=500)

    def get_id(self):
        '''
        Return the id associated with a chapter. The format of the id will
        follow the following format: <book_symbol>-<chapter_number>-<number>
        '''
        number = str(self.number)
        number = "0" * (3-len(number)) + number
        return f'{self.chapter.get_id()}-{number}'
    
    def __str__(self):
        return f'{self.chapter}:{self.number}'
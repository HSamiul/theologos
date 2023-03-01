from django.db import models

# TODO change relevant fields to enums instead of charfields

class Testament(models.Model):
    original_title = models.CharField(max_length=30)
    original_lang_id = models.CharField(default='en', max_length=10)

class Book(models.Model):
    testament = models.ForeignKey(Testament, on_delete=models.CASCADE)
    original_title = models.CharField(max_length=30)
    original_lang_id = models.CharField(default='en', max_length=10)

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    number = models.IntegerField()

class Verse(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    number = models.IntegerField()
    original_text = models.CharField(max_length=200)
    original_lang_id = models.CharField(default='en', max_length=10)
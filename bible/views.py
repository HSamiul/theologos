from django.shortcuts import get_object_or_404, render

from .models import Book, Chapter
from commentary.models import Post

def index(request, book_id, chapter_num): # TODO add version_id in the future
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, book=book_id, number=chapter_num)
    verses = chapter.verse_set.order_by("id")
    
    return render(request, 'bible/index.html', {'book': book, 'chapter_num': chapter_num, 'verses': verses})

def commentary(request, book_id, chapter_num, verse_num):
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, book=book_id, number=chapter_num)
    verses = chapter.verse_set.order_by("id")
    
    posts = get_object_or_404(Post, verse=verse_num)
    
    context = {
        'book': book, 
        'chapter_num': chapter_num, 
        'verses': verses,
        'posts': posts
        }
    
    return render(request, 'commentary/index.html', context)
from django.shortcuts import get_object_or_404, render

from .models import Book, Chapter

def index(request, book_id, chapter_id): # TODO add version_id in the future
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    return render(request, 'bible/index.html', {'book': book, 'chapter': chapter})
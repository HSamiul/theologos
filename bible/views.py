from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Book, Chapter, Verse
from commentary.forms import PostCreationForm

def index(request, book_symbol=None, chapter_num=None, verse_num=None): # TODO add version_id in the future
    books = Book.objects.all()

    if not book_symbol and not chapter_num and not verse_num: # the user is reading the Bible from the top
        context = {
            'books' : books,
            }
        
        return render(request, 'bible/index.html', context)
    
    else: # the user is viewing OR submitting commentary for a specific verse
        book = get_object_or_404(Book, pk=book_symbol)
        chapter = get_object_or_404(Chapter, book=book, number=chapter_num)
        verses = chapter.verse_set.order_by("id")
        verse = get_object_or_404(Verse, chapter=chapter, number=verse_num)
        posts = verse.post_set.order_by('creation_time')
        
        if request.method == 'GET': # the user is viewing commentary
            postCreationForm = PostCreationForm()
        
            context = {
                'books' : books,
                'book' : book,
                'chapter' : chapter,
                'verses': verses,
                'verse': verse, # specific verse being viewed
                'posts': posts, # posts for that verse
                'postCreationForm': postCreationForm # form to add commentary to that verse
                }
        
            return render(request, 'bible/index.html', context)
        
        else: # the user is submitting commentary
            if not request.user.is_authenticated: # do not allow posts to be made while not signed in
                return HttpResponse('Failed to post. You must be signed in to post.')
        
            else:
                postCreationForm = PostCreationForm(request.POST) # use request data to populate form fields

                if postCreationForm.is_valid():
                    post = postCreationForm.save(commit=False) # obtain a post object without commiting to DB
                    
                    post.author = request.user.profile
                    post.verse = verse
                    post.save()
                    
                    # TODO: Flash success message
                    return HttpResponseRedirect(request.META['HTTP_REFERER']) # reload the page
                
                # TODO: Flash failure message and redirect to the same page
                else:
                    return HttpResponse('your post was not valid so it was not posted.')
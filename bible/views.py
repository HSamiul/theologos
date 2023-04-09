from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Book, Chapter, Verse
from commentary.forms import PostCreationForm
from commentary.models import Post

from django.views import View

class BibleCommentaryView(View):
    books = Book.objects.all()

    def get(self, request, *args, **kwargs):
        book_symbol = kwargs.get('book_symbol', None)
        chapter_num = kwargs.get('chapter_num', None)
        verse_num = kwargs.get('verse_num', None)
        # TODO add version_id in the future
        post_id = kwargs.get('post_id', None)
        
        # the user is reading the Bible from the top
        if not book_symbol and not chapter_num and not verse_num and not post_id:
            context = {
                'books' : self.books,
            }
            return render(request, 'bible/index.html', context)
        
        # the user is viewing OR submitting commentary for a specific verse
        book = get_object_or_404(Book, pk=book_symbol)
        chapter = get_object_or_404(Chapter, book=book, number=chapter_num)
        verses = chapter.verse_set.order_by("id")
        verse = get_object_or_404(Verse, chapter=chapter, number=verse_num)
        
        if not post_id:
            posts = verse.post_set.order_by('creation_time')
            postCreationForm = PostCreationForm()
            
            context = {
                'books' : self.books,
                'book' : book,
                'chapter' : chapter,
                'verses': verses,
                'verse': verse, # specific verse being viewed
                'posts': posts, # posts for that verse
                'postCreationForm': postCreationForm # form to add commentary to that verse
            }
            
            return render(request, 'bible/index.html', context)
        
        # the user is viewing a post detail view
        post = get_object_or_404(Post, pk=post_id)
        context = {
            'books' : self.books,
                'book' : book,
                'chapter' : chapter,
                'verses': verses,
                'verse': verse, # specific verse being viewed
                'post' : post
        }

        return render(request, 'bible/index.html', context)

    def post(self, request, *args, **kwargs):
        book_symbol = kwargs.get('book_symbol', None)
        chapter_num = kwargs.get('chapter_num', None)
        verse_num = kwargs.get('verse_num', None)
        
        if not book_symbol and not chapter_num and not verse_num:
            return HttpResponse('Failed to post. You must select a verse to post.')

        book = get_object_or_404(Book, pk=book_symbol)
        chapter = get_object_or_404(Chapter, book=book, number=chapter_num)
        verse = get_object_or_404(Verse, chapter=chapter, number=verse_num)
        postCreationForm = PostCreationForm()

        # do not allow posts to be made while not signed in
        if not request.user.is_authenticated:
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
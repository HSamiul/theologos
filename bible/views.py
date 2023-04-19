from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Book, Verse
from commentary.forms import PostCreationForm
from commentary.models import Post
from commentary.filters import PostFilter

from django.views import View

class BibleCommentaryView(View):
    books = Book.objects.all()

    def get(self, request, *args, **kwargs):
        verse_id = kwargs.get('verse_id', None)
        post_id = kwargs.get('post_id', None)
        
        # the user is reading the Bible from the top
        if not verse_id:
            context = {
                'books' : self.books,
            }
            return render(request, 'bible/index.html', context)
        
        # the user is viewing OR submitting commentary for a specific verse
        verse = get_object_or_404(Verse, pk=verse_id)
        
        if not post_id:
            post_filter = PostFilter(request.GET, queryset=verse.post_set)
            postCreationForm = PostCreationForm()
            
            context = {
                'books' : self.books,
                'verse': verse, # specific verse being viewed
                'posts': post_filter.qs.order_by('creation_time'), # filtered posts for that verse
                'postCreationForm': postCreationForm, # form to add commentary to that verse
                'postFilterForm': post_filter.form # form to filter posts
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
        verse_id = kwargs.get('verse_id', None)
        
        if not verse_id:
            return HttpResponse('Failed to post. You must select a verse to post.')

        verse = get_object_or_404(Verse, pk=verse_id)
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

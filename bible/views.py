from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .models import Book, Verse
from commentary.forms import PostCreationForm
from commentary.models import Post, Vote
from commentary.filters import PostFilter

from django.views import View

class BibleCommentaryView(View):
    '''
    This class is a Django class-based view. Like all Django views, its job is 
    to process a request and return a response.
    
    Currently, this view is responsible for:

      (get)
      - querying the database for the Bible
      - querying the database for all posts related to a verse
      - creating a form to create a new post
      - creating a form to filter posts

      (post)
      - saving a new post to the database

      (toggle_vote)
      - toggling a user profile's vote on a post
    '''

    books = Book.get_all_books() # query the database for all books

    def get(self, request, *args, **kwargs):
        '''
        This function handles a GET request to get data about the Bible. This 
        method handles one argument: verse_id. There are 2 cases handled in
        this method:
        1. the user is viewing the Bible and no posts (example url: /bible/)
        2. the user is viewing the Bible and a list of posts for one verse (example url: /bible/gen-01-01/)
        '''
        # extract value for verse_id from arguments
        verse_id = kwargs.get('verse_id', None)
        
        # case 1: the user is viewing the Bible and no posts (example url: /bible/)
        if not verse_id:
            # create a dictionary mapping variable names to their values
            context = {
                'books' : self.books,
            }
            # call render which combines the given template and context into an HttpResponse
            return render(request, 'bible/index.html', context)
        
        # case 2: the user is viewing the Bible and a list of posts for one verse (example url: /bible/gen-01-01/)

        # query the database for one specific verse that belongs to the given chapter and has the given verse_num
        verse = get_object_or_404(Verse, pk=verse_id)
        
        # create an instance of PostFilter which will query the database for posts
        # (either all posts or posts filtered by faith tradition specified in form, see below)
        post_filter = PostFilter(request.GET, queryset=verse.post_set)

        # create an instance of PostCreationForm which allows users to create posts associated with a verse
        postCreationForm = PostCreationForm()
        
        # create a dictionary mapping variable names to their values
        context = {
            'books' : self.books,
            'verse': verse, # specific verse being viewed
            'posts': post_filter.qs.order_by('creation_time'), # filtered posts for that verse
            'postCreationForm': postCreationForm, # form to add commentary to that verse
            'postFilterForm': post_filter.form # form to filter posts
        }
        
        # call render which combines the given template and context into an HttpResponse
        return render(request, 'bible/index.html', context)

    def post(self, request, *args, **kwargs):
        '''
        This function handles a POST request to accept new data about a post.
        This method handles one argument: verse_id.
        '''
        # extract value for verse_id from arguments
        verse_id = kwargs.get('verse_id', None)
        
        # cannot create a post without knowing which book, chapter, and verse it belongs to
        if not verse_id:
            return HttpResponse('Failed to post. You must select a verse to post.')

        # query the database for one specific verse that belongs to the given chapter and has the given verse_num
        verse = get_object_or_404(Verse, pk=verse_id)
        postCreationForm = PostCreationForm()

        # do not allow posts to be made while not logged in
        if not request.user.is_authenticated:
            return HttpResponse('Failed to post. You must be signed in to post.')
        
        else:
            # use request data to populate form fields
            postCreationForm = PostCreationForm(request.POST)

            if postCreationForm.is_valid():
                # obtain a post object without commiting to database
                post = postCreationForm.save(commit=False)
                
                # set the Post author attribute to the current user's profile object
                post.author = request.user.profile
                
                # set the Post verse attribute to the selected verse object
                post.verse = verse

                # save to database
                post.save()
                
                # TODO: Flash success message
                return redirect('bible:index', verse_id=verse_id) # reload the page
            
            # TODO: Flash failure message and redirect to the same page
            else:
                return HttpResponse('your post was not valid so it was not posted.')

def toggle_vote(request, post_id):
    '''
    This function processes a request to vote or unvote a post. The result is
    that the page is reloaded. Each user can only vote on a post once. If they
    have already voted when this function is called, the vote will be removed.
    '''
    # do not allow votes while not logged in
    if not request.user.is_authenticated:
        return HttpResponse('You must be signed in to upvote posts.') # TODO: give a more helpful response (flash a message?)
    
    # get the profile of the user who made the request
    profile = request.user.profile
    
    # query the database for the post with the given post_id
    post = get_object_or_404(Post, pk=post_id)

    # get the set of votes that are associated with this post
    votes = post.vote_set

    # filter to get the vote that is associated with this profile
    vote = votes.filter(voter=profile).first()
    
    # if the profile has a vote associated with this post
    if vote != None:
        # delete the vote
        vote.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER']) # reload the page
    else:
        # create a new vote associated with this profile and post
        vote = Vote(voter=profile, post=post)

        # save to database
        vote.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER']) # reload the page
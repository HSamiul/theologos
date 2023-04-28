from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from bible.models import Book
from .models import Post

'''
Referenced https://legionscript.medium.com/building-a-social-media-site-with-python-and-django-part-4-edit-delete-posts-add-comments-8e6ca1ef0441

Learn more about Django's generic display views here: https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-display/
Learn more about Django's generic editing views here: https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-editing/


The LoginRequiredMixin used by the PostUpdateView and PostDeleteView tells Django 
that this view is only accessible if the request user is logged in.

The UserPassesTestMixin used by the PostUpdateView and PostDeleteView tells Django 
that this view is only accessible if the request user is approved by the check
determined in the test_func method.
'''


class PostDetailView(DetailView):
    '''
    This class is a Django DetailView. Because this view inherits from a DetailView 
    it requires less code and handles a lot of the logic for us, such as rendering
    an HttpResponse and handling GET requests.

    Because this DetailView references the `Post` model, it automatically looks for
    the template named post_detail.html.
    '''
    model = Post

    def get_context_data(self, **kwargs):
        '''
        This built-in Django function handles passing the context dictionary
        to the post_detail template.
        '''
        context = super().get_context_data(**kwargs)

        # Note: self.object refers to the post whose detail view we are in
        # Pass in the specific verse that the post is correlated to
        context["verse"] = self.object.verse

        # Get all the Bible books in order
        context["books"] = Book.get_all_books()
        return context
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''
    This class is a Django DeleteView. Because this view inherits from a DeleteView 
    a lot of the logic typically required for writing a view is handled for us.

    This DeleteView automatically looks for the template named post_confirm_delete.html
    to indicate the template to go to as a confirmation page before the user actually
    deletes a post.
    '''
    model = Post

    def get_context_data(self, **kwargs):
        '''
        This built-in Django function handles passing the context dictionary
        to the post_confirm_delete template.
        '''
        context = super().get_context_data(**kwargs)

        # Note: self.object refers to the post whose delete view we are in
        # Pass in the specific verse that the post is correlated to
        context["verse"] = self.object.verse

        # Get all the Bible books in order
        context["books"] = Book.get_all_books()
        return context

    def get_success_url(self):
        '''
        This built-in Django function returns the URL that you get redirected to 
        after the delete succeeds. In this case, it should return to the bible index view.
        '''
        post = self.get_object()

        # Get the URL for the bible index view and pass in the required arguments
        return reverse_lazy('bible:index', kwargs={'verse_id': post.verse.get_id() })
    
    def test_func(self):
        '''
        This built-in Django function is used by the UserPassesTestMixin to decide 
        if a user is allowed to access the view.
        
        Returns True if they should be allowed to access the view.
        '''
        post = self.get_object()

        # They are allowed to delete the post if the request user is the same as the post author
        return self.request.user.id == post.author.user.id


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    '''
    This class is a Django UpdateView. Because this view inherits from a UpdateView 
    a lot of the logic typically required for writing a view is handled for us.
    '''
    model = Post

    # Define which fields we are including in the update form
    fields = ['title', 'text']

    # Tells the view to search for the "post_update_form.html" template
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        '''
        This built-in Django function handles passing the context dictionary
        to the post_update_form template.
        '''
        context = super().get_context_data(**kwargs)

        # Note: self.object refers to the post whose update view we are in
        # Pass in the specific verse that the post is correlated to
        context["verse"] = self.object.verse

        # Get all the Bible books in order
        context["books"] = Book.get_all_books()
        return context
    
    def get_success_url(self):
        '''
        This built-in Django function returns the URL that you get redirected to 
        after the update succeeds. In this case, it should return to the bible index view.
        '''
        post = self.get_object()

        # Get the URL for the bible index view and pass in the required arguments
        return reverse_lazy('bible:index', kwargs={'verse_id': post.verse.get_id() })

    def test_func(self):
        '''
        This built-in Django function is used by the UserPassesTestMixin to decide 
        if a user is allowed to access the view.
        
        Returns True if they should be allowed to access the view.
        '''
        post = self.get_object()

        # They are allowed to update the post if the request user is the same as the post author
        return self.request.user.id == post.author.user.id
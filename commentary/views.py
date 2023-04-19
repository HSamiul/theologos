from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from bible.models import Book
from .models import Post

'''
Referenced https://legionscript.medium.com/building-a-social-media-site-with-python-and-django-part-4-edit-delete-posts-add-comments-8e6ca1ef0441

Notes:
- get_success_url is the URL that you get redirected to after the update/delete
- test_func is used by the UserPassesTestMixin to decide if a user is allowed to access the view
'''

class PostListView(ListView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = Book.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = Book.objects.all()
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = Book.objects.all()
        return context

    def get_success_url(self):
        post = self.get_object()
        return reverse_lazy('bible:index', kwargs={'verse_id': post.verse.get_id() })
    
    def test_func(self):
        post = self.get_object()
        return self.request.user.id == post.author.user.id
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Post

# referenced https://legionscript.medium.com/building-a-social-media-site-with-python-and-django-part-4-edit-delete-posts-add-comments-8e6ca1ef0441
# get_success_url is the URL that you get redirected to after the update/delete
# test_func is used by the UserPassesTestMixin to decide if a user is allowed to access the view

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def get_success_url(self):
        post = self.get_object()
        verse = post.verse
        book_symbol, chapter_num, verse_num = verse.chapter.book.symbol, verse.chapter.number, verse.number
        return reverse_lazy('bible:index', kwargs={'book_symbol': book_symbol, 'chapter_num': chapter_num, 'verse_num': verse_num})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user.id == post.author.user.id


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text']
    template_name_suffix = '_update_form' # searches for the "post_update_form.html" template
    
    def get_success_url(self):
        post = self.get_object()
        verse = post.verse
        book_symbol, chapter_num, verse_num = verse.chapter.book.symbol, verse.chapter.number, verse.number
        return reverse_lazy('bible:index', kwargs={'book_symbol': book_symbol, 'chapter_num': chapter_num, 'verse_num': verse_num})

    def test_func(self):
        post = self.get_object()
        return self.request.user.id == post.author.user.id
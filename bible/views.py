from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Book, Chapter, Verse
from commentary.models import Post

from commentary.forms import PostCreationForm

def index(request, book_id, chapter_num, verse_num=None): # TODO add version_id in the future
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, book=book_id, number=chapter_num)
    verses = chapter.verse_set.order_by("id")
    
    if (verse_num): # user is trying to view commentary for a specific verse
        verse = get_object_or_404(Verse, chapter=chapter, number=verse_num)
        posts = verse.post_set.order_by('id')
        
        print(f'verse_num: {verse.number}')
        
        if request.method == 'POST' and not request.user.is_authenticated:
            return HttpResponse('Failed to post. You must be signed in to post.')
        
        elif request.method == 'POST' and request.user.is_authenticated:
            # use request data to populate form fields
            postCreationForm = PostCreationForm(request.POST)
            
            postCreationFormValid = postCreationForm.is_valid()
            
            if postCreationFormValid:
                print(f'user: {request.user}')
                print(f'profile: {request.user.profile}')
                post = postCreationForm.save(commit=False)
                
                post.author = request.user.profile
                post.verse = verse
                print(f'author of post: {post.author}')
                print(f'verse of post: {post.verse}')
                
                post.save()
                
                return HttpResponse('successfully posted!')
            else:
                for error in postCreationForm.errors:
                    print(f'error: {error}')
                return HttpResponse('your post was not valid so it was not posted.')
        else: # user is just viewing the commentary
            postCreationForm = PostCreationForm()
        
            context = {
                'book': book,
                'book_id': book_id,
                'verse_num': verse_num,
                'chapter_num': chapter_num,
                'verses': verses,
                'verse': verse,
                'posts': posts,
                'postCreationForm': postCreationForm
                }
        
            return render(request, 'bible/index.html', context)


    else: # user is just viewing a chapter
        return render(request, 'bible/index.html', {'book': book, 'book_id': book_id, 'chapter_num': chapter_num, 'verses': verses})

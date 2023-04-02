from django.db import models
from bible.models import Verse
from .validators import validate_min_post_length, validate_min_comment_length

class Post(models.Model):
    '''
    A user can create a `Post` on a Bible verse to share their commentary with
    others.
    '''

    # The user who wrote this post
    author = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
   
    # [FK] The verse the post belongs to
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)

    # The title of this post
    title = models.CharField(max_length=255)

    # The text body of this post
    text = models.TextField(validators=[validate_min_post_length])

    # The time this post was created
    creation_time = models.DateTimeField(auto_now_add=True)

    # The time this post was last updated
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.author}: \"{self.text}\""

class Comment(models.Model):
    '''
    A user can comment on a `Post` or `Comment`.

    This model is self-referential, meaning that it has a foreign key to itself,
    creating a parent-child relationship between instances of the same model.
    This design allows for infinite levels of comments.

    If the `Comment` is under a `Post`, the `parent_comment` field will be null.
    If the `Comment` is under another `Comment`, the `parent_comment` field will
    be set. All `Comments` must specify an associated `post`.
    '''

    # The user who wrote this comment
    author = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)

    # The text body of this comment
    text = models.TextField(validators=[validate_min_comment_length])

    # The time this comment was created
    creation_time = models.DateTimeField(auto_now_add=True)

    # The time this comment was last updated
    update_time = models.DateTimeField(auto_now=True)

    # The post this comment is associated with
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # If the comment is under another comment, then it must have a parent
    # comment. This field can be null in the database and blank in any forms
    # if the comment belongs to a post. The related_name specifies the name of
    # the reverse relation, where a parent comment may have many 
    # 'child_comments'.
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_comments')

    def add_child_comment(self, comment):
        '''
        Add a given child comment to a parent (this `Comment`). Set the 
        `parent_comment` and `post` fields of the given `comment` and save the
        `comment` to the database.
        '''
        comment.parent_comment = self
        comment.post = self.post
        comment.save()

    def get_child_comments(self):
        '''
        Retrieve all child comments of this parent comment.
        '''
        return Comment.objects.filter(parent_comment=self)
    
    def __str__(self):
        return f"Comment by {self.author}: \"{self.text}\""

class Vote(models.Model):
    '''
    A user can upvote or downvote a `Post` or `Comment`. If the vote belongs to
    a `Post`, then the `comment` field will be null. If the vote belongs to a
    `Comment`, then the `post` field will be null.
    '''

    # Define an enumeration for vote choices
    VOTE_CHOICES = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    )

    # The user that this vote belongs to
    voter = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)

    # The post that this vote belongs to
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

    # The comment that this vote belongs to
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)

    # The vote can either be an 'Upvote' or 'Downvote'
    vote_type = models.CharField(max_length=4, choices=VOTE_CHOICES)

    # The time when this vote was created
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote {self.vote_type} by {self.voter}"

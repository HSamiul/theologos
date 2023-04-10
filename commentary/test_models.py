from django.test import TestCase
from accounts.models import User
from profiles.models import Profile
from .models import Post, Comment, Vote

class CommentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, faith_tradition='PENT')
        self.post = Post.objects.create(author=self.profile, title='Test Post', text='Test post content')
        self.comment = Comment.objects.create(author=self.profile, text='Test comment', post=self.post)

    def test_add_child_comment(self):
        child_comment = Comment.objects.create(author=self.profile, text='Test child comment', post=self.post)
        self.comment.add_child_comment(child_comment)
        self.assertEqual(child_comment.parent_comment, self.comment)
        self.assertEqual(len(self.post.get_comments()), 2)

    def test_get_child_comments(self):
        child_comment_1 = Comment.objects.create(author=self.profile, text='Test child comment 1', post=self.post)
        child_comment_2 = Comment.objects.create(author=self.profile, text='Test child comment 2', post=self.post)
        self.comment.add_child_comment(child_comment_1)
        self.comment.add_child_comment(child_comment_2)
        child_comments = self.comment.get_child_comments()
        self.assertIn(child_comment_1, child_comments)
        self.assertIn(child_comment_2, child_comments)
        self.assertEqual(len(self.post.get_comments()), 3)

class VoteTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, faith_tradition='PENT')
        self.post = Post.objects.create(author=self.profile, title='Test Post', text='Test post content')
        self.comment = Comment.objects.create(author=self.profile, text='Test comment', post=self.post)

    def test_add_post_vote(self):
        vote = Vote.objects.create(voter=self.profile, post=self.post, vote_type='up')
        self.assertEqual(vote.voter, self.profile)
        self.assertEqual(vote.post, self.post)
        self.assertEqual(vote.vote_type, 'up')

    def test_add_comment_vote(self):
        vote = Vote.objects.create(voter=self.profile, post=self.post, comment=self.comment, vote_type='down')
        self.assertEqual(vote.voter, self.profile)
        self.assertEqual(vote.comment, self.comment)
        self.assertEqual(vote.vote_type, 'down')

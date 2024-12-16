from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post

class UserTestCase(TestCase):
    """Test cases for User model functionality"""
    def test_create_user(self):
        """Test user creation and verification should return TRUE"""
        # Create a test user with username, email and password
        test_user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='testPass123..'
        )
        
        # Verify user attributes match what was provided
        self.assertEqual(test_user.username, 'testuser')
        self.assertEqual(test_user.email, 'test@gmail.com')
        self.assertTrue(test_user.check_password('testPass123..'))
        
        # Verify user was properly saved to database
        saved_user = User.objects.get(username='testuser')
        self.assertEqual(saved_user.username, test_user.username)
        self.assertEqual(saved_user.email, test_user.email)

    def test_unsigned_user_create_post(self):
        """Test if an unsigned user can create a post should return FALSE"""
        client = Client()
        
        # Try to create a post without being logged in
        response = client.post(reverse('create_post'), {
            'title': 'Test Post',
            'content': 'Test Content',
            'anonymous_name': 'Anonymous User'
        })
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/create_post/')
        
        # Verify no post was created
        self.assertEqual(Post.objects.count(), 0)

    def test_post_without_header_image(self):
        """Test if a post can be created without header image should return FALSE"""
        # Create and login test user
        test_user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='testPass123..'
        )
        client = Client()
        client.login(username='testuser', password='testPass123..')
        
        # Try to create a post without header image
        response = client.post(reverse('create_post'), {
            'title': 'Test Post',
            'content': 'Test Content',
        })
        
        # Should be successful
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Verify post was created
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'Test Content')
        self.assertIsNone(post.header_image)

    def test_logged_in_user_comment(self):
        """Test if a logged in user can create a comment should return TRUE"""
        # Create and login test user
        test_user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='testPass123..'
        )
        client = Client()
        client.login(username='testuser', password='testPass123..')
        
        # Create a test post first
        post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=test_user
        )
        
        # Try to create a comment on the post
        response = client.post(reverse('view_post', kwargs={'post_id': post.id}), {
            'form_type': 'comment_form',
            'content': 'Test Comment',
            'post_as_anonymous': False
        })
        
        # Should redirect back to post page after successful comment creation
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_post', kwargs={'post_id': post.id}))
        
        # Verify comment was created
        self.assertEqual(post.comments.count(), 1)
        comment = post.comments.first()
        self.assertEqual(comment.content, 'Test Comment')
        self.assertEqual(comment.author, test_user)

    def test_unsigned_user_comment(self):
        """Test if an unsigned user can create a comment should return TRUE"""
        client = Client()
        
        # Create a test post first
        test_user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='testPass123..'
        )
        post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=test_user
        )
        
        # Try to create a comment on the post as unsigned user
        response = client.post(reverse('view_post', kwargs={'post_id': post.id}), {
            'form_type': 'comment_form',
            'content': 'Test Anonymous Comment',
            'anonymous_name': 'Anonymous User'
        })
        
        # Should redirect back to post page after successful comment creation
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_post', kwargs={'post_id': post.id}))
        
        # Verify comment was created
        self.assertEqual(post.comments.count(), 1)
        comment = post.comments.first()
        self.assertEqual(comment.content, 'Test Anonymous Comment')
        self.assertIsNone(comment.author)
        self.assertEqual(comment.anonymous_name, 'Anonymous User')

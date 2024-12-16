from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
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

        def test_post_creation_count(self):
            """Test that creating a post via form URL increases post count"""
            # Get initial post count
            initial_count = Post.objects.count()
                
            # Set up test client and user
            client = Client()
            user = User.objects.create_user(
                username='postuser',
                email='post@test.com', 
                password='testPass123..'
            )
            client.login(username='postuser', password='testPass123..')
            # Make POST request to form URL to create post
            post_data = {
                'title': 'Test Post',
                'content_delta': '{}',
                'header_image': SimpleUploadedFile(
                    name='test_image.jpg',
                    content=b'',
                    content_type='image/jpeg'
                )
            }
            response = client.post('/form', post_data)
                
            # Verify post count increased by 1
            self.assertEqual(Post.objects.count(), initial_count + 1)
                
            # Verify post was created with correct data
            latest_post = Post.objects.latest('date_posted')
            self.assertEqual(latest_post.title, 'Test Post')
            self.assertEqual(latest_post.author, user)

            def test_comment_creation(self):
                """Test that creating a comment on a post works"""
                # Create test user and post
                user = User.objects.signup(
                    username='commentuser',
                    password='testPass123..'
                )
                
                post = Post.objects.create(
                    title='Test Post',
                    content_delta='{}',
                    author=user
                )

                # Create a comment on the post
                comment = Comment.objects.crate(
                    content='Test comment',
                    post=post,
                    author=user
                )

                # Verify comment was created and associated with post
                self.assertEqual(Comment.objects.count(), 1)
                self.assertEqual(post.comments.count(), 1)
                self.assertEqual(comment.content, 'Test comment')
                self.assertEqual(comment.author, user)
                self.assertEqual(comment.post, post)

    def test_index_page_accessible(self):
        """Test that the index page is accessible to all users"""
        # Create test client
        client = Client()
        # Make GET request to index page
        response = client.get('/')
        # Verify successful response
        self.assertEqual(response.status_code, 200)
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
        
from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    """Tests for User model"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        email = 'test@mail.pl'
        password = '2020Pass2020'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email, msg='User email is incorrect')
        self.assertTrue(user.check_password(password), msg='User password is incorrect')

    def test_new_user_email_normalized(self):
        """Test the email for the new user is normalized"""

        email = 'test@MAIL.NET'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower(), msg='Email normalization incorrect')

    def test_new_user_invalid_email(self) -> None:
        """Test creating new user with no email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self) -> None:
        """Test creating a new superuser"""

        user = get_user_model().objects.create_superuser(
            email='test@policja.net',
            password='test123455'
        )

        self.assertTrue(user.is_superuser, msg='Created superuser user isn''t superuser')
        self.assertTrue(user.is_staff, msg='Created super user isn''t staff')

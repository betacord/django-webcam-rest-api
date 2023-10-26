from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class UserAdminSiteTests(TestCase):
    """Tests for User representation in admin panel"""
    def setUp(self):
        """Method for setting up tests"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@mail.net',
            password='test123456'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@mail.net',
            password='pass12345',
            name='test user name'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""

        url = reverse('admin:user_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""

        url = reverse('admin:user_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200, msg='Incorrect response code')

    def test_create_user_page(self):
        """Test create user page works"""

        url = reverse('admin:user_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

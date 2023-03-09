from django.contrib.auth import get_user_model
from django.test import TestCase

class UsersModelTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="normaluser", email="normal@user.com", first_name="Normal", last_name="User", password="foo")
        self.assertIsNotNone(user.username)
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(username="", email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(username="superuser", email="super@user.com", first_name="Super", last_name="User", password="foo")
        self.assertIsNotNone(admin_user.username)
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username="superuser", email="super@user.com",
                password="foo", is_superuser=False)
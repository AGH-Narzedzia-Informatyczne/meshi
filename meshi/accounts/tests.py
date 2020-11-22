from django.test import TestCase
from django.contrib.auth import get_user_model
from account.models import Account
# Create your tests here.

class AccountTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'medo@testemail.com'
        password = 'Testpassword12!'
        username= 'testuser'
        user = Account.objects.create_user(
            email=email,
            password=password,
            username=username
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'medo@TESTUSER.COM'
        user = Account.objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            Account.objects.create_user(None, 'test123')

    def test_create_superuser(self):
        user = Account.objects.create_superuser(
        email='testsuperuser@adminemail.com',
        password ='testadmin123',
        username= 'testadmin'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff) 


class MyAccountManagerTests(TestCase):

    def test_create_user(self):
        Account = get_user_model()
        account = Account.objects.create_user(email='normal@user.com',username='User', password='foo')
        self.assertEqual(account.email, 'normal@user.com')
        self.assertTrue(account.is_active)
        self.assertFalse(account.is_staff)
        self.assertFalse(account.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNotNone(account.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            Account.objects.create_user()
        with self.assertRaises(TypeError):
            Account.objects.create_user(email='')
        with self.assertRaises(ValueError):
            Account.objects.create_user(email='', username='', password="foo")

    def test_create_superuser(self):
        Account = get_user_model()
        admin_user = Account.objects.create_superuser('super@user.com','user', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNotNone(admin_user.username)
        except AttributeError:
            pass
        '''with self.assertRaises(ValueError):
            Account.objects.create_superuser(
                email='super@user.com', password='foo', username='user', is_superuser = True)'''

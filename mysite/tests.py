from django.test import TestCase
from django.contrib.auth.models import User
from django.test import client

# need to be rewrite


class IndexWebpageTestCase(TestCase):

    def setUp(self):
        self.c = client.Client()

    def test_index_visiting(self):
        resp = self.c.get('/index/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<h2>Welcome to restaurant king</h2>')
        self.assertTemplateUsed(resp, 'index.html')


class LoginTestCase(TestCase):

    def setUp(self):
        User.objects.create_user('user',
                                 email='user@example.com', password='abcde')
        self.c = client.Client()

    def test_login_and_logout(self):
        resp = self.c.get('/restaurants_list/')
        # no login, test redirects
        self.assertRedirects(resp,
                             '/accounts/login/?next=/restaurants_list/')

        # django built-in login
        self.c.login(username='user', password='abcde')

        # access after login
        resp = self.c.get('/restaurants_list/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'restaurants_list.html')

        # django built-in logout
        self.c.logout()
        resp = self.c.get('/restaurants_list/')
        self.assertRedirects(resp,
                             '/accounts/login/?next=/restaurants_list/')

    def test_login_and_logout_by_http_protocal(self):
        # no login access
        resp = self.c.get('/restaurants_list/')
        # test redirects
        self.assertRedirects(resp,
                             '/accounts/login/?next=/restaurants_list/')

        # login manually
        resp = self.c.post('/accounts/login/', {'username': 'user',
                           'password': 'abcde'}, follow=True)

        # set LOGIN_REDIRECT_URL in settings.py
        self.assertEqual(resp.redirect_chain,
                         [('http://testserver/index/', 302)])

        # access after login
        resp = self.c.get('/restaurants_list/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'restaurants_list.html')

        # visit logout page to logout manually
        self.c.get('/accounts/logout/')
        resp = self.c.get('/restaurants_list/')
        self.assertRedirects(resp,
                             '/accounts/login/?next=/restaurants_list/')

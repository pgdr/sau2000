from django.test import TestCase, Client
from sau.models import Sheep
from .data import generate_test_db


class TemplateTestcase(TestCase):
    def setUp(self):
        generate_test_db()

    def login(self, do_login=True):
        c = Client()
        if not do_login:
            return c
        login = c.login(username='Smeagol', password='myprecious')
        self.assertTrue(login)
        return c

    def _get_html(self, client, url, **kwargs):
        response = client.get(url, **kwargs)
        self.assertEqual(response.status_code, 200)
        return str(response.content)

    def test_nologin_site(self):
        client = self.login(do_login=False)
        for url in ('/', '/sau/britanna/1', '/sau/nosuchsau/100'):
            response = client.get(url, follow=True)
            self.assertEqual(response.status_code, 200, msg='on url=%s' % url)
            self.assertIn('Django admin', str(response.content))  # go to admin

        for url in ('nosuchpage', ):
            response = client.get(url, follow=True)
            self.assertEqual(response.status_code, 404, msg='on url=%s' % url)

    def test_login_wrong(self):
        client = self.login(do_login=False)
        login_ = client.login(username='nouser', password='nopass')
        self.assertFalse(login_)
        response = client.get('/sau/britanna/1', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Django admin', str(response.content))  # go to admin

    def test_login_site(self):
        client = self.login()
        response = client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hei', str(response.content))
        self.assertIn('Smeagol', str(response.content))

    def test__self_setup(self):
        self.assertEqual(10, len(Sheep.objects.all()))

    def test_index(self):
        client = self.login(do_login=True)
        html = self._get_html(client, '/')
        self.assertIn('2608', html)
        self.assertIn('lolcakes', html)
        self.assertIn('britanna', html)

    def test_sau_statistics(self):
        client = self.login()
        html = self._get_html(client, '/sau/britanna/1')
        self.assertIn('min: 10', html)
        self.assertIn('max: 12', html)
        self.assertEqual(3, html.count('<svg'))

    def test_stats(self):
        client = self.login()
        html = self._get_html(client, '/stats')
        self.assertEqual(2, html.count('<svg'))

    def test_sau_edit(self):
        client = self.login()
        html = self._get_html(client, '/sau/britanna/1/edit')
        self.assertIn('Advanced editor', html)

    def test_search(self):
        client = self.login()
        html = self._get_html(client, '/search?q=brit')
        self.assertIn('Found 1 ', html)

        html = self._get_html(client, '/search?q=rb')
        self.assertIn('Found 6 ', html)

        html = self._get_html(client, '/search?q=rb&s=prod')
        self.assertIn('Found 4 ', html)

        html = self._get_html(client, '/search?q=rb&s=noprod')
        self.assertIn('Found 2 ', html)

from datetime import datetime as dt
from django.test import TestCase, Client
from django.contrib.auth.models import User
from sau.models import Sheep, Farm, Medicine, Dose

def generate_sheep_db():
    s = Sheep.objects.create(name='britanna',
                             birth_date_utc=dt.now(),
                             sex='f',
                             farm=Farm.objects.all()[0])
    s.save()


class TemplateTestcase(TestCase):

    @classmethod
    def setUpClass(cls):
        farm = Farm.objects.create(name='Misty Mountains')
        cls.username = 'Smeagol'
        cls.password = 'myprecious'
        cls.user = User.objects.create_user(username=cls.username,
                                             password=cls.password)
        farm.farmers.add(cls.user)
        farm.save()
        generate_sheep_db()

    def setUp(self):
        self.c = Client()


    def test_nologin_site(self):
        for url in ('/', '/sau/britanna', '/sau/nosuchsau'):
           response = self.c.get(url, follow=True)
           self.assertEqual(response.status_code, 200, msg='on url=%s'%url)
           self.assertIn('Django admin', str(response.content))  # go to admin

        for url in ('nosuchpage',):
           response = self.c.get(url, follow=True)
           self.assertEqual(response.status_code, 404, msg='on url=%s'%url)


    def test_login_wrong(self):
        login = self.c.login(username='nouser', password='nopass')
        response = self.c.get('/sau/britanna', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Django admin', str(response.content))  # go to admin

    def test_login_site(self):
        login = self.c.login(username=self.username, password=self.password)
        self.assertEqual(True, login)
        response = self.c.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hei', str(response.content))
        self.assertIn(self.username, str(response.content))


    @classmethod
    def tearDownClass(cls):
        pass

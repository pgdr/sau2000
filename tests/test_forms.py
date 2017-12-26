from django.test import TestCase, Client
from sau.forms import SheepForm


class SheepFormTests(TestCase):

    def test_valid(self):
        form = SheepForm(data={'name': 'testsau', 'sex': 'm', 'ear_tag_color': 'w', 'birth_date_utc': '2010-01-01 06:00:00', })
        self.assertTrue(form.is_valid())

    def test_invalid(self):        
        form = SheepForm(data={'name': 'testsau', 'sex': 'm', })
        
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['ear_tag_color'], ['This field is required.'])
        self.assertEqual(form.errors['birth_date_utc'], ['This field is required.'])

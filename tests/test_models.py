from datetime import datetime
from django.test import TestCase
from sau.models import Sheep


class SheepTestcase(TestCase):
    def setUp(self):
        self.instance = Sheep.objects.create(name='britanna',
                                             birth_date_utc=datetime.now(),
                                             sex='f')

    def test_sheep_name(self):
        sau = Sheep.objects.get(name='britanna')
        self.assertIsNotNone(sau)

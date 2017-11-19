from datetime import datetime
from django.test import TestCase
from sau.models import Sheep


class SheepTestcase(TestCase):
    def setUp(self):
        self.instance = Sheep.objects.create(name='britanna',
                                             birth_date_utc=datetime.now(),
                                             sex='f')
        Sheep.objects.create(name='lolcakes',
                             birth_date_utc=datetime.now(),
                             sex='f',
                             ear_tag='2608',
                             ear_tag_color='r')

    def test_sheep_name(self):
        sau = Sheep.objects.get(name='britanna')
        self.assertIsNotNone(sau)

    def test_sheep_tag(self):
        sau = Sheep.objects.get(name='britanna')
        self.assertEqual('', sau.ear_tag)
        self.assertEqual('w', sau.ear_tag_color)
        lol = Sheep.objects.get(name='lolcakes')
        color, tag = lol.colored_tag
        self.assertEqual('r', color)
        self.assertEqual('2608', tag)

    def test_sheep_alive(self):
        sau = Sheep.objects.get(name='britanna')
        self.assertEqual('', sau.quality)
        self.assertTrue(sau.alive)

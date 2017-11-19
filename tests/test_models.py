from datetime import datetime
from django.test import TestCase
from sau.models import Sheep

SAUS = [
    {
        'name': 'britanna',
        'birth_date_utc': datetime.now(),
        'sex': 'f',
    },
    {
        'name': 'lolcakes',
        'birth_date_utc': datetime.now(),
        'sex': 'f',
        'ear_tag': '2608',
        'ear_tag_color': 'r',
        'quality': 'e+',
    },
    {
        'name': 'rambo',
        'birth_date_utc': datetime.now(),
        'sex': 'm',
        'quality': 'p-',
    },
]


def get_sheep(names):
    return [Sheep.objects.get(name=n) for n in names]


class SheepTestcase(TestCase):
    def setUp(self):
        for sau in SAUS:
            s = Sheep.objects.create(**sau)
            s.save()

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

    def test_parenthood(self):
        l, r = get_sheep(('lolcakes', 'rambo'))
        self.assertIsNone(l.father)
        self.assertIsNone(l.mother)
        self.assertIsNone(r.father)
        self.assertIsNone(r.mother)

        ram = Sheep.objects.create(
            name='boy',
            birth_date_utc=datetime.now(),
        )

        ram.save()
        ram.father = r
        ram.mother = l
        ram.save()
        self.assertEqual(l, ram.mother)
        self.assertEqual(r, ram.father)

    def test_qualities(self):
        l, r, b = get_sheep(('lolcakes', 'rambo', 'britanna'))
        self.assertEqual('e+', l.quality)
        self.assertEqual('p-', r.quality)
        self.assertEqual('', b.quality)

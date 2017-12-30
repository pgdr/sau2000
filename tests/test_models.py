from datetime import datetime as dt
from django.test import TestCase
from sau.models import Sheep, Farm

from .data import generate_test_db, get_sheep, date


class SheepTestcase(TestCase):
    def setUp(self):
        generate_test_db()

    def test__self_setup(self):
        self.assertEqual(9, len(Sheep.objects.all()))

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
        rba = Sheep.objects.get(name='rb_a')
        self.assertFalse(rba.alive)

    def test_parenthood(self):
        l, r = get_sheep(('lolcakes', 'rambo'))
        self.assertIsNone(l.father)
        self.assertIsNone(l.mother)
        self.assertIsNone(r.father)
        self.assertIsNone(r.mother)

        ram = Sheep.objects.create(
            name='boy',
            farm=Farm.objects.all()[0],
            birth_date_utc=dt.now(),
        )

        ram.save()
        ram.father = r
        ram.mother = l
        ram.save()
        self.assertEqual(l, ram.mother)
        self.assertEqual(r, ram.father)

    def test_prod(self):
        b, child = get_sheep(('britanna', 'rb_a'))
        self.assertEqual(b, child.mother)

    def test_qualities(self):
        l, r, b = get_sheep(('lolcakes', 'rambo', 'britanna'))
        self.assertEqual('e+', l.quality)
        self.assertEqual('p-', r.quality)
        self.assertEqual('', b.quality)

    def test_children(self):
        l, r, b = get_sheep(('lolcakes', 'rambo', 'britanna'))
        self.assertEqual(0, len(l.children))
        self.assertEqual(0, len(l.children_tree))

        self.assertEqual(6, len(r.children))
        self.assertEqual(6, len(r.children_tree))

        self.assertEqual(3, len(b.children))
        self.assertEqual(6, len(b.children_tree))

        rb_a = get_sheep(('rb_a', ))[0]
        self.assertIn(rb_a, b.children_tree)

    def test_farm(self):
        f = Farm.objects.create(name='Flatråker')
        f.save()

        sau = Sheep.objects.get(name='britanna')
        sau.farm = f
        sau.save()

        self.assertEqual(f.name, sau.farm.name)

    def test_batch(self):
        britanna, rambo = get_sheep(('britanna', 'rambo'))
        self.assertEqual(9, len(Sheep.objects.all()))
        self.assertEqual(3, len(britanna.children))
        self.assertEqual(6, len(rambo.children))

        batch = Sheep.batch(farm=Farm.objects.all()[0],
                            mother=britanna,
                            father=rambo,
                            ewes=3,
                            rams=2,
                            birth_date_utc=date())
        self.assertEqual(5, len(batch))
        ewes = len([x for x in batch if x.sex == 'f'])
        rams = len([x for x in batch if x.sex == 'm'])
        self.assertEqual(3, ewes)
        self.assertEqual(2, rams)
        self.assertEqual(set([date()]), set([x.birth_date_utc for x in batch]))
        self.assertEqual(9+5, len(Sheep.objects.all()))
        self.assertEqual(3+5, len(britanna.children))
        self.assertEqual(6+5, len(rambo.children))

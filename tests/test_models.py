from datetime import datetime as dt
from django.test import TestCase
from sau.models import Sheep, Farm

from .data import generate_test_db, get_sheep, date


class SheepTestcase(TestCase):
    def setUp(self):
        generate_test_db()

    def test__self_setup(self):
        self.assertEqual(10, len(Sheep.objects.all()))

    def test_sheep_name(self):
        sau = Sheep.objects.get(id=1)
        self.assertIsNotNone(sau)

    def test_sheep_tag(self):
        sau = Sheep.objects.get(id=1)
        self.assertEqual('', sau.ear_tag)
        self.assertEqual('w', sau.ear_tag_color)
        lol = Sheep.objects.get(id=2)
        color, tag = lol.colored_tag
        self.assertEqual('r', color)
        self.assertEqual('2608', tag)

    def test_sheep_alive(self):
        sau = Sheep.objects.get(id=1)
        self.assertEqual('', sau.quality)
        self.assertTrue(sau.alive)
        rba = Sheep.objects.get(id=5)
        self.assertFalse(rba.alive)

    def test_parenthood(self):
        l, r = get_sheep((2, 3))
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
        b, child = get_sheep((1, 5))
        self.assertEqual(b, child.mother)

    def test_qualities(self):
        l, r, b = get_sheep((2, 3, 1))
        self.assertEqual('e+', l.quality)
        self.assertEqual('p-', r.quality)
        self.assertEqual('', b.quality)

    def test_children(self):
        l, r, b = get_sheep((2, 3, 1))
        self.assertEqual(0, len(l.children))
        self.assertEqual(0, len(l.children_tree))

        self.assertEqual(6, len(r.children))
        self.assertEqual(6, len(r.children_tree))

        self.assertEqual(3, len(b.children))
        self.assertEqual(6, len(b.children_tree))

        rb_a = get_sheep((5, ))[0]
        self.assertIn(rb_a, b.children_tree)

    def test_farm(self):
        f = Farm.objects.create(name='Flatråker')
        f.save()

        sau = Sheep.objects.get(id=1)
        sau.farm = f
        sau.save()

        self.assertEqual(f.name, sau.farm.name)


class BatchTestCase(TestCase):
    def setUp(self):
        generate_test_db()

        self.father = Sheep.objects.create(
            name='father',
            farm=Farm.objects.all()[0],
            birth_date_utc=dt.now(),
        )

        self.mother = Sheep.objects.create(
            name='mother',
            farm=Farm.objects.all()[0],
            birth_date_utc=dt.now(),
        )

    def test_mother_only(self):
        Sheep.batch(farm=Farm.objects.all()[0],
                            mother=self.mother,
                            father=None,
                            ewes=2,
                            rams=0,
                            birth_date_utc=date())

        self.assertEqual(2, len(self.mother.children))

    def test_with_father(self):
        batch = Sheep.batch(farm=Farm.objects.all()[0],
                            mother=self.mother,
                            father=self.father,
                            ewes=2,
                            rams=1,
                            birth_date_utc=date())

        self.assertEqual(3, len(self.father.children))
        self.assertEqual(set([date()]), set([x.birth_date_utc for x in batch]))

    def test_children(self):
        batch = Sheep.batch(farm=Farm.objects.all()[0],
                            mother=self.mother,
                            father=self.father,
                            ewes=3,
                            rams=2,
                            birth_date_utc=date())
        ewes = len([x for x in batch if x.sex == 'f'])
        rams = len([x for x in batch if x.sex == 'm'])
        self.assertEqual(3, ewes)
        self.assertEqual(2, rams)

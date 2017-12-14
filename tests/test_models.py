from datetime import datetime as dt
from django.test import TestCase
from sau.models import Sheep, Medicine, Dose

def date(y=2010, m=1, d=1, h=6, min_=0, sec=0):
    return dt(y, m, d, h, min_, sec)

SAUS = [
    {
        'name': 'britanna',
        'birth_date_utc': date(),
        'sex': 'f',
    },
    {
        'name': 'lolcakes',
        'birth_date_utc': date(),
        'sex': 'f',
        'ear_tag': '2608',
        'ear_tag_color': 'r',
        'quality': 'e+',
    },
    {
        'name': 'rambo',
        'birth_date_utc': date(),
        'sex': 'm',
        'quality': 'p-',
    },
    {
        'name': 'rb_a',
        'birth_date_utc': date(2012),
        'sex': 'm',
        'quality': 'r',
        'weight': 1000,
        'fat_percentage': 0.8,
    },
    {
        'name': 'rb_b',
        'birth_date_utc': date(2012),
        'sex': 'm',
        'quality': 'u',
        'weight': 1100,
        'fat_percentage': 0.8,
    },
    {
        'name': 'rb_c',
        'birth_date_utc': date(2012),
        'sex': 'f',
        'quality': 'e',
        'weight': 1200,
        'fat_percentage': 0.8,
    },
    {
        'name': 'rb_c_a',
        'birth_date_utc': date(2013),
        'sex': 'm',
        'quality': 'r',
        'weight': 600,
        'fat_percentage': 0.2,
    },
    {
        'name': 'rb_c_b',
        'birth_date_utc': date(2013),
        'sex': 'm',
        'quality': 'u',
        'weight': 700,
        'fat_percentage': 0.3,
    },
    {
        'name': 'rb_c_c',
        'birth_date_utc': date(2013),
        'sex': 'm',
        'quality': 'e',
        'weight': 800,
        'fat_percentage': 0.4,
    },
]


def generate_sheep_db():
    for sau in SAUS:
        s = Sheep.objects.create(**sau)
        s.save()
    r,b = get_sheep(['rambo','britanna'])
    rb_a = Sheep.objects.get(name='rb_a')
    rb_b = Sheep.objects.get(name='rb_b')
    rb_c = Sheep.objects.get(name='rb_c')
    for s in (rb_a, rb_b, rb_c):
        s.father = r
        s.mother = b
        s.save()
    rb_c_a = Sheep.objects.get(name='rb_c_a')
    rb_c_b = Sheep.objects.get(name='rb_c_b')
    rb_c_c = Sheep.objects.get(name='rb_c_c')
    for s in (rb_c_a, rb_c_b, rb_c_c):
        s.father = r
        s.mother = rb_c
        s.save()


def get_sheep(names):
    return [Sheep.objects.get(name=n) for n in names]


class SheepTestcase(TestCase):

    def setUp(self):
        generate_sheep_db()

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

    def test_parenthood(self):
        l, r = get_sheep(('lolcakes', 'rambo'))
        self.assertIsNone(l.father)
        self.assertIsNone(l.mother)
        self.assertIsNone(r.father)
        self.assertIsNone(r.mother)

        ram = Sheep.objects.create(
            name='boy',
            birth_date_utc=dt.now(),
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

    def test_children(self):
        l, r, b = get_sheep(('lolcakes', 'rambo', 'britanna'))
        self.assertEqual(0, len(l.children))
        self.assertEqual(0, len(l.children_tree))

        self.assertEqual(6, len(r.children))
        self.assertEqual(6, len(r.children_tree))

        self.assertEqual(3, len(b.children))
        self.assertEqual(6, len(b.children_tree))



class MedicineTestcase(TestCase):
    def _init_saus(self):
        for sau in SAUS:
            s = Sheep.objects.create(**sau)
            s.save()

    def setUp(self):
        self._init_saus()
        self.l, self.r = get_sheep(('lolcakes', 'rambo'))

        self.med = Medicine.objects.create(
            name='Paracit', description='For headaches or headcakes')
        self.med.save()
        self.dose = Dose.objects.create(
            medicine=self.med, sheep=self.l, amount=200)
        self.dose = Dose.objects.create(
            medicine=self.med, sheep=self.r, amount=250)
        self.dose.save()

    def test_dose(self):
        self.assertEqual(2, len(Dose.objects.all()))
        self.assertEqual(1, len(Medicine.objects.all()))

        dr = Dose.objects.get(sheep=self.r)
        self.assertEqual(250, dr.amount)
        dl = Dose.objects.get(sheep=self.l)
        self.assertEqual(200, dl.amount)

    def test_sheep_dose(self):
        doses = Dose.get(sheep=self.r)
        self.assertEqual(1, len(doses))
        dose = doses[0]
        self.assertEqual(250, dose.amount)
        self.assertEqual('Paracit', dose.medicine.name)

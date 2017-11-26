from datetime import datetime
from django.test import TestCase
from sau.models import Sheep, Medicine, Dose

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

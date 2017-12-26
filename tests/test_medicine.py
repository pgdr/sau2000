from django.test import TestCase
from sau.models import Medicine, Dose

from .data import generate_test_db, get_sheep


class MedicineTestcase(TestCase):
    def setUp(self):
        generate_test_db()
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

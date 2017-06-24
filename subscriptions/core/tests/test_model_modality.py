from django.core.exceptions import ValidationError
from django.test import TestCase
from model_mommy import mommy

from subscriptions.core.models import Modality


class ModalityModelTest(TestCase):
    def setUp(self):
        self.modality = Modality(
            modality='3',
            file_modality='3km ',
        )
        # self.modality = mommy.prepare(Modality)

    def test_create_modality(self):
        self.modality.save()
        self.assertTrue(Modality.objects.exists())

    def test_invalid_modality_choice(self):
        modality = mommy.prepare(Modality, modality='invalid')

        with self.assertRaises(ValidationError):
            modality.save()
        self.assertFalse(Modality.objects.exists())

    def test_str(self):
        self.assertEqual(self.modality.modality, str(self.modality))

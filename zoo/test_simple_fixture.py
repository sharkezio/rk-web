from django.test import TestCase
from zoo.models import Dog


class SimpleTestCase(TestCase):
    fixtures = ['dog.json']

    def test_dog_fixture(self):
        snoopy = Dog.objects.get(id=1)
        self.assertEqual(snoopy.name, 'Snoopy')

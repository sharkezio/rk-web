from django.test import TestCase
from zoo import models


class AnimalTestCase(TestCase):

    def test_dogs_says(self):
        dog = models.Dog(name='Snoopy')
        # self.assertEqual(dog.says(), '...')  # test error simulate
        self.assertEqual(dog.says(), 'woof')

    def test_cat_says(self):
        cat = models.Cat(name='Garfield')
        self.assertEqual(cat.says(), 'meow')

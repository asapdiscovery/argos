from django.test import TestCase

# Create your tests here.

class BlankTest(TestCase):
    def test_placeholder(self):
        self.assertEqual(1, 1)

    def test_fail(self):
        self.assertEqual(1,2)

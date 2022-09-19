import unittest
from django.test import TestCase
from materials.docs.models import *


class TestReminder(TestCase):
    def test_reminder(self):
        doc = Document.objects.all()
        print(doc)

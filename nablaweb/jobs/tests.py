# -*- coding: utf-8 -*-

# Automatisert testing av jobs-appen i NablaWeb-appen

import unittest
from django.test import TestCase
from jobs.templatetags.jobs_filters import commas_no
from jobs.models import TagChoices



class NorwegianCommasTest(TestCase):
    __name__ = "some_name"

    def setUp(self):
        for i in range(5):
            TagChoices.objects.create(tag=str(i))

    def test_list_contains_no_elements(self):
        self.assertEqual("", commas_no([]))

    @unittest.skip
    def test_list_contains_one_element(self):
        element = "hei"
        self.assertEqual(element, commas_no([element]))

    def test_queryset_contains_no_elements(self):
        queryset = TagChoices.objects.filter(id=1000)
        self.assertEqual("", commas_no(queryset))

    def test_queryset_contains_one_element(self):
        queryset = TagChoices.objects.all()[:1]
        self.assertEqual("0", commas_no(queryset))

    def test_queryset_contains_two_elements(self):
        queryset = TagChoices.objects.all()[:2]
        self.assertEqual("0 og 1", commas_no(queryset))

    def test_queryset_contains_three_elements(self):
        queryset = TagChoices.objects.all()[:3]
        self.assertEqual("0, 1 og 2", commas_no(queryset))

    def test_queryset_contains_five_elements(self):
        queryset = TagChoices.objects.all()[:5]
        self.assertEqual("0, 1, 2, 3 og 4", commas_no(queryset))


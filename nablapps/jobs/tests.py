from django.test import TestCase
from nablapps.jobs.models import TagChoices
from nablapps.jobs.templatetags.jobs_filters import commas_no


class NorwegianCommasTest(TestCase):

    def setUp(self):
        for i in range(5):
            TagChoices.objects.create(tag=str(i))

    def test_list_contains_no_elements(self):
        self.assertEqual("", commas_no([]))

    def test_list_contains_one_element(self):
        element = "hei"
        self.assertEqual(element, commas_no([element]))

    def test_list_of_5_elements(self):
        self.assertEqual("0, 1, 2, 3 og 4", commas_no(range(5)))

    def test_queryset_contains_no_elements(self):
        queryset = TagChoices.objects.filter(id=1000)
        self.assertEqual("", commas_no(queryset))

    def test_queryset_contains_one_element(self):
        queryset = TagChoices.objects.all()[:1]
        self.assertEqual(str(queryset[0]), commas_no(queryset))

    def test_queryset_contains_two_elements(self):
        queryset = TagChoices.objects.all()[:2]
        self.assertEqual(f"{queryset[0]} og {queryset[1]}", commas_no(queryset))

    def test_queryset_contains_three_elements(self):
        queryset = TagChoices.objects.all()[:3]
        strings = [str(x) for x in queryset]
        self.assertEqual(f"{strings[0]}, {strings[1]} og {strings[2]}", commas_no(queryset))

    def test_queryset_contains_five_elements(self):
        queryset = TagChoices.objects.all()[:5]
        strings = [str(x) for x in queryset]
        self.assertEqual("{}, {}, {}, {} og {}".format(*strings), commas_no(queryset))

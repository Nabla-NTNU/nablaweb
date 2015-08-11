# -*- coding: utf-8 -*-

from haystack.forms import SearchForm

class NewSearchForm(SearchForm):
    def search(self):
        s = super(NewSearchForm, self).search()
        return s

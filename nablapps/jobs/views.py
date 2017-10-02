from content.templatetags.listutil import row_split
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from nablapps.jobs.models import Advert, Company, YearChoices, RelevantForChoices, TagChoices


def split_into_rows(jobs):
    """Deler f.eks. opp [1, 2, 3, 4, 5] til [[1, 2], [3, 4], [5]]."""
    return row_split(jobs, 2) if jobs else None


class GenericJobsList(ListView):
    """Abstrakt rotklasse som håndterer info for sidebaren."""
    context_object_name = 'jobs_list'
    template_name = 'jobs/jobs_list.html'
    paginate_by = 8
    model = Advert

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['years'] = YearChoices.objects.all()
        context['choices'] = RelevantForChoices.objects.all()
        context['tags'] = TagChoices.objects.all()

        paginator = Paginator(self.object_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            jobs_rows = paginator.page(page)
        except PageNotAnInteger:
            jobs_rows = paginator.page(1)
        except EmptyPage:
            jobs_rows = paginator.page(paginator.num_pages)

        context['jobs_rows'] = split_into_rows(jobs_rows)

        return context


class EverythingList(GenericJobsList):
    """Alle aktive stillingsannonser."""
    def get_queryset(self):
        return Advert.objects.active()


class CompanyList(GenericJobsList):
    """Stillingsannonser for en spesifikk bedrift."""
    def get_queryset(self):
        company = get_object_or_404(Company, id=self.kwargs['pk'])
        return super().get_queryset().filter(company=company)


class YearList(GenericJobsList):
    """Stillingsannonser som er lagt inn dette året."""
    def get_queryset(self):
        return super().get_queryset().filter(created_date__year=self.kwargs['year'])


class MonthList(YearList):
    """Stillingsannonser som er lagt inn denne måneden."""
    def get_queryset(self):
        return super().get_queryset().filter(created_date__month=self.kwargs['month'])


class TagList(GenericJobsList):
    """Stillingsannonser merket med en spesifikk tag."""
    def get_queryset(self):
        return super().get_queryset().filter(tags__tag__iexact=self.kwargs['tag'])


class RelevantForLinjeList(GenericJobsList):
    """Stillingsannonser merket som relevante for en spesifikk studieretning."""
    def get_queryset(self):
        return super().get_queryset()\
            .filter(relevant_for_group__studieretning__iexact=self.kwargs['linje'])


class RelevantForYearList(GenericJobsList):
    """Stillingsannonser merket som relevante for et spesifikt årskull."""
    def get_queryset(self):
        return super(RelevantForYearList, self).get_queryset()\
            .filter(relevant_for_year__year__iexact=self.kwargs['year'])


class ShowJob(DetailView):
    """Detaljviewet for en spesifikk stillingsannonse."""
    model = Advert
    context_object_name = 'job'
    template_name = "jobs/jobs_detail.html"

from django.views.generic import DetailView, ListView
from .models import ComPage, ComMembership


class ShowPage(DetailView):
    template_name = 'com/com_details.html'
    model = ComPage
    context_object_name = 'com'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        com = self.get_object().com
        context['members'] = ComMembership.objects.filter(
                com=com, is_active=True).order_by('joined_date')
        context['compages'] = ComPage.objects.order_by('com__name')
        return context


class CommitteeOverview(ListView):
    template_name = 'com/committee_overview.html'

    model = ComPage


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        committees = ComPage.objects.filter(is_interest_group=False).order_by('com__name')
        interest_groups = ComPage.objects.filter(is_interest_group=True).order_by('com__name')

        context['committees'] = committees
        context['interest_groups'] = interest_groups

        return context

"""
Views for nablad apps
"""
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, HttpResponseRedirect, reverse
from django.utils import formats
from django.views.generic import DetailView, TemplateView
from django.http import HttpResponse
from django.conf import settings
from nablapps.core.view_mixins import AdminLinksMixin
from .models import Nablad


class NabladDetailView(AdminLinksMixin, DetailView):
    """Show a single nablad"""
    model = Nablad
    template_name = 'nabladet/nablad_detail.html'
    context_object_name = 'nablad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        nablad_archive = {}
        nablad_list = Nablad.objects.all()

        if not self.request.user.is_authenticated:
            nablad_list = nablad_list.exclude(is_public=False)

        # Creates a dictionary with publication year as key and
        # a list of all nablads from that year as value.
        for n in nablad_list:
            year = formats.date_format(n.pub_date, "Y")
            nablad_archive[year] = nablad_archive.get(year, []) + [n]

        context['nablad_archive'] = nablad_archive

        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            nablad = self.get_object()
            if not nablad.is_public:
                return redirect_to_login(next=nablad.get_absolute_url())
        return super().get(request, *args, **kwargs)


def serve_nablad(request, path):
    """
    View for serving nablad-pdfs if they are public or if the user is logged in.
    Uses nginx X-accel to serve the files when DEBUG=False.
    """
    if not request.user.is_authenticated:
        filename = 'nabladet/' + path
        nablad = get_object_or_404(Nablad, filename=filename)
        if not nablad.is_public:
            return redirect_to_login(next=nablad.get_absolute_url())

    #if settings.DEBUG:
    #    return HttpResponseRedirect(reverse('serve_nablad_debug', kwargs={'path': path}))

    response = HttpResponse()
    response['Content-Type'] = "application/pdf"
    response['X-Accel-Redirect'] = "/{0}/nabladet/{1}".format(settings.PROTECTED_MEDIA_FOLDER, path)

    return response


class NabladList(TemplateView):
    """View for listing nablad"""
    template_name = "nabladet/nablad_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nablad_list = Nablad.objects.all()
        if not self.request.user.is_authenticated:
            nablad_list = nablad_list.exclude(is_public=False)

        nablad_archive = {}

        # Place the nablads in a dictonary with key = publication year
        # and value = a list of nablads from that year
        for nablad in nablad_list:
            nablad_archive.setdefault(formats.date_format(nablad.pub_date, "Y"), []).append(nablad)

        context['nablad_archive'] = nablad_archive
        context['current_year'] = max(nablad_archive.keys())
        return context

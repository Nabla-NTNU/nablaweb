# -*- coding: utf-8 -*-

from meeting_records.models import MeetingRecord
from functools import wraps
from django.contrib import admin
from content.admin import ContentAdmin


# Stygg hack for å endre navnet på appen i admin
def rename_app_list(func):
    m = {'Meeting_Records': 'Referater'}

    @wraps(func)
    def _wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        app_list = response.context_data.get('app_list')

        if app_list is not None:
            for a in app_list:
                name = a['name']
                a['name'] = m.get(name, name)
        title = response.context_data.get('title')
        if title is not None:
            app_label = title.split(' ')[0]
            if app_label in m:
                response.context_data['title'] = "%s administration" % m[app_label]
        return response
    return _wrapper


class MeetingRecordAdmin(ContentAdmin):
    fields = ("picture",
              "cropping",
              "headline",
              "slug",
              "lead_paragraph",
              "body",
              "priority",
              "pub_date",
              "file")
    prepopulated_fields = {"slug": ("headline",)}

admin.site.register(MeetingRecord, MeetingRecordAdmin)
admin.site.__class__.index = rename_app_list(admin.site.__class__.index)
admin.site.__class__.app_index = rename_app_list(admin.site.__class__.app_index)

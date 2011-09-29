from gallery.models import *
from django.contrib import admin

"""
class PictureAdmin(admin.ModelAdmin):

    list_display= ('__unicode__', 'id','picture', 'album')
    fieldsets = [
        ('Tittel',      {'fields':['title']}),
        ('Bilde',       {'fields':['picture']}),
        ('Album',       {'fields':['album']}),    
        ('Beskrivelse', {'fields':['description'], 'classes': ['collapse']}), 
    ]
"""

class PictureInline(admin.TabularInline):
    model = Picture
    extra = 3


class AlbumAdmin(admin.ModelAdmin):
    actions=['really_delete_selected']

    def get_actions(self, request):
        actions = super(AlbumAdmin, self).get_actions(request)
        #del actions['delete_selected']
        return actions

    def delete_view(self, request, object_id, extra_context=None):
        # if request.POST is set, the user already confirmed deletion
        if not request.POST:
            perform_my_action()
        super(MyModelAdmin, self).delete_view(request, object_id, extra_context)

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 album entry was"
        else:
            message_bit = "%s album entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)
    really_delete_selected.short_description = "[HOMEMADE] Delete selected entries"
#    list_display = ('title', 'description')
#    fieldsets = [    
#        ('Tittel',      {'fields':['title']}),
#        ('Beskrivelse', {'fields':['description']}),
#    ]
#    inlines = [PictureInline]
#admin.site.register(Picture, PictureAdmin)
admin.site.register(Picture)
admin.site.register(Album, AlbumAdmin)
#admin.site.register(Picture, PictureAdmin)


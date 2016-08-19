from django.contrib import admin
from .models import Universitet, Utveksling,Link


class UtvekslingAdmin(admin.ModelAdmin):
    list_display = ["student_navn"]
    search_fields = ["student_navn"]

    class Meta:
        model = Utveksling

class UniversitetAdmin(admin.ModelAdmin):
    list_display = ["univ_navn"]
    search_fields = ["univ_navn"]

    class Meta:
        model = Universitet

class LinkAdmin(admin.ModelAdmin):
    list_display = ["link_info"]
    search_fields = ["link_info"]

    class Meta:
        model = Link

admin.site.register(Utveksling,UtvekslingAdmin)
admin.site.register(Universitet,UniversitetAdmin)
admin.site.register(Link,LinkAdmin)

# Register your models here.

# -*- coding: utf-8 -*-
from django.contrib import admin
from image_cropping import ImageCroppingMixin


class ContentAdmin(ImageCroppingMixin, admin.ModelAdmin):


    def save_model(self, request, obj, form, change):
        obj.last_changed_by = request.user

        # Hvis objekter ikke er laget av noen, legg til denne brukeren
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()
        
    def tweet(self, request, content_list):
        if len(content_list) > 1:
            self.message_user(request, "Du kan bare twitre en ting om gangen")
        else:
            from nablaweb.twitter import utils

            content = content_list[0]
            msg = "(Test, ignorer dette) http://nabla.no" +  \
                  content.get_absolute_url() + " : "  +  \
                  content.headline
            try:
                utils.tweet(msg)
            except TweepError:
                self.message_user(request, u"Meldingen ble for lang. Tips: Gjør slug-en og/eller tittelen kortere")
                
            self.message_user(request, "Du har twitret '" + msg + "' som @nabla_ntnu")
    tweet.short_description = "Post link og overskrift til Twitter"


    actions = [tweet]

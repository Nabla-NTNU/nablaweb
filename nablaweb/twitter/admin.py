# -*- coding: utf-8 -*-

class TweetMixin(object):

    def __init__(self):
        self.actions.append(tweet)

    def tweet(self, request, content_list):
        if len(content_list) > 1:
            self.message_user(request, "Du kan bare twitre en ting om gangen")
        else:
            from twitter import utils

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

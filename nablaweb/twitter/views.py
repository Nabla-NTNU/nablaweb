# -*- coding: utf-8 -*-

# Views for twitter-appen

from django.views.generic import ListView, RedirectView
from django.shortcuts import get_object_or_404, get_list_or_404
import twitter

def getRecentTweets(n, user):
	api = twitter.Api()
	tweets = api.GetUserTimeline(user)
	return tweets

class ListLatest(ListView):
	context_object_name = "content_list"
	template_name = "content/content_list.html"
	getRecentTweets(5, "aqwis")

class RedirectToFrontpage(RedirectView):
	def get_redirect_url(self, **kwargs):
		url = "#footer";
		return url

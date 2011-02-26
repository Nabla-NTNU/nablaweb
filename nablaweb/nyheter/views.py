from nyheter.models import News
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

def show_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if news.author_name:
        author_name = news.author_name
    else:
        author_name = news.user.get_full_name()
    return render_to_response('nyheter/news_article.html', {'news': news, 'author_name':author_name})

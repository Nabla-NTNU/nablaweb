
from ..models.blog import *
from .mixins import AdminLinksMixin
from django.views.generic import DetailView, ListView
from django.http import HttpResponseNotFound


class BlogPostView(AdminLinksMixin, DetailView):
    model = BlogPost
    template_name = "content/blog_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = kwargs['object']
        post.add_view()
        context['blog'] = post.blog
        context['post_list'] = BlogPost.objects.filter(blog=post.blog).order_by('-created_date')
        return context


class BlogView(ListView):
    model = BlogPost
    template_name = "content/blog_view.html"
    context_object_name = "post_list"
    paginate_by = 5

    def get(self, *args, **kwargs):
        slug = kwargs.get('blog')
        try:
            self.blog = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            return HttpResponseNotFound()

        return super().get(*args, **kwargs)

    def get_queryset(self):
        return BlogPost.objects.filter(blog=self.blog).order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = self.blog
        return context


class BlogListView(ListView):
    model = Blog
    template_name = "content/blog_list.html"
    context_object_name = "blog_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = BlogPost.objects.order_by('-created_date')[:5]
        return context

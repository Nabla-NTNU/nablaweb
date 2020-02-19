"""
Views for blog app
"""
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.views.generic import DetailView, ListView

from nablapps.core.view_mixins import AdminLinksMixin

from .models import Blog, BlogPost


class BlogPostView(AdminLinksMixin, DetailView):
    """
    Show a single blog post
    """

    model = BlogPost
    template_name = "blog/blog_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = kwargs["object"]
        context["blog"] = post.blog
        context["post_list"] = BlogPost.objects.filter(blog=post.blog).order_by(
            "-created_date"
        )
        return context

    def get_admin_links(self):
        return [
            {
                "name": "Bloggadmin",
                "glyphicon_symbol": "cog",
                "url": reverse("admin:blog_blog_change", args=[self.object.blog.id]),
            },
            *super().get_admin_links(),
        ]


class BlogView(AdminLinksMixin, ListView):
    """
    View for a blog also lists the posts in the blog
    """

    model = BlogPost
    template_name = "blog/blog_view.html"
    context_object_name = "post_list"
    paginate_by = 5
    blog = None

    def get(self, request, *args, **kwargs):
        slug = kwargs.get("blog")
        try:
            self.blog = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            return HttpResponseNotFound()

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return BlogPost.objects.filter(blog=self.blog).order_by("-created_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog"] = self.blog
        context["full_list"] = BlogPost.objects.filter(blog=self.blog).order_by(
            "-created_date"
        )
        return context

    def get_admin_links(self):
        return [
            {
                "name": "Bloggadmin",
                "glyphicon_symbol": "cog",
                "url": reverse("admin:blog_blog_change", args=[self.blog.id]),
            },
        ]


class BlogListView(ListView):
    """
    List all blogs on the site.
    """

    model = Blog
    template_name = "blog/blog_list.html"
    context_object_name = "blog_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_list"] = BlogPost.objects.order_by("-created_date")[:5]
        return context

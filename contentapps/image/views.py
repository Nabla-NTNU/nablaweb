"""
Views for image app
"""
from django.shortcuts import render


def view_markdown(request):
    """
    View for testing the custom markdown filter

    It is not meant for production, just for testing and debugging the markdown filter.
    """
    return render(
        request,
        "content/images/markdown_test.html",
        {"markdown_text": request.POST.get("markdown_text", "")})

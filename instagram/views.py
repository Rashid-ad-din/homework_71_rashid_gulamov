from django.shortcuts import render
from django.views.generic import TemplateView

from accounts.forms import SearchForm
from posts.models import Post


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        kwargs['search_form'] = SearchForm()
        kwargs['posts'] = Post.objects.all().order_by('-created_at')
        return kwargs

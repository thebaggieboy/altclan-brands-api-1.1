from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from .models import *
from .serializers import *




@method_decorator(cache_page(600), name='list')      # 10 min cache
@method_decorator(cache_page(600), name='retrieve')
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


@method_decorator(cache_page(600), name='list')      # 10 min cache
@method_decorator(cache_page(600), name='retrieve')
class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.order_by('-date_created')
    serializer_class = ArticlesSerializer
    lookup_field = 'slug'

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            # Keep existing ID links working while the site moves to slug URLs.
            return get_object_or_404(self.queryset, pk=self.kwargs[self.lookup_url_kwarg])





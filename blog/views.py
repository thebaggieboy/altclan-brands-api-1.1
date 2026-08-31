from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import *
from .serializers import *




class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


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





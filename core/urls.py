from django.contrib import admin
from django.urls import path, include
from .routers import router


urlpatterns = [
    # path('', IndexView.as_view(), name='index'),
    path('', include(router.urls)),

]



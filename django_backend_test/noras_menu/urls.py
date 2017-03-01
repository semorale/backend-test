# -*- encoding: utf-8 -*-
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from .views import CreateMenu,ListMenu,UpdateMenu,CreateSelection,ListSelection,CreateSubscriber

urlpatterns = [
    url(r'^menu/new$',CreateMenu.as_view(),name='Create Menu'),
    url(r'^menu/edit/(?P<pk>\d+)/$',UpdateMenu.as_view(),name='Update Menu'),
    url(r'^menu/list$',ListMenu.as_view(),name='List Menu'),
    url(r'^menu/selection$',ListSelection.as_view(),name='List Selection'),
    url(r'^menu/(?P<uuid>[0-9a-z-]+)$',CreateSelection.as_view(),name='Create Selection'),
    url(r'^subscriber/new$',CreateSubscriber.as_view(),name='Create Subscriber'),
    
]
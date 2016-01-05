from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^theme/(?P<theme_id>[0-9]+)/$', views.theme_page),
]

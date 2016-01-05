from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home$', views.home_page, name='homepage'),
    url(r'^theme/(?P<theme_id>[0-9]+)/$', views.theme_page),
    url(r'^profile/(?P<user_id>[0-9]+)/$', views.profile_page)
]

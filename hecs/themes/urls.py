from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home$', views.home_page, name='homepage'),
    url(r'^signup$', views.signup_page, name='signup'),
    url(r'^login$', views.login_page, name='login'),
    url(r'^theme/(?P<theme_id>[0-9]+)/$', views.theme_page),
]
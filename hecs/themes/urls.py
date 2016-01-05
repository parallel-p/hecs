from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='homepage'),
    url(r'^signup$', views.signup_page, name='signup'),
    url(r'^login$', views.login_page, name='login'),
    url(r'^logout$', views.logout_page, name='logout'),
    url(r'^theme/(?P<theme_id>[0-9]+)/$', views.theme_page),
    url(r'^profile/(?P<user_id>[0-9]+)/$', views.profile_page)
]

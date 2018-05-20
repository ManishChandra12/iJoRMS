from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'search/$', views.search, name='search'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^vitae/(?P<update>[0-1])/$', views.vitae, name='vitae'),
    url(r'^stats/$', views.stats, name='stats'),
    url(r'details/(?P<id>[0-9]+)$', views.details, name='details'),
    url(r'^add/$', views.add, name='add'),
    url(r'^jhos/$', views.populateResumetoDb, name='populateResumetoDb'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    # url(r'^update_profile/$', views.update_profile, name='update_profile'),
]
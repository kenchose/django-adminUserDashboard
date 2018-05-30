from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'signin$', views.signin),
    url(r'^registration$', views.registration),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^dashboard/admin$', views.admindash),
    url(r'^users/show/(?P<user_id>\d+)$', views.userProfile),
    url(r'^messageto/(?P<user_id>\d+)$', views.messageFor),
    url(r'^commentto/(?P<user_id>\d+)/(?P<msg_id>\d+)$', views.commentTo),
    url(r'^edit/(?P<user_id>\d+)$', views.userEdit),
    url(r'^editinfo/(?P<user_id>\d+)$', views.userEditInfo),
    # url(r'^commentto/(?P<user_id>\d+)$', views.commentTo),
    # url(r'users/edit/(?P<user_id>)$', views.user_edit),
    url(r'^logout$', views.logout),
]
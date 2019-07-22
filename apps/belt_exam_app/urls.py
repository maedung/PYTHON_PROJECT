from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^jobs/new$', views.new_job),
    url(r'^create_job$', views.create_job),
    url(r'^job_delete/(?P<id>\d+)$', views.job_delete),
    url(r'^job/(?P<id>\d+)$', views.job_info),
    url(r'^edit/(?P<id>\d+)$', views.edit_job),
    url(r'^edit_process$', views.edit_process),
    url(r'^job_add_to_user/(?P<id>\d+)$', views.job_add_to_user),
    url(r'^job_del_from_user/(?P<id>\d+)$', views.job_delete_from_user),
]
from django.conf.urls import url
from asynctask import views

urlpatterns = [

    url(r'^task$', views.AsyncTaskView.as_view(), name='task'),
]
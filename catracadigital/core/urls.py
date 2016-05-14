from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^employee/$', views.employee_create, name='employee-create'),
    url(r'^employee/delete/(?P<pk>.+)', views.employee_delete, name='employee-delete'),
    url(r'^employee/report/(?P<pk>.+)', views.generate_report, name='employee-report'),
    url(r'^employee/register/(?P<pk>.+)', views.employee_register, name='employee-register'),
    url(r'^employee/(?P<pk>.+)$', views.employee_detail, name='employee-detail'),
    url(r'^register/(?P<pk>.*)', views.register_detail, name='register-detail'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]
from django.conf.urls import url

from . import views

app_name = 'slas'

urlpatterns = [
    url(r'^$', views.index, name='slas'),
    url(r'^inscription/(?P<activity_id>[0-9]+)$', views.inscription, name='inscription'),
    url(r'^add_student/(?P<activity_id>[0-9]+)$', views.add_student, name='add_student'),
    url(r'^check_student/(?P<activity_id>[0-9]+)/(?P<surname>.+?)/(?P<first_name>.+?)$', views.check_student,
        name='check_student'),
    url(r'^payed/(?P<activity_id>[0-9]+)/(?P<payed>[0-9]+)$', views.payed, name='payed'),
    url(r'^payed$', views.payed, name='payed_clean'),
    url(r'^answered/(?P<activity_id>[0-9]+)/(?P<answered>[0-9]+)$', views.answered, name='answered'),
    url(r'^answered', views.payed, name='answered_clean'),
    url(r'^list', views.list_inscriptions, name='list'),
    url(r'^data', views.get_excel_data, name='data'),

]


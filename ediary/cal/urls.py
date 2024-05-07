from django.urls import path
from . import views

urlpatterns = [
    path('calendar', views.CalendarView.as_view(), name='calendar'),
    path('event', views.event, name='event_new'),
    path('event_edit/(?P<event_id>\d+)/$', views.editevent, name='event_edit'),
    path('diaryview', views.diaryview, name='diaryview'),
    path('adddiary', views.adddiary, name='adddiary'),
    path('view/<int:id>/', views.view, name='view'),
    path('view/<int:id>/editdiary/', views.editdiary, name='editdiary'),
    
]
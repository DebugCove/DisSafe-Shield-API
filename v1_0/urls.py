from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('status/', views.status_view, name ='status'),
    path('make_report/', views.make_report_view, name='make_report'),
]

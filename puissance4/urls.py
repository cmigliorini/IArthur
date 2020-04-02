from django.conf.urls import url

from . import views

urlpatterns = [
    url('ajax/play/', views.play, name='play'),
    url('ajax/reset/', views.reset, name='reset'),
    url('ajax/refresh/', views.refresh, name='refresh'),
    url('ajax/waitForComputer/', views.computer_play, name='computer_play'),
    url('ajax/setIA/', views.chooseIA, name='chooseIA'),
    url('admin/', views.admin, name='admin'),
    url('spectate/', views.spectate, name='spectate'),
    url('', views.index, name='index'),
]
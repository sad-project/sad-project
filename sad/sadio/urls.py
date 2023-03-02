from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('libraries', views.libraries, name='libraries'),
    path('library/<str:library_name>', views.library, name='library'),
]

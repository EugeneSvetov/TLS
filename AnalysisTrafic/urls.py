from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('download_file/', download_file, name='download_file'),
    path('dashboard/', dashboard, name='dashboard')

]


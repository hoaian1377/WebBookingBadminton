from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('badminton_court_booking/',views.badminton_court_booking,name='badminton_court_booking')
    
]
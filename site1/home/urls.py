from django.contrib import admin
from django.urls import path
from home import views as home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home.get_home,name='home')
]
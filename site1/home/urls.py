from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('badminton_court_booking/',views.badminton_court_booking,name='badminton_court_booking'),
    path('login/',views.login,name='login'),
    path('court_history/',views.court_history,name='court_history'),
    path('badminton_court_booking/court_booking1/',views.court_booking1,name='court_booking1'),
    path('login/register/',views.register,name='register')
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
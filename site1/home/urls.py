from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('badminton_court_booking/', views.badminton_court_booking, name='badminton_court_booking'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/profile1/', views.profile1, name='profile1'),
    path('court_history/', views.court_history, name='court_history'),
    path('badminton_court_booking/court_booking1/', views.court_booking1, name='court_booking1'),
    path('login/register/', views.register, name='register'),
    path('login/forgot_password/', views.forgot_password, name='forgot_password'),  # Thêm dấu "/" ở cuối để nhất quán
    path('support/', views.support, name='support'),
    path('shop/', views.shop, name='shop'),
    path('shop/item_detail/<int:pk>/', views.item_detail, name='item_detail'),
    path('shop/cart_detail/', views.cart_detail, name='cart_detail'),
    path('shop/add_to_cart/', views.add_to_cart, name='add_to_cart'),  # Thêm đường dẫn này
]

# Static files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

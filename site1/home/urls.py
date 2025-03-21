from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import update_cart
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('badminton_court_booking/', views.badminton_court_booking, name='badminton_court_booking'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/profile1/', views.profile1, name='profile1'),
    path('court_history/', views.court_history, name='court_history'),
    path('badminton_court_booking/court_booking1/<int:sanid>/', views.court_booking1, name='court_booking1'),
    path('login/register/', views.register, name='register'),
    path('login/forgot_password/', views.forgot_password, name='forgot_password'),
    path('support/', views.support, name='support'),
    path('shop/', views.shop, name='shop'),
    path('shop/item_detail/<int:pk>/', views.item_detail, name='item_detail'),
    path('shop/cart_detail/', views.cart_detail, name='cart_detail'),
    path('shop/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('shop/remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  # Thêm đường dẫn xóa sản phẩm
    path('shop/checkout/', views.checkout, name='checkout'),  # Thêm đường dẫn thanh toán
    path('shop/remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('shop/checkout/', views.checkout, name='checkout'),  # Đường dẫn thanh toán
    path('shop/remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:product_id>/', update_cart, name='update_cart'),
    path('hoadon/<str:hoadonid>/', views.hoadon_detail, name='hoadon_detail'),
    path("checkout/", views.checkout, name="checkout"),
    path("shop/checkout/", views.checkout, name="checkout"),\
    path('court_history/xoa_dat_san/<int:id>/', views.xoa_dat_san, name='xoa_dat_san'),
    path('huy-hoadon/<int:hoadon_id>/', views.huy_hoadon, name='huy_hoadon'),
    path('add_review/<int:sanpham_id>/', views.add_review, name='add_review'),
    path('payment/<int:datsanid>/', views.payment, name='payment'),  # Trang thanh toán
    path("generate_qr/<int:datsanid>/", views.generate_qr, name="generate_qr"),  # Thêm URL này


]


# Static files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
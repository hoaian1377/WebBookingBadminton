from django.contrib import admin
from .models import San,Sanpham,Taikhoan,Khachhang,Hoadon,Chitiethoadon,Datsan
# Register your models here.
admin.site.register(Sanpham)
admin.site.register(San)
admin.site.register(Taikhoan)
admin.site.register(Datsan)
admin.site.register(Hoadon)
admin.site.register(Chitiethoadon)
admin.site.register(Khachhang)
from django.contrib import admin
from .models import San,Sanpham,Taikhoan,Khachhang,Hoadon,Chitiethoadon,Datsan
# Register your models here.



class KhachhangAdmin(admin.ModelAdmin):
    list_display = ('khachhangid', 'hoten', 'email', 'sdt', 'diachi')
    
class HoadonAdmin(admin.ModelAdmin):
    list_display = ('hoadonid', 'khachhangid', 'total', 'phuongthucthanhtoan', 'thoigian', 'trangthai')

class SanAdmin(admin.ModelAdmin):
    list_display = ('sanid', 'tensan', 'giathue', 'soluongsan', 'diachi')

class SanphamAdmin(admin.ModelAdmin):
    list_display = ('sanphamid', 'tensp', 'giatien', 'soluong', 'trangthai')


class DatsanAdmin(admin.ModelAdmin):
    list_display = ('datsanid', 'khachhangid', 'sanid', 'thoigianbatdau', 'thoigianketthuc', 'trangthai', 'tongtien')

class ChitiethoadonAdmin(admin.ModelAdmin):
    list_display = ('chitiethoadonid', 'hoadonid', 'sanphamid', 'soluong', 'giatien')


class TaikhoanAdmin(admin.ModelAdmin):
    list_display = ('taikhoanid', 'username', 'roleid')

admin.site.register(Sanpham,SanphamAdmin)
admin.site.register(San,SanAdmin)
admin.site.register(Taikhoan,TaikhoanAdmin)
admin.site.register(Datsan,DatsanAdmin)
admin.site.register(Hoadon,HoadonAdmin)
admin.site.register(Chitiethoadon,ChitiethoadonAdmin)
admin.site.register(Khachhang,KhachhangAdmin)
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.timezone import now  

class Chitiethoadon(models.Model):
    chitiethoadonid = models.AutoField(db_column='ChiTietHoaDonID', primary_key=True)  # Field name made lowercase.
    hoadonid = models.ForeignKey('Hoadon', models.DO_NOTHING, db_column='HoaDonID')  # Field name made lowercase.
    sanphamid = models.ForeignKey('Sanpham', models.DO_NOTHING, db_column='SanPhamID')  # Field name made lowercase.
    soluong = models.IntegerField(db_column='SoLuong')  # Field name made lowercase.
    giatien = models.DecimalField(db_column='GiaTien', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ChiTietHoaDon'


class Datsan(models.Model):
    datsanid = models.AutoField(db_column='DatSanID', primary_key=True)  # Field name made lowercase.
    thoigianbatdau = models.TimeField(db_column='ThoiGianBatDau', blank=True, null=True)  # Field name made lowercase.
    thoigianketthuc = models.TimeField(db_column='ThoiGianKetThuc', blank=True, null=True)  # Field name made lowercase.
    trangthai = models.CharField(db_column='TrangThai', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sanid = models.ForeignKey('San', models.DO_NOTHING, db_column='SanID', blank=True, null=True)  # Field name made lowercase.
    khachhangid = models.ForeignKey('Khachhang', models.DO_NOTHING, db_column='KhachHangID', blank=True, null=True)  # Field name made lowercase.
    tongtien = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Đảm bảo có dòng này
    thoigiandat = models.DateTimeField(db_column='ThoiGianDat', blank=True, null=True)  # Thêm dòng này
    class Meta:
        managed = False
        db_table = 'DatSan'
        

class Hoadon(models.Model):
    hoadonid = models.IntegerField(db_column='HoaDonID', primary_key=True)  # Field name made lowercase.
    khachhangid = models.ForeignKey('Khachhang', models.DO_NOTHING, db_column='KhachHangID')  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=10, decimal_places=2)  # Field name made lowercase.
    phuongthucthanhtoan = models.CharField(db_column='PhuongThucThanhToan', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    thoigian = models.DateTimeField(db_column='ThoiGian', blank=True, null=True,default=now)  # Field name made lowercase.
    trangthai = models.CharField(db_column='TrangThai', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HoaDon'


class Khachhang(models.Model):
    khachhangid = models.IntegerField(db_column='KhachHangID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    hoten = models.CharField(db_column='HoTen', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sdt = models.IntegerField(db_column='SDT', blank=True, null=True)  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KhachHang'


class Role(models.Model):
    roleid = models.IntegerField(db_column='RoleID', primary_key=True)  # Field name made lowercase.
    rolename = models.CharField(db_column='RoleName', unique=True, max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Role'


class San(models.Model):
    sanid = models.IntegerField(db_column='SanID', primary_key=True)  # Field name made lowercase.
    tensan = models.CharField(db_column='TenSan', unique=True, max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    giathue = models.FloatField(db_column='GiaThue')  # Field name made lowercase.
    soluongsan = models.FloatField(db_column='SoLuongSan')  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    imageurl = models.CharField(db_column='ImageUrl', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'San'


class Sanpham(models.Model):
    sanphamid = models.IntegerField(db_column='SanPhamID', primary_key=True)  # Field name made lowercase.
    tensp = models.CharField(db_column='TenSP', unique=True, max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    giatien = models.FloatField(db_column='GiaTien')  # Field name made lowercase.
    soluong = models.FloatField(db_column='SoLuong')  # Field name made lowercase.
    thoigiannhaphang = models.DateTimeField(db_column='ThoiGianNhapHang', blank=True, null=True)  # Field name made lowercase.
    trangthai = models.CharField(db_column='TrangThai', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    imageurl = models.CharField(db_column='ImageUrl', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SanPham'


class Taikhoan(models.Model):
    taikhoanid = models.OneToOneField(Khachhang, models.DO_NOTHING, db_column='TaiKhoanID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', unique=True, max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    password = models.CharField(db_column='PassWord', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    roleid = models.ForeignKey(Role, models.DO_NOTHING, db_column='RoleID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TaiKhoan'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    first_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    email = models.CharField(max_length=254, db_collation='SQL_Latin1_General_CP1_CI_AS')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    model = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')
    session_data = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
class CartItem(models.Model):
    product = models.ForeignKey('Sanpham', on_delete=models.CASCADE)  # Liên kết đến sản phẩm
    quantity = models.IntegerField(default=1)  # Số lượng sản phẩm
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  # Tổng tiền cho mặt hàng này

    class Meta:
        db_table = 'cart_item'  # Tên bảng trong cơ sở dữ liệu
        
        
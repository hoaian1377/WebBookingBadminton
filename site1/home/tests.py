from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from .models import Khachhang, Taikhoan, Hoadon, Sanpham, Chitiethoadon, Datsan, San
import datetime

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Tạo khách hàng
        self.khachhang = Khachhang.objects.create(khachhangid=1, email='test@example.com')
        
        # Tạo tài khoản
        self.taikhoan = Taikhoan.objects.create(
            taikhoanid=self.khachhang, username='testuser', password=make_password('testpassword')
        )

        # Tạo sản phẩm
        self.sanpham = Sanpham.objects.create(sanphamid=1, tensp='Vợt Yonex', giatien=100000, soluong=10, trangthai='còn hàng')

        # Tạo sân
        self.san = San.objects.create(sanid=2, tensan='Sân As', soluongsan=5, giathue=50000)

        # Tạo đặt sân
        Datsan.objects.all().delete()
        self.datsan = Datsan.objects.create(
            sanid=self.san, khachhangid=self.khachhang, thoigianbatdau='10:00',
            thoigianketthuc='12:00', thoigiandat=datetime.date.today(), trangthai='Chưa thanh toán'
        )
        
        # Tạo hóa đơn hợp lệ
        self.hoadon = Hoadon.objects.create(
            hoadonid=1, khachhangid=self.khachhang, total=200000, phuongthucthanhtoan='Tiền mặt',
            thoigian=now(), trangthai='Chờ xác nhận', description='Test đơn hàng'
        )
        
        # Lưu thông tin đăng nhập vào session
        session = self.client.session
        session['taikhoanid'] = self.taikhoan.pk  # Sử dụng pk để tránh lỗi
        session.save()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_shop_view(self):
        response = self.client.get(reverse('shop'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop.html')

    def test_item_detail_view(self):
        response = self.client.get(reverse('item_detail', args=[self.sanpham.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'item_detail.html')

    def test_cart_detail_view(self):
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart_detail.html')

    def test_add_to_cart(self):
        response = self.client.post(reverse('add_to_cart'), {'sanpham_id': self.sanpham.pk, 'quantity': 2})
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(self.sanpham.pk), self.client.session.get('cart', {}))

    def test_remove_from_cart(self):
        session = self.client.session
        session['cart'] = {str(self.sanpham.pk): 1}
        session.save()
        
        response = self.client.post(reverse('remove_from_cart', args=[self.sanpham.pk]))
        self.assertNotIn(str(self.sanpham.pk), self.client.session.get('cart', {}))

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser', 'email': 'newuser@example.com', 'password': 'Test@1234', 'confirm_password': 'Test@1234'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Taikhoan.objects.filter(username='newuser').exists())

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        }, follow=True)  # Bật follow=True để test theo dõi redirect

        self.assertRedirects(response, reverse('home'))  # Kiểm tra redirect về home


    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('logout'))  # Đổi từ logout_view thành logout
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_court_booking_success(self):
        response = self.client.post(reverse('court_booking1', args=[self.san.pk]), {
            'date': datetime.date.today().strftime('%Y-%m-%d'), 'thoigianbatdau': '10:00', 'duration': '2'
        })
        self.assertEqual(Datsan.objects.count(), 2)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Đặt sân thành công!' in str(m) for m in messages))

    def test_cancel_hoadon(self):
        response = self.client.post(reverse('huy_hoadon', args=[self.hoadon.pk]))
        self.hoadon.refresh_from_db()
        self.assertEqual(self.hoadon.trangthai, 'Đã hủy')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Hủy hóa đơn thành công' in str(m) for m in messages))

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .models import Sanpham, San, Taikhoan,Khachhang,Chitiethoadon,Hoadon
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from django.shortcuts import redirect
from .models import CartItem
from decimal import Decimal
import random

def shop(request):
    sanpham_list = Sanpham.objects.filter(trangthai='còn hàng')
    search_query = request.GET.get('search', '').strip()
    price_filter = request.GET.get('price', '')

    if search_query:
        sanpham_list = sanpham_list.filter(tensp__icontains=search_query)

    if price_filter == 'low':
        sanpham_list = sanpham_list.order_by('giatien')
    elif price_filter == 'high':
        sanpham_list = sanpham_list.order_by('-giatien')

    paginator = Paginator(sanpham_list, 24)
    page_number = request.GET.get('page', 1)
    sanpham_page = paginator.get_page(page_number)

    cart = request.session.get('cart', {})
    return render(request, 'shop.html', {'sanpham': sanpham_page, 'cart': cart})

def item_detail(request, pk):
    sanpham = get_object_or_404(Sanpham, pk=pk)
    return render(request, 'item_detail.html', {'sanpham': sanpham})

def cart_detail(request):
    cart = request.session.get('cart', {})
    sanpham_list = []
    total_price = 0
    total_items = 0

    for sanphamid, quantity in cart.items():
        try:
            sanphamid = int(sanphamid)
            product = get_object_or_404(Sanpham, pk=sanphamid)
            subtotal = product.giatien * quantity
            sanpham_list.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
            total_price += subtotal
            total_items += quantity
        except (ValueError, TypeError):
            continue

    shipping_cost = 20000
    total_payment = total_price + shipping_cost

    return render(request, 'cart_detail.html', {
        'cart_items': sanpham_list,
        'total_price': total_price,
        'total_items': total_items,
        'shipping_cost': shipping_cost,
        'total_payment': total_payment
    })

def add_to_cart(request):
    if request.method == 'POST':
        sanphamid = request.POST.get('sanpham_id')
        try:
            sanphamid = int(sanphamid)
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                messages.error(request, 'Số lượng phải lớn hơn 0.')
                return redirect('shop')

            cart = request.session.get('cart', {})
            if sanphamid in cart:
                cart[sanphamid] += quantity
            else:
                cart[sanphamid] = quantity

            request.session['cart'] = cart
            messages.success(request, 'Sản phẩm đã được thêm vào giỏ hàng.')
            return redirect('cart_detail')
        except (ValueError, TypeError):
            messages.error(request, 'Dữ liệu không hợp lệ hoặc sản phẩm không tồn tại.')
            return redirect('shop')

    return redirect('shop')
def generate_unique_id():
    # Lấy ID lớn nhất hiện có trong bảng KhachHang
    last_id = Khachhang.objects.aggregate(max_id=models.Max('khachhangid'))['max_id']
    if last_id is None:
        return 1  # Nếu bảng trống, bắt đầu từ 1
    return last_id + 1  # ID tiếp theo


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')  # Lấy email từ form
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Kiểm tra mật khẩu
        if password != confirm_password:
            messages.error(request, 'Mật khẩu không khớp.')
            return render(request, 'register.html')

        # Kiểm tra tên đăng nhập đã tồn tại
        if Taikhoan.objects.filter(username=username).exists():
            messages.error(request, 'Tên đăng nhập đã tồn tại.')
            return render(request, 'register.html')

        # Kiểm tra email đã tồn tại
        if Khachhang.objects.filter(email=email).exists():
            messages.error(request, 'Email đã được sử dụng.')
            return render(request, 'register.html')

        # Tạo khách hàng mới
        khachhang = Khachhang.objects.create(
            khachhangid=generate_unique_id(),  # Hàm tự tạo ID duy nhất
            email=email  # Gán email từ form
        )

        # Tạo tài khoản mới liên kết với khách hàng
        hashed_password = make_password(password)
        Taikhoan.objects.create(
            taikhoanid=khachhang,  # Sử dụng đối tượng Khachhang
            username=username,
            password=hashed_password
        )

        messages.success(request, 'Đăng ký thành công!')
        return redirect('login')

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        # Đảm bảo giá trị không phải None, thay bằng chuỗi rỗng nếu thiếu
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Kiểm tra nếu trường bị bỏ trống
        if not username or not password:
            messages.error(request, 'Vui lòng nhập đầy đủ thông tin.')
            return render(request, 'login.html')

        try:
            # Tìm người dùng theo tên đăng nhập
            user = Taikhoan.objects.get(username=username)

            # Kiểm tra mật khẩu
            if check_password(password, user.password):
                # Lưu thông tin vào session
                request.session['taikhoanid'] = user.taikhoanid_id  # Lấy ID nếu là khóa ngoại
                request.session['username'] = user.username
                return redirect('home')
            else:
                messages.error(request, 'Sai mật khẩu.')

        except Taikhoan.DoesNotExist:
            messages.error(request, 'Tên đăng nhập không tồn tại.')

    return render(request, 'login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Bạn đã đăng xuất thành công.')
    return redirect('/')

def badminton_court_booking(request):
    DanhSachSan = San.objects.all()
    address_filter = request.GET.get('address', '').strip()
    price_filter = request.GET.get('price', '')
    name_filter = request.GET.get('search', '').strip()

    if address_filter:
        DanhSachSan = DanhSachSan.filter(diachi__icontains=address_filter)
    if price_filter:
        if price_filter == 'cheap':
            DanhSachSan = DanhSachSan.filter(giathue__lt=100000)
        elif price_filter == 'medium':
            DanhSachSan = DanhSachSan.filter(giathue__gte=100000, giathue__lt=500000)
        elif price_filter == 'vip':
            DanhSachSan = DanhSachSan.filter(giathue__gte=500000)
    if name_filter:
        DanhSachSan = DanhSachSan.filter(tensan__icontains=name_filter)

    paginator = Paginator(DanhSachSan, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'badminton_court_booking.html', {'page_obj': page_obj})

def home(request):
    return render(request, 'home.html')

def forgot_password(request):
    return render(request, 'forgot_password.html')

def support(request):
    return HttpResponseRedirect("https://docs.google.com/forms/d/e/1FAIpQLSdsZGwFck63-cPDZcW8gZyyMAhf2UyYaOINuByEgwbMvtTm3A/viewform")

def profile1(request):
    taikhoan_id = request.session.get('taikhoanid')

    if not taikhoan_id:
        messages.error(request, "Bạn cần đăng nhập để cập nhật thông tin.")
        return redirect('login')

    khachhang = Khachhang.objects.get(khachhangid=taikhoan_id)

    if request.method == 'POST':
        hoten = request.POST.get('name')
        sdt = request.POST.get('phone')
        diachi=request.POST.get('diachi')
        khachhang.hoten = hoten
        khachhang.sdt = sdt
        khachhang.diachi=diachi
        khachhang.save()  

        messages.success(request, "Cập nhật thông tin thành công!")
        return redirect('profile')

    return render(request, 'profile1.html', {'khachhang': khachhang})

def profile(request):
    taikhoan_id=request.session.get('taikhoanid')
    if taikhoan_id:
        try:
            taikhoan=Taikhoan.objects.get(taikhoanid=taikhoan_id)
            khachhang=taikhoan.taikhoanid
        except Taikhoan.DoesNotExist:
            khachhang = None
    else :
        khachhang = None     
    return render(request, 'profile.html',{'khachhang':khachhang})

def court_history(request):
    return render(request, 'court_history.html')

def court_booking1(request):
    return render(request, 'court_booking1.html')

def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if product_id in cart:
            if quantity > 0:
                cart[product_id] = quantity
            else:
                del cart[product_id]
        request.session['cart'] = cart
        messages.success(request, 'Giỏ hàng đã được cập nhật.')
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        messages.success(request, 'Sản phẩm đã được xóa khỏi giỏ hàng.')
    request.session['cart'] = cart
    return redirect('cart_detail')

def checkout(request):
    cart = request.session.get('cart', {})  # Lấy giỏ hàng từ session
    if not cart:  # Kiểm tra nếu giỏ hàng rỗng
        return render(request, 'checkout.html', {'message': 'Giỏ hàng trống!'})

    user = request.user
    try:
        khachhang = Khachhang.objects.get(email=user.email)  # Lấy thông tin khách hàng
    except Khachhang.DoesNotExist:
        messages.error(request, "Không tìm thấy khách hàng.")
        return redirect('cart_detail')

    cart_items = []
    total_price = 0

    for sanphamid, quantity in cart.items():
        try:
            product = Sanpham.objects.get(pk=sanphamid)
            subtotal = product.giatien * quantity
            cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
            total_price += subtotal
        except Sanpham.DoesNotExist:
            continue  # Bỏ qua sản phẩm không tồn tại

    shipping_cost = 20000  # Phí vận chuyển cố định
    total_payment = total_price + shipping_cost  # Tổng tiền

    if request.method == "POST":
        phuong_thuc = request.POST.get("phuong_thuc")

        # Tạo hóa đơn mới
        hoadon = Hoadon.objects.create(
            khachhangid=khachhang,
            total=Decimal(total_payment),
            phuongthucthanhtoan=phuong_thuc,
            trangthai="Chờ xác nhận"
        )

        # Lưu từng sản phẩm vào ChiTietHoaDon
        for item in cart_items:
            Chitiethoadon.objects.create(
                hoadonid=hoadon,
                sanphamid=item['product'],
                soluong=item['quantity'],
                giatien=item['product'].giatien,
                tongtien=item['subtotal']
            )
            # Cập nhật số lượng sản phẩm trong kho
            product = item['product']
            product.soluong -= item['quantity']
            product.save()

        # Xóa giỏ hàng trong session sau khi thanh toán
        request.session['cart'] = {}

        return redirect("payment_success")  # Chuyển hướng đến trang thành công

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "shipping_cost": shipping_cost,
        "total_payment": total_payment
    })
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]  # Xóa sản phẩm khỏi giỏ hàng
        messages.success(request, 'Sản phẩm đã được xóa khỏi giỏ hàng.')
    request.session['cart'] = cart
    return redirect('cart_detail')  # Điều hướng lại đến trang giỏ hàng
from django.shortcuts import redirect
from .models import CartItem

def update_cart(request, product_id):
    if request.method == "POST":
        action = request.POST.get('action')
        quantity = request.POST.get('quantity')

        # Logic để cập nhật giỏ hàng
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            if action == "increase":
                cart[str(product_id)] += 1
            elif action == "decrease" and cart[str(product_id)] > 1:
                cart[str(product_id)] -= 1
            elif action == "remove":  # Thêm logic để xóa sản phẩm
                del cart[str(product_id)]

        request.session['cart'] = cart
        messages.success(request, 'Giỏ hàng đã được cập nhật.')
    return redirect('cart_detail')  # Hoặc đường dẫn phù hợp đến trang giỏ hàng
def update_cart(request, product_id):
    if request.method == "POST":
        action = request.POST.get('action')
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            if action == "increase":
                cart[str(product_id)] += 1
            elif action == "decrease" and cart[str(product_id)] > 1:
                cart[str(product_id)] -= 1
            elif action == "remove":
                del cart[str(product_id)]

        request.session['cart'] = cart
        messages.success(request, 'Giỏ hàng đã được cập nhật.')
    return redirect('cart_detail')
def cart_detail(request):
    cart = request.session.get('cart', {})
    sanpham_list = []
    total_price = 0
    total_items = 0

    for sanphamid, quantity in cart.items():
        try:
            sanphamid = int(sanphamid)
            product = get_object_or_404(Sanpham, pk=sanphamid)
            subtotal = product.giatien * quantity
            sanpham_list.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
            total_price += subtotal
            total_items += quantity
        except (ValueError, TypeError):
            continue

    shipping_cost = 20000
    total_payment = total_price + shipping_cost

    return render(request, 'cart_detail.html', {
        'cart_items': sanpham_list,
        'total_price': total_price,
        'total_items': total_items,
        'shipping_cost': shipping_cost,
        'total_payment': total_payment
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.http import HttpResponseRedirect,HttpResponse
from .models import Sanpham, San, Taikhoan,Khachhang,Chitiethoadon,Hoadon,Datsan
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.shortcuts import redirect
from .models import CartItem
from django.db import transaction
from decimal import Decimal
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.http import JsonResponse
from django.shortcuts import render

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
    het_hang = sanpham.soluong <= 0  # Kiểm tra nếu hết hàng
    return render(request, 'item_detail.html', {'sanpham': sanpham, 'het_hang': het_hang})

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
        next_url = request.POST.get('next', 'shop')  # Lấy URL tiếp theo hoặc quay về 'shop'
        
        try:
            sanphamid = int(sanphamid)
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                messages.error(request, 'Số lượng phải lớn hơn 0.')
                return redirect(next_url)

            cart = request.session.get('cart', {})
            if sanphamid in cart:
                cart[sanphamid] += quantity
            else:
                cart[sanphamid] = quantity

            request.session['cart'] = cart
            messages.success(request, 'Sản phẩm đã được thêm vào giỏ hàng.')
            return redirect(next_url)  # Trả về trang trước
        except (ValueError, TypeError):
            messages.error(request, 'Dữ liệu không hợp lệ hoặc sản phẩm không tồn tại.')
            return redirect(next_url)

    return redirect('shop')


def generate_unique_id():
    # Lấy ID lớn nhất hiện có trong bảng KhachHang
    last_id = Khachhang.objects.aggregate(max_id=models.Max('khachhangid'))['max_id']
    if last_id is None:
        return 1  # Nếu bảng trống, bắt đầu từ 1
    return last_id + 1  # ID tiếp theo

def Datsan_id():
    # Lấy ID lớn nhất hiện có trong bảng KhachHang
    last_id = Datsan.objects.aggregate(max_id=models.Max('datsanid'))['max_id']
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
    taikhoan_id = request.session.get('taikhoanid')
    khachhang = None
    hoadons = None

    if taikhoan_id:
        try:
            # Lấy khách hàng kèm danh sách hóa đơn (tối ưu cho nhiều hóa đơn)
            khachhang = Khachhang.objects.prefetch_related('hoadon_set').get(taikhoan__taikhoanid=taikhoan_id)

            # Lấy danh sách hóa đơn từ quan hệ `hoadon_set`
            hoadons = khachhang.hoadon_set.all().order_by('-thoigian')

        except Khachhang.DoesNotExist:
            khachhang = None
            hoadons = None

    return render(request, 'profile.html', {'khachhang': khachhang, 'hoadons': hoadons})
def generate_Hoadon_id():
    # Lấy ID lớn nhất hiện có trong bảng KhachHang
    last_id = Hoadon.objects.aggregate(max_id=models.Max('hoadonid'))['max_id']
    if last_id is None:
        return 1  # Nếu bảng trống, bắt đầu từ 1
    return last_id + 1  # ID tiếp theo




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
        else:
            # Nếu sản phẩm chưa có trong giỏ hàng, thêm mới
            cart[str(product_id)] = 1

        request.session['cart'] = cart
        messages.success(request, 'Giỏ hàng đã được cập nhật.')

        # Phản hồi JSON cho AJAX nếu có
        if request.is_ajax():
            return JsonResponse({'status': 'success', 'cart_total': sum(cart.values())})

    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        messages.success(request, 'Sản phẩm đã được xóa khỏi giỏ hàng.')
    request.session['cart'] = cart
    return redirect('cart_detail')

def checkout(request):
    cart = request.session.get('cart', {})  # Lấy giỏ hàng từ session
    if not cart:
        messages.error(request, "Giỏ hàng trống! Vui lòng thêm sản phẩm trước khi thanh toán.")
        return redirect('cart_detail')

    taikhoan_id = request.session.get('taikhoanid')  # Lấy ID tài khoản từ session
    if not taikhoan_id:
        messages.error(request, "Bạn chưa đăng nhập! Vui lòng đăng nhập để thanh toán.")
        return redirect('login')

    # Kiểm tra khách hàng từ tài khoản ID
    try:
        taikhoan = Taikhoan.objects.get(taikhoanid=taikhoan_id)
        khachhang = Khachhang.objects.get(taikhoan=taikhoan)
        if not khachhang.diachi or not khachhang.sdt:
            messages.error(request, "Vui lòng cập nhật địa chỉ và số điện thoại trước khi thanh toán.")
            return redirect('profile')

    except (Taikhoan.DoesNotExist, Khachhang.DoesNotExist):
        messages.error(request, "Không tìm thấy thông tin khách hàng. Vui lòng cập nhật tài khoản.")
        return redirect('profile')
    except (Taikhoan.DoesNotExist, Khachhang.DoesNotExist):
        messages.error(request, "Không tìm thấy thông tin khách hàng. Vui lòng cập nhật tài khoản.")
        return redirect('profile')

    cart_items = []
    total_price = Decimal(0)

    # Lấy thông tin sản phẩm từ giỏ hàng
    for sanphamid, quantity in cart.items():
        try:
            product = Sanpham.objects.get(pk=sanphamid)
            subtotal = Decimal(str(product.giatien)) * Decimal(quantity)  # Fix lỗi Decimal
            cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal   })
            total_price += subtotal
        except Sanpham.DoesNotExist:
            continue  # Bỏ qua sản phẩm không tồn tại

    shipping_cost = Decimal(20000)  # Phí vận chuyển cố định
    total_payment = total_price + shipping_cost  # Tổng tiền

    if request.method == "POST":
        phuong_thuc = request.POST.get("phuong_thuc")
        if not phuong_thuc:
            messages.error(request, "Vui lòng chọn phương thức thanh toán.")
            return redirect("checkout")

        try:
            with transaction.atomic():
                hoadon = Hoadon.objects.create(
                    hoadonid=generate_Hoadon_id(),
                    khachhangid=khachhang,
                    total=total_payment,
                    phuongthucthanhtoan=phuong_thuc,
                    trangthai="Chờ xác nhận"
                )

                for item in cart_items:
                    product = item['product']
                    if product.soluong < item['quantity']:
                        messages.error(request, f"Sản phẩm {product.tensanpham} không đủ hàng.")
                        return redirect("checkout")

                    Chitiethoadon.objects.create(
                        hoadonid=hoadon,
                        sanphamid=product,
                        soluong=item['quantity'],
                        giatien=product.giatien
                    )

                    product.soluong -= item['quantity']
                    product.save()

                request.session['cart'] = {}

                messages.success(request, "Thanh toán thành công! Đơn hàng của bạn đang được xử lý.")
                return redirect("home")

        except Exception as e:
            messages.error(request, f"Có lỗi xảy ra: {str(e)}")
            return redirect("checkout")

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
def hoadon_detail(request, hoadonid):
    try:
        hoadon = Hoadon.objects.get(hoadonid=hoadonid)
        chitiet_list = Chitiethoadon.objects.filter(hoadonid=hoadon)

        # Cập nhật tổng tiền cho từng chi tiết hóa đơn
        for chitiet in chitiet_list:
            chitiet.tongtien = chitiet.soluong * chitiet.giatien

        # Tính tổng tiền cho hóa đơn
        total_sum = sum(chitiet.tongtien for chitiet in chitiet_list)

    except Hoadon.DoesNotExist:
        return render(request, '404.html', {'message': 'Hóa đơn không tồn tại.'})

    return render(request, 'hoadon_detail.html', {
        'hoadon': hoadon,
        'chitiet_list': chitiet_list,
        'total_sum': total_sum,  # Tổng tiền của hóa đơn
    })
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Datsan, San, Khachhang, Taikhoan

def court_booking1(request, sanid):
    san = get_object_or_404(San, sanid=sanid)

    taikhoan_id = request.session.get('taikhoanid')
    if not taikhoan_id:
        messages.error(request, "Bạn chưa đăng nhập! Vui lòng đăng nhập để đặt sân.")
        return redirect('login')

    try:
        taikhoan = Taikhoan.objects.get(taikhoanid=taikhoan_id)
        khachhang = Khachhang.objects.get(taikhoan=taikhoan)
    except (Taikhoan.DoesNotExist, Khachhang.DoesNotExist):
        messages.error(request, "Không tìm thấy thông tin khách hàng.")
        return redirect('profile')

    if request.method == "POST":
        print("Dữ liệu POST:", request.POST)  # Debug

        ngaychoi_str = request.POST.get("date")  # Lấy ngày chơi
        thoigianbatdau_str = request.POST.get("thoigianbatdau")
        duration_str = request.POST.get("duration")

        if not ngaychoi_str or not thoigianbatdau_str or not duration_str:
            messages.error(request, "Vui lòng chọn đầy đủ ngày và thời gian đặt sân.")
            return redirect('court_booking1', sanid=sanid)

        try:
            ngaychoi = datetime.strptime(ngaychoi_str, "%Y-%m-%d").date()  # Chuyển ngày chơi thành kiểu date
            thoigianbatdau = datetime.strptime(thoigianbatdau_str, "%H:%M").time()
            duration = float(duration_str)  # Chuyển đổi thời lượng thành số giờ
            thoigianketthuc = (datetime.combine(ngaychoi, thoigianbatdau) + timedelta(hours=duration)).time()

            print(f"Ngày chơi: {ngaychoi}, Thời gian bắt đầu: {thoigianbatdau}, Thời gian kết thúc: {thoigianketthuc}")  # Debug

            datsan = Datsan.objects.create(
                sanid=san,
                khachhangid=khachhang,
                thoigianbatdau=thoigianbatdau,
                thoigianketthuc=thoigianketthuc,
                thoigiandat=ngaychoi,  # Lưu ngày chơi vào đây!
                trangthai="Chưa thanh toán"
            )

            print(f"Đặt sân thành công: {datsan.datsanid}")  # Debug

            messages.success(request, "Đặt sân thành công! Đang chờ xác nhận.")
            return redirect('court_history')

        except Exception as e:
            print("Lỗi khi lưu vào DB:", str(e))  # Debug lỗi
            messages.error(request, "Đã xảy ra lỗi khi đặt sân!")
            return redirect('court_booking1', sanid=sanid)

    return render(request, 'court_booking1.html', {'san': san})


def court_history(request):
    """ Lấy dữ liệu lịch sử đặt sân và tính tổng tiền từng sân. """
    taikhoan_id = request.session.get('taikhoanid')
    if not taikhoan_id:
        messages.error(request, "Bạn chưa đăng nhập! Vui lòng đăng nhập để xem lịch sử.")
        return redirect('login')

    try:
        taikhoan = Taikhoan.objects.get(taikhoanid=taikhoan_id)
        khachhang = Khachhang.objects.get(taikhoan=taikhoan)
    except (Taikhoan.DoesNotExist, Khachhang.DoesNotExist):
        messages.error(request, "Không tìm thấy thông tin khách hàng.")
        return redirect('profile')

    # Lấy danh sách đặt sân của khách hàng
    lich_su = Datsan.objects.filter(khachhangid=khachhang).select_related('sanid').order_by('-thoigiandat')

    for booking in lich_su:
        if booking.sanid:
            giathue = booking.sanid.giathue  # Lấy giá thuê sân từ model `San`

            # Nếu `thoigiandat` bị None, dùng ngày hiện tại
            if booking.thoigiandat is None:
                booking.thoigiandat = datetime.now()
                booking.save()  # Lưu lại để tránh lỗi lần sau

            # Chuyển đổi thời gian bắt đầu và kết thúc thành dạng datetime
            ngay_choi = booking.thoigiandat.date()
            thoigianbatdau = datetime.combine(ngay_choi, booking.thoigianbatdau)
            thoigianketthuc = datetime.combine(ngay_choi, booking.thoigianketthuc)

            # Nếu giờ kết thúc nhỏ hơn giờ bắt đầu (qua đêm), cộng thêm 1 ngày
            if thoigianketthuc < thoigianbatdau:
                thoigianketthuc += timedelta(days=1)

            # Tính thời lượng đặt sân (theo giờ)
            thoiluong = (thoigianketthuc - thoigianbatdau).total_seconds() / 3600

            # Tính tổng tiền
            tongtien = round(giathue * thoiluong, 0)

            # Lưu vào database nếu tổng tiền chưa cập nhật
            if booking.tongtien != tongtien:
                booking.tongtien = tongtien
                booking.save()

    return render(request, 'court_history.html', {'lich_su': lich_su})

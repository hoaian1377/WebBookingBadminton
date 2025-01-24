from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .models import Sanpham, San, Taikhoan
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect
from .models import CartItem

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

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Mật khẩu không khớp.')
            return render(request, 'register.html')

        if Taikhoan.objects.filter(username=username).exists():
            messages.error(request, 'Tên đăng nhập đã tồn tại.')
            return render(request, 'register.html')

        hashed_password = make_password(password)
        Taikhoan.objects.create(username=username, password=hashed_password)
        messages.success(request, 'Đăng ký thành công!')
        return redirect('login')

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Taikhoan.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
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
    return render(request, 'profile1.html')

def profile(request):
    return render(request, 'profile.html')

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
    # Logic xử lý thanh toán
    return render(request, 'checkout.html')
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
        cart_item = CartItem.objects.get(product_id=product_id)
        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart_detail')  # Hoặc đường dẫn phù hợp đến trang giỏ hàng
# home/views.py
from django.shortcuts import redirect
from .models import CartItem

def update_cart(request, product_id):
    if request.method == "POST":
        action = request.POST.get('action')
        quantity = request.POST.get('quantity')

        # Tìm cart item bằng product_id
        cart_item = CartItem.objects.get(product__sanphamid=product_id)

        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart_detail')  # Hoặc đường dẫn phù hợp đến trang giỏ hàng
from django.shortcuts import render

def checkout(request):
    # Logic xử lý thanh toán
    return render(request, 'checkout.html')
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]  # Xóa sản phẩm khỏi giỏ hàng
        messages.success(request, 'Sản phẩm đã được xóa khỏi giỏ hàng.')
    request.session['cart'] = cart
    return redirect('cart_detail')  # Điều hướng lại đến trang giỏ hàng
def update_cart(request, product_id):
    if request.method == "POST":
        action = request.POST.get('action')
        quantity = request.POST.get('quantity')

        # Logic để cập nhật giỏ hàng
        cart_item = CartItem.objects.get(product_id=product_id)
        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()
        
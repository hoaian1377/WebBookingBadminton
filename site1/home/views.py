from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Products
from .models import San
from .models import Registeruser
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request, 'home.html')

def badminton_court_booking(request):
    san_list=San.objects.all()
    return render(request, 'badminton_court_booking.html',{'san_list': san_list})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('Username')  # Match the form field name
        password = request.POST.get('Password')  # Match the form field name

        try:
            # Fetch the user from the database
            user = Registeruser.objects.get(username=username)

            # Check password
            if check_password(password, user.password):
                # Store user info in the session
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                return redirect('home')  # Redirect to the home view
            else:
                messages.error(request, 'Sai mật khẩu.')
        except Registeruser.DoesNotExist:
            messages.error(request, 'Tên đăng nhập không tồn tại.')
    
    return render(request, 'login.html')  # Reload the login page if errors occur
def court_history(request):
    return render(request, 'court_history.html')

def profile(request):
    return render(request, 'profile.html')

def profile1(request):
    return render(request, 'profile1.html')

def court_booking1(request):
    return render(request, 'court_booking1.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Kiểm tra mật khẩu khớp
        if password != confirm_password:
            messages.error(request, 'Mật khẩu không khớp.')
            return render(request, 'register.html')

        # Kiểm tra xem username và email đã tồn tại chưa
        if Registeruser.objects.filter(username=username).exists():
            messages.error(request, 'Tên đăng nhập đã tồn tại.')
            return render(request, 'register.html')
        if Registeruser.objects.filter(email=email).exists():
            messages.error(request, 'Email đã tồn tại.')
            return render(request, 'register.html')

        # Mã hóa mật khẩu và lưu vào cơ sở dữ liệu
        hashed_password = make_password(password)
        Registeruser.objects.create(username=username, email=email, password=hashed_password)
        messages.success(request, 'Đăng ký thành công!')
        return redirect('login')  # Chuyển hướng đến trang đăng nhập

    return render(request, 'register.html')


def forgot_password(request):
    return render(request, 'forgot_password.html')

def support(request):
    return HttpResponseRedirect("https://docs.google.com/forms/d/e/1FAIpQLSdsZGwFck63-cPDZcW8gZyyMAhf2UyYaOINuByEgwbMvtTm3A/viewform")

def shop(request):
    products = Products.objects.filter(isactive=True)  # Fetch active products
    return render(request, 'shop.html', {'products': products})

def item_detail(request, pk):
    products = get_object_or_404(Products, pk=pk)
    return render(request, 'item_detail.html', {'products': products})

def cart_detail(request):

    cart = request.session.get('cart', {})
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Products, pk=product_id)
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity
        })
        total += product.price * quantity

    return render(request, 'cart_detail.html', {'cart_items': products, 'total': total})

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')  # Lấy product_id từ form
        quantity = int(request.POST.get('quantity', 1))  # Lấy số lượng, mặc định là 1

        # Lấy giỏ hàng từ session hoặc tạo mới nếu chưa có
        cart = request.session.get('cart', {})

        # Thêm hoặc cập nhật sản phẩm trong giỏ hàng
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

        # Lưu giỏ hàng lại vào session
        request.session['cart'] = cart

        return redirect('cart_detail')  # Điều hướng đến trang chi tiết giỏ hàng

    return redirect('shop')  # Điều hướng đến trang shop nếu không phải POST

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import UserRegistrationForm, OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.db.models import Count

def index(request):
    dishes = Dish.objects.annotate(total_likes=Count('likes')).order_by('-total_likes')
    liked_dishes = request.user.liked_dishes.values_list('id', flat=True) if request.user.is_authenticated else []
    return render(request, 'index.html', {'dishes': dishes, 'liked_dishes': liked_dishes})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

def menu(request):
    dishes = Dish.objects.all()
    context = {
        'dishes': dishes,
    }
    return render(request, 'menu.html', context)

def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == 'POST':
        if 'text' in request.POST:
            text = request.POST.get('text')
            Comment.objects.create(dish=dish, user=request.user, text=text)
        elif 'like_comment_id' in request.POST:
            comment_id = request.POST.get('like_comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            comment.likes.add(request.user)
        return redirect('dish_detail', dish_id=dish.id)
    comments = dish.comments.all()
    return render(request, 'dish_detail.html', {'dish': dish, 'comments': comments})

@login_required
def add_comment(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == 'POST':
        text = request.POST.get('content')
        Comment.objects.create(dish=dish, user=request.user, text=text)
        return redirect('dish_detail', dish_id=dish.id)
    return redirect('dish_detail', dish_id=dish.id)

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
    if not created:
        like.delete()
    return redirect('dish_detail', dish_id=comment.dish.id)

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, dish=dish)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{dish.name} додано до кошика.")
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    messages.success(request, "Страву видалено з кошика.")
    return redirect('cart_detail')

@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.error(request, "Ваш кошик порожній.")
        return redirect('menu')

    order = Order.objects.create(user=request.user, total_price=0)
    total_price = 0

    for item in cart_items:
        OrderItem.objects.create(order=order, dish=item.dish, quantity=item.quantity)
        total_price += item.dish.price * item.quantity

    order.total_price = total_price
    order.save()

    cart_items.delete()
    messages.success(request, "Замовлення створено успішно.")
    return redirect('order_detail', order_id=order.id)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})

@login_required
def like_dish(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    like, created = Like.objects.get_or_create(user=request.user, dish=dish)
    if not created:
        like.delete()
    return redirect('index')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user.is_superuser:
        comment.delete()
        messages.success(request, 'Коментар видалено.')
    else:
        messages.error(request, 'Ви не маєте дозволу на видалення цього коментаря.')
    return redirect('dish_detail', dish_id=comment.dish.id)
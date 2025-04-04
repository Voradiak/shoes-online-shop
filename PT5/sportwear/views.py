from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CommentForm
from django.core.paginator import Paginator
from .models import Comment, Shoe, Favourite, Cart
import json

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def products_page(request):
    shoes = Shoe.objects.all()
    paginator = Paginator(shoes, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products.html', {'page_obj': page_obj, 'shoes': shoes})


def about_page(request):
    return render(request, 'about.html')

def contacts_page(request):
    return render(request, 'contacts.html')

def index_page(request):
    comments = Comment.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('index')
    else:
        form = CommentForm()
    return render(request, 'index.html', {'form': form, 'comments': comments})

@login_required
def add_to_favourites(request, product_id):
    product = get_object_or_404(Shoe, id=product_id)
    favourite, created = Favourite.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f'Товар "{product.name}" добавлен в избранное.')
    else:
        messages.info(request, f'Товар "{product.name}" уже находится в избранном.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Shoe, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'Товар "{product.name}" добавлен в корзину.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

@login_required
def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def favourite_list(request):
    favourites = Favourite.objects.filter(user=request.user)
    return render(request, 'favourite_list.html', {'favourites': favourites})

@login_required
def favourite_remove(request, favourite_id):
    favourite = get_object_or_404(Favourite, id=favourite_id, user=request.user)
    favourite.delete()
    return redirect('favourite_list')

def product_page(request, product_slug):
    product = get_object_or_404(Shoe, slug=product_slug)
    comments = product.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            messages.success(request, 'Ваш комментарий добавлен')
            return redirect('product_page', product_slug=product.slug)
    else:
        form = CommentForm()

    return render(request, 'product_page.html', {
        'product': product,
        'comments': comments,
        'form': form,
    })
    
@staff_member_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, 'Комментарий успешно удален.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def update_cart_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                return JsonResponse({'success': True, 'total_price': cart_item.total_price()})
            else:
                cart_item.delete()
                return JsonResponse({'success': True, 'deleted': True})
        except (ValueError, KeyError):
            return JsonResponse({'success': False, 'error': 'Invalid input'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
# Create your views here.

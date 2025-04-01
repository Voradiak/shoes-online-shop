from django.urls import path
from .views import register, user_login, logout_view, contacts_page, about_page, index_page, delete_comment
from .views import products_page, add_to_cart, remove_from_cart, add_to_favourites, cart_detail, favourite_list, favourite_remove, decrease_quantity, increase_quantity, product_page

urlpatterns = [
    path('', index_page, name='index'),
    path('products/', products_page, name='products'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('contacts/', contacts_page, name='contacts'),
    path('about/', about_page, name='about'),
    path('favourites/<int:product_id>/', add_to_favourites, name='add_to_favourites'),
    path('cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('favourites/', favourite_list, name='favourite_list'),
    path('favourites/remove/<int:favourite_id>/', favourite_remove, name='favourite_remove'),
    path('cart/decrease/<int:cart_id>/', decrease_quantity, name='decrease_quantity'),
    path('cart/increase/<int:cart_id>/', increase_quantity, name='increase_quantity'),
    path('products/<slug:product_slug>/', product_page, name='product_page'),
    path('comments/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
]
from django.urls import path, include
from . import views


urlpatterns = [
    path('demo_django/', views.home, name="home"),
    path('demo_django/store/', views.store, name="store"),
    path('demo_django/store/products_items/', views.products_items, name="products_items"),
	path('demo_django/store/cart/', views.cart, name="cart"),
	path('demo_django/store/checkout/', views.checkout, name="checkout"),
    # adding items inside cart
    path('demo_django/store/update_item/', views.updateItem, name="update_item"),
    # proceed to payment
    path('demo_django/store/process_order/', views.processOrder, name="process_order"),
    # user login/logout
    path('demo_django/store/user_login/', views.user_login, name="login"),
    path('demo_django/store/user_signup/', views.user_signup, name="signup"),
    path('demo_django/store/user_logout/', views.user_logout, name="logout"),
    path('demo_django/scraping/', include('scraping.urls')),
]

from django.urls import path
from . import views


urlpatterns = [
    path('', views.scraping_home, name='scraping_home'),
    path('search_products/', views.search_products, name='search_products'),
]

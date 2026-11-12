from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.home, name='home'),
    path('ad/<int:pk>/', views.listing_detail, name='detail'),
    path('post/', views.create_ad, name='create_ad'),
    path('dashboard/', views.seller_dashboard, name='dashboard'),
    path('ad/<int:pk>/edit/', views.edit_ad, name='edit_ad'),  # <-- Add this line
    path('ad/<int:pk>/toggle-sold/', views.toggle_sold_status, name='toggle_sold'),
    path('ad/<int:pk>/delete/', views.delete_ad, name='delete_ad'),
    path('store/<str:username>/', views.seller_store_view, name='seller_store'),
]
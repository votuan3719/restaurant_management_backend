from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from restaurant import views

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('api/signup/staff/', views.register_staff, name='register_staff'),
    path('api/signup/customer/', views.register_customer, name='register_customer'),

    path('api/login/', views.login, name='login'),

    path('api/menu/add/', views.create_menu_item, name='create_menu_item'),
    path('api/menu/update/', views.update_menu_item, name='update_menu_item'),
    path('api/menu/delete/', views.delete_menu_item, name='delete_menu_item'),
    
    path('api/order/add/', views.place_order, name='place_order'),
    path('api/order/view/today/', views.view_orders_today, name='view_orders_today'),
    path('api/order/view/customer/', views.view_customer_order, name='view_customer_order'),
    path('api/order/update/status/', views.update_order_status, name='update_order_status'),

    path('api/menu/view/', views.view_menu, name='view_menu'),
    
]

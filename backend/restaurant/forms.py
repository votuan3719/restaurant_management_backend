from django import forms
from django.contrib.auth.models import User
from .models import Staff, Customer, Menu, Order, OrderItem
from django.contrib.auth.password_validation import validate_password


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['phone_number']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'address', 'city', 'state', 'zip_code']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'description', 'price']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_id', 'total_amount', 'status']

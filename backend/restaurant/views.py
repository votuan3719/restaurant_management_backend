from datetime import date

from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import UserForm, StaffForm, CustomerForm, MenuItemForm
from .models import Staff, Customer, Menu, Order, OrderItem

from .services import add_new_customer, add_new_staff, add_menu_item, update_menu_item, add_order_item
from .permissions import IsStaff, IsCustomer, IsStaffOrCustomer

@api_view(['POST'])
@permission_classes([])
def register_staff(request):
    staff_info = request.data

    try:
        if staff_info:
            user_info = UserForm(staff_info)
            staff_info = StaffForm(staff_info)

            if user_info.is_valid() and staff_info.is_valid():
                user_info = user_info.cleaned_data
                staff_info = staff_info.cleaned_data

                created = add_new_staff(user_info, staff_info)
                if created:
                    return JsonResponse({
                        'message': 'Staff created successfully'
                        },
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return JsonResponse({
                        'error': 'Staff creation failed'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    ) 
    except Exception as e:
        return JsonResponse({
            'error': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([])
def register_customer(request):
    customer_info = request.data

    try:
        if customer_info:
            user_info = UserForm(customer_info)
            customer_info = CustomerForm(customer_info)

            if user_info.is_valid() and customer_info.is_valid():
                user_info = user_info.cleaned_data
                customer_info = customer_info.cleaned_data

                created = add_new_customer(user_info, customer_info)
                if created:
                    return JsonResponse({
                        'message': 'Customer created successfully'
                        },
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return JsonResponse({
                        'error': 'Customer creation failed'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    ) 
    except Exception as e:
        return JsonResponse({
            'error': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([])
def login(request):
    
    username = request.data['username']
    password = request.data['password']
    if not username or not password:
        return JsonResponse({
            'error': 'Username and password are required'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    if not user:
        return JsonResponse({
            'error': 'Invalid credentials'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    refresh = RefreshToken.for_user(user)
    return JsonResponse({
            'message': 'Login successful',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, 
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStaff])
def create_menu_item(request):
        item_info = request.data

        try:
            if item_info:
                item_info = MenuItemForm(item_info)

                if item_info.is_valid():
                    item_info = item_info.cleaned_data

                    created = add_menu_item(item_info)
                    if created:
                        return JsonResponse({
                            'message': 'Menu item created successfully',
                        }, 
                        status=status.HTTP_201_CREATED
                    )
                    else:
                        return JsonResponse({
                            'error': 'Menu item creation failed',
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStaff])
def update_menu_item(request):
    menu_id = request.data['menu_id']
    item_info = request.data

    try:
        if item_info:
            item_info = MenuItemForm(item_info)

            if item_info.is_valid():
                item_info = item_info.cleaned_data
                
                updated = update_menu_item(menu_id, item_info)
                if updated:
                    return JsonResponse({
                        'message': 'Menu item updated successfully',
                        }, 
                        status=status.HTTP_200_OK
                    )
                else:
                    return JsonResponse({
                        'error': 'Menu item update failed',
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
    except Menu.DoesNotExist:
        return JsonResponse({
            'error': 'Menu item not found',
        }, 
        status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStaff])
def delete_menu_item(request):
    menu_id = request.data['menu_id']
    
    try:
        item = Menu.objects.get(menu_id=menu_id)
        if item:
            item.delete()

            return JsonResponse({
                'message': 'Menu item deleted successfully',
            }, 
            status=status.HTTP_200_OK
        )
    except Menu.DoesNotExist:
        return JsonResponse({
            'error': 'Menu item not found',
        }, 
        status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsCustomer])
def place_order(request):
    customer = Customer.objects.get(user=request.user)
    menu_items = request.data['menu_items']
    
    if not menu_items:
        return JsonResponse({
                'error': 'No items in order'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    customer_id = customer.customer_id
    order_info = {
        'customer_id': customer_id,
        'total_amount': 0,
        'status': 'pending',
    }
    order = OrderForm(order_info)
    if order.is_valid():
        order = order.save()

    order_id = order.order_id
    try:
        total_amount = 0

        for item in menu_items:
            menu_id = item['menu_id']
            quantity = item['quantity']
            
            amount = add_order_item(order_id, customer_id, menu_id, quantity)
            if amount:
                total_amount += amount
            else:
                return JsonResponse({
                    'error': 'Order item creation failed',
                }, 
                status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, 
        status=status.HTTP_400_BAD_REQUEST
        )

    if total_amount:
        order.total_amount = total_amount
        order.save()
        
        return JsonResponse({
            'message': 'Order placed successfully'
        }, 
        status=status.HTTP_201_CREATED
        )
    else:
        return JsonResponse({
            'error': 'Order placement unsuccessful',
        }, 
        status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaff])
def view_orders_today(request):
    curr_date = date.today()
    orders_today = []

    try:
        orders = Order.objects.filter(date=curr_date)

        for order in orders:
            order_id = order.order_id
            customer_id = order.customer_id
            total_amount = order.total_amount
            status = order.status
            date = order.date

            orders_today.append({
                'order_id': order_id,
                'customer_id': customer_id,
                'total_amount': total_amount,
                'status': status,
                'date': date
            })

        return Response({
            'orders': orders_today
            },
            status=status.HTTP_200_OK
        )
    except Order.DoesNotExist:
        return JsonResponse({
            'error': 'Order not found',
        }, 
        status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaff])
def view_customer_order(request):
    customer_id = request.data['customer_id']
    order_id = request.data['order_id']

    try:
        order = Order.objects.get(customer_id=customer_id, order_id=order_id)
        if order:
            order_id = order.order_id
            order_items = OrderItem.objects.filter(order_id=order_id)

            menu_items = []
            for item in order_items:
                menu_id = item.menu_id
                quantity = item.quantity

                menu_item = Menu.objects.get(menu_id=menu_id)
                name = menu_item.name
                description = menu_item.description
                price = menu_item.price

                menu_items.append({
                    'name': name,
                    'description': description,
                    'price': price,
                    'quantity': quantity
                })

            customer_order = {
                'order_id': order_id,
                'customer_id': order.customer_id,
                'items': menu_items,
                'total_amount': order.total_amount,
                'date': order.date            
            }
    
            return JsonResponse({
                'customer_order': customer_order
                },
                status=status.HTTP_200_OK
            )
    except Order.DoesNotExist:
        return JsonResponse({
            'error': 'Order not found',
        }, 
        status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStaff])
def update_order_status(request):
    customer_id = request.data['customer_id']
    order_id = request.data['order_id']
    status = request.data['status']

    try:
        order = Order.objects.get(customer_id=customer_id, order_id=order_id)
        if order:
            order.status = status
            order.save()

            return JsonResponse({
                'message': 'Order status updated successfully',
            }, 
            status=status.HTTP_200_OK
        )
    except Order.DoesNotExist:
        return JsonResponse({
            'error': 'Order not found',
        }, 
        status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffOrCustomer])
def view_menu(request):
    menu_items = []
    
    try:
        menu = Menu.objects.all()
 
        for item in menu:
            name = item.name
            description = item.description
            price = item.price

            menu_items.append({
                'name': name,
                'description': description,
                'price': price
            })

        return JsonResponse({
            'menu': menu_items
            },
            status=status.HTTP_200_OK
        )
    except Menu.DoesNotExist:
        return JsonResponse({
            'error': 'Menu not found',
        }, 
        status=status.HTTP_404_NOT_FOUND
        )


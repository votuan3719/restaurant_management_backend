from django.contrib.auth.models import User
from .models import Staff, Customer, Menu, Order, OrderItem

def add_new_staff(user_info, staff_info):
    user, user_created = User.objects.get_or_create(
        username=user_info['username'],
        email=user_info['email'],
        defaults={
            'first_name': user_info['first_name'],
            'last_name': user_info['last_name'],
            'username': user_info['username'],
            'email': user_info['email']},
    )
    if user_created:
        user.set_password(user_info['password'])
        user.save()
    else:
        return False

    staff, staff_created = Staff.objects.get_or_create(
        user=user,
        defaults={
            'user': user,
            'phone_number': staff_info['phone_number']},
    )
    if staff_created:
        staff.save()
    else:
        return False

    return staff_created        

def add_new_customer(user_info, customer_info):
    user, user_created = User.objects.get_or_create(
        username=user_info['username'],
        email=user_info['email'],
        defaults={
            'first_name': user_info['first_name'],
            'last_name': user_info['last_name'],
            'username': user_info['username'],
            'email': user_info['email']},
    )
    if user_created:
        user.set_password(user_info['password'])
        user.save()
    else:
        return False

    customer, customer_created = Customer.objects.get_or_create(
        user=user,
        defaults={
            'user': user,
            'phone_number': customer_info['phone_number'],
            'address': customer_info['address'],
            'city': customer_info['city'],
            'state': customer_info['state'],
            'zip_code': customer_info['zip_code']
        }
    )
    if customer_created:
        customer.save()
    else:
        return False

    return customer_created

def add_menu_item(item_info):
    item, item_created = Menu.objects.get_or_create(
        category=item_info['category'],
        name=item_info['name'],
        description=item_info['description'],
        price=item_info['price'],
        defaults={
            'category': item_info['category'],
            'name': item_info['name'],
            'description': item_info['description'],
            'price': item_info['price']
        }
    )
    if item_created:
        item.save()
    else:
        return False

    return item_created

def update_menu_item(menu_id, item_info):
    try:
        item = Menu.objects.get(menu_id=menu_id)
        item.update(
            category=item_info['category'],
            name=item_info['name'],
            description=item_info['description'],
            price=item_info['price']
        )
        return True
    except Menu.DoesNotExist:
        return False

def add_order_item(order_id, menu_id, quantity):
    amount = 0
    try:
        menu_item = Menu.objects.get(menu_id=menu_id)
        OrderItem.objects.create(
            order_id=order_id,
            menu_id=menu_id,
            quantity=quantity,
            price=menu_item.price
        )
        amount += menu_item.price * quantity
    except Menu.DoesNotExist:
        return False
    return amount


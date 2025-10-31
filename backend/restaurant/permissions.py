from rest_framework.permissions import BasePermission

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated
        is_staff = Staff.objects.filter(user=request.user).exists()

        if not is_authenticated:
            return False
        if not is_staff:
            return False
        
        return True

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated
        is_customer = Customer.objects.filter(user=request.user).exists()

        if not is_authenticated:
            return False
        if not is_customer:
            return False
        
        return True

class IsStaffOrCustomer(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated
        is_staff = Staff.objects.filter(user=request.user).exists()
        is_customer = Customer.objects.filter(user=request.user).exists()

        if not is_authenticated:
            return False
        if not is_staff and not is_customer:
            return False
        
        return True
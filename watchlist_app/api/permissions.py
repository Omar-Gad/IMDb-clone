from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
    """Permission class that allows admin only to update data"""
    def has_permission(self, request, view):
        admin_permission = super().has_permission(request, view) #bool(request.user and request.user.is_staff) => Returns a boolean checking if user is staff
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return admin_permission
    
class IsReviewOwnerOrReadOnly(permissions.BasePermission):
    """Permission class that allows only owner to update review"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user == obj.review_user or request.user.is_staff
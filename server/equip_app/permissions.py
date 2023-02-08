from rest_framework import permissions

class IsAuthOrAnyoneCanCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated
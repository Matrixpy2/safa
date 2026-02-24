from rest_framework.permissions import BasePermission , IsAuthenticated

class Is_student(BasePermission):
    def has_permission(self , request , view):
        return request.user.groups.filter(name='students').exists()
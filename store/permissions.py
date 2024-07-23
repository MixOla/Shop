from rest_framework import permissions
from django.contrib.auth import get_user_model
from orders.models import OrderItem


class IsGoodsBoughtByUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return OrderItem.objects.filter(
            order__user_id=request.user.id,
            order__status='succeeded',
            goods_id=obj.goods.id
        ).exists()

    

class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author_id == request.user.id
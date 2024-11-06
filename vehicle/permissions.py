from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):

    def has_permission(self, request, view):
        """Добавляем права доступа"""
        if request.user.is_staff:  # Проверка, что пользователь менеджер
            return True

        return request.user == view.get_object().owner  # Проверка, что
        # пользователь владелец

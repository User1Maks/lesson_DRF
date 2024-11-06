from rest_framework.pagination import PageNumberPagination


class VehiclePaginator(PageNumberPagination):
    """Для пагинации"""
    page_size = 10  # Количество элементов на странице



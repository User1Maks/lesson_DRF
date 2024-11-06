from rest_framework import status
from rest_framework.test import APITestCase


class VehicleTestCase(APITestCase):

    def setUp(self) -> None:
        pass

    def test_create_car(self):
        """
        Тестирование на создание машины
         self.client - это экземпляр класса APIClient, который уже есть и
         доступен для работы.
        """
        data = {
            'title': 'Test',
            'description': 'Test description'
        }

        response = self.client.post(
            '/cars/',
            data=data
        )

        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

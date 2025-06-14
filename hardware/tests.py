from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from hardware.models import Category
from hardware.serializers import HardwareCategorySerializer
from inventio_auth.models import Role
from shared import RoleEnum


class CategoryViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        for role in RoleEnum:
            Role.objects.create(name=role.value)

        self.user = get_user_model().objects.create(
            email='testTechnician@test.test',
            password='testpass123',
            role = RoleEnum.TECHNICIAN,
            name = 'TestName',
            surname = 'TestSurname'
        )

        self.client.force_authenticate(user=self.user)  # Uwierzytelnienie

        self.category_data = {
            "name": "Testowa kategoria",
        }
        self.category = Category.objects.create(**self.category_data)
        self.url_list = reverse("hardware:categories-list")
        self.url_detail = reverse("hardware:categories-detail", args=[self.category.id])

    def test_get_all_categories(self):
        response = self.client.get(self.url_list)
        categories = Category.objects.all()
        serializer = HardwareCategorySerializer(categories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


    def test_get_category(self):
        response = self.client.get(self.url_detail)
        category = Category.objects.get(id=self.category.id)
        serializer = HardwareCategorySerializer(category)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_category(self):
        new_task_data = {
            "name": "Testowa kategoria dla testu tworzenia",
        }
        response = self.client.post(self.url_list, new_task_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_update_category(self):
        updated_data = {
            "name": "Testowa kategoria 2",
        }
        response = self.client.put(self.url_detail, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Testowa kategoria 2")

    def test_delete_category(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)  # Powinno być 0 zadań (usunięto jedyne zadanie)
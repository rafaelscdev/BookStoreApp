import json

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from order.factories import UserFactory
from product.factories import CategoryFactory
from product.models import Category


class TestCategoryViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.token = Token.objects.get_or_create(user=self.user)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.category = CategoryFactory(title="books")

    def test_get_all_category(self):
        response = self.client.get(reverse("category-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category_data = json.loads(response.content)

        self.assertEqual(category_data["results"][0]["title"], self.category.title)

    def test_create_category(self):
        data = json.dumps(
            {
                "title": "technology",
                "slug": "technology",
                "description": "Technology products",
                "active": True,
            }
        )

        response = self.client.post(
            reverse("category-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_category = Category.objects.get(title="technology")
        self.assertEqual(created_category.title, "technology")
        self.assertEqual(created_category.slug, "technology")
        self.assertEqual(created_category.description, "Technology products")
        self.assertEqual(created_category.active, True)

import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from product.factories import CategoryFactory, ProductFactory
from product.models import Product
from order.factories import UserFactory


class TestProductViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="mouse", price=100
        )
        self.product.categories.add(self.category)

    def test_get_all_product(self):
        response = self.client.get(
            reverse("product-list", kwargs={"version": "v1"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product_data = json.loads(response.content)
        self.assertEqual(
            product_data[0]["title"], self.product.title
        )
        self.assertEqual(
            product_data[0]["price"], self.product.price
        )
        self.assertEqual(
            product_data[0]["active"], self.product.active
        )
        self.assertEqual(
            product_data[0]["categories"][0]["title"],
            self.category.title,
        )

    def test_create_product(self):
        data = json.dumps(
            {
                "title": "keyboard",
                "description": "keyboard gamer",
                "price": 200,
                "active": True,
                "categories_id": [self.category.id],
            }
        )

        response = self.client.post(
            reverse("product-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_product = Product.objects.get(title="keyboard")
        self.assertEqual(created_product.title, "keyboard")
        self.assertEqual(created_product.description, "keyboard gamer")
        self.assertEqual(created_product.price, 200)
        self.assertEqual(created_product.active, True)
        self.assertEqual(created_product.categories.first().title, "technology")
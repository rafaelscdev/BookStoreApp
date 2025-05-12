import json

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from order.factories import UserFactory
from product.factories import CategoryFactory, ProductFactory
from product.models import Product


class TestProductViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.token = Token.objects.get_or_create(user=self.user)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(title="mouse", price=100)
        self.product.categories.add(self.category)

    def test_get_all_product(self):
        response = self.client.get(reverse("product-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product_data = json.loads(response.content)
        self.assertEqual(product_data["results"][0]["title"], self.product.title)
        self.assertEqual(product_data["results"][0]["price"], self.product.price)
        self.assertEqual(product_data["results"][0]["active"], self.product.active)
        self.assertEqual(
            product_data["results"][0]["categories"][0]["title"],
            self.category.title,
        )

    def test_create_product(self):
        product_count = Product.objects.count()
        product_dict = {
            "title": "pro controller",
            "description": "nintendo switch pro controller",
            "price": 450.00,
            "active": True,
            "categories_id": [self.category.id],
        }
        response = self.client.post(
            reverse("product-list", kwargs={"version": "v1"}),
            data=product_dict,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), product_count + 1)

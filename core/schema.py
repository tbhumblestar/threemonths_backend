from pymysql import NULL
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

from orders.models import Order
from orders.serializers import (
    PackageOrderSerializer,
    CafeOrderSerializer,
    CakeOrderSerializer,
)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="package_order",
            description="additional_explanation ,purpose 필드는 존재하지 않아도 괜찮음 ",
            request_only=True,
            value={
                "title": "test",
                "type": "package",
                "customer_name": "tester",
                "contact": "010-0000-0000",
                "additional_explanation": "test_explanation",
                "delivery_location": "test_location",
                "delivery_date": "2022-10-10",
                "purpose": "testasd",
                "orderedproducts": [
                    {"product_id": 4, "buying": "True"},
                    {"product_id": 8, "buying": "True"},
                ],
            },
        ),
        OpenApiExample(
            name="cake_order",
            description="additional_explanation 필드는 존재하지 않아도 괜찮음",
            request_only=True,
            value={
                "title": "testingasdsad",
                "type": "cake",
                "customer_name": "tester",
                "contact": "010-0000-0000",
                "additional_explanation": "test_explanation",
                "status": "not_confirmed",
                "product_id": 13,
                "want_pick_up_date": "2022-10-15",
                "superdubaduib": "asdasdasd",
                "count": 3,
            },
        ),
        OpenApiExample(
            name="cafe_order",
            description="additional_explanation 필드는 존재하지 않아도 괜찮음",
            request_only=True,
            value={
                "title": "test",
                "type": "cafe",
                "customer_name": "tester",
                "contact": "010-0000-0000",
                "additional_explanation": "test_explanation",
                "cafename": "testcafe",
                "cafe_owner_name": "test_owner",
                "corporate_registration_num": "kkk",
                "cafe_location": "test_location",
                "product_explanation": "asdasdasd",
            },
        ),
        # Response Example
        OpenApiExample(
            name="package_order_response",
            response_only=True,
            value={
                "id": 342,
                "type": "package",
                "title": "test",
                "customer_name": "tester",
                "contact": "010-0000-0000",
                "status": "not_confirmed",
                "additional_explanation": NULL,
                "created_at": "2022-08-08T03:40:58.554790",
                "updated_at": "2022-08-08T03:40:58.554824",
                "packageorders": {
                    "id": 182,
                    "delivery_location": "test_location",
                    "delivery_date": "2022-10-10",
                    "is_packaging": NULL,
                    "purpose": "testasdasdfgasdasdasdasdasdasdsad",
                    "orderedproducts": [
                        {"product_id": 4, "buying": True, "product_name": "플레인 휘낭시에"},
                        {"product_id": 8, "buying": True, "product_name": "둘세 마들렌"},
                    ],
                },
            },
        ),
        OpenApiExample(
            name="cake_order_response",
            response_only=True,
            value={
                "id": 346,
                "type": "cake",
                "title": "testingasdsad",
                "customer_name": "tester",
                "contact": "010-0000-0000",
                "status": "not_confirmed",
                "additional_explanation": NULL,
                "created_at": "2022-08-08T04:12:07.160059",
                "updated_at": "2022-08-08T04:12:07.160088",
                "cakeorders": {
                    "id": 65,
                    "product_id": 16,
                    "product_name": "시즌 케이크(딸기)",
                    "want_pick_up_date": "2022-10-15",
                    "count": 3,
                },
            },
        ),
        OpenApiExample(
            name="cafe_order_response",
            response_only=True,
            value={
                "id": 347,
                "type": "cafe",
                "title": "test",
                "customer_name": "tester",
                "contact": "010-0000-0000",
                "status": "not_confirmed",
                "additional_explanation": NULL,
                "created_at": "2022-08-08T04:13:11.779439",
                "updated_at": "2022-08-08T04:13:11.779466",
                "cafeorders": {
                    "id": 48,
                    "cafename": "testcafe",
                    "cafe_owner_name": "test_owner",
                    "corporate_registration_num": "kkk",
                    "cafe_location": "test_location",
                    "product_explanation": "asdasdasd",
                },
            },
        ),
    ]
)
class OrderSerializerSchema(serializers.ModelSerializer):

    packageorders = PackageOrderSerializer()
    cafeorders = CafeOrderSerializer()
    cakeorders = CakeOrderSerializer()

    class Meta:
        model = Order
        fields = [
            "id",
            "type",
            "title",
            "customer_name",
            "contact",
            "status",
            "additional_explanation",
            "created_at",
            "updated_at",
            "packageorders",
            "cafeorders",
            "cakeorders",
        ]

from rest_framework import  serializers
from .models import Product,Cart,Review
from django.contrib.auth.models import User


class ReviewSerializer(serializers.ModelSerializer):
    # This means that these fields will not be used for deserialization
    # (i.e., they won't be expected as input when creating or updating instances),
    # and they will only be used for serialization (i.e., they will be included when
    # sending data to the client).
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    product = serializers.CharField(read_only=True)
    class Meta:
        model = Review
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):

    # This means that these fields will not be used for deserialization
    # (i.e., they won't be expected as input when creating or updating instances),
    # and they will only be used for serialization (i.e., they will be included when
    # sending data to the client).
    id=serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    product = serializers.CharField(read_only=True)
    date = serializers.CharField(read_only=True)

    class Meta:
        model=Cart
        fields="__all__"


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)




class ProductSerializer(serializers.ModelSerializer):
    avg_rating = serializers.ReadOnlyField()

    # Add a read-only field for avg_rating
    ratingcount = serializers.SerializerMethodField()

    class Meta:
        model=Product
        fields="__all__"

    # custom method for total number of reviews for each product
    def get_ratingcount(self, obj):
        ratings = obj.product_reviews.all().values_list("rating", flat=True)
        if ratings:
            return len(ratings)
        else:
            return 0

# class ProductSerializer(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField()
#     price=serializers.IntegerField()
#     description=serializers.CharField()
#     category=serializers.CharField()
#     image=serializers.ImageField()
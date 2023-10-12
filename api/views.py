from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product,Cart,Review
from django.core import serializers
from .serializers import ProductSerializer,AuthUserSerializer,CartSerializer,ReviewSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics,mixins
from rest_framework.authentication import TokenAuthentication


class ReviewDetailViewset(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class CartModelViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


    # all below 3 gives same result
    # in this case we need to pass like http://127.0.0.1:8000/api/cart/?user_id=4
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['user_id']

    # def list(self, request, *args, **kwargs):
    #     user=request.user
    #     cartData=Cart.objects.filter(user=user)
    #     serializer=CartSerializer(cartData,many=True)
    #     return Response(data=serializer.data)

    # equivalent to above list
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)



class UsermodelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AuthUserSerializer
    # permission_classes = [IsAuthenticated]


# modelviewset method
class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    #authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    # we can create custom methods for our needs
    @action(methods=['GET'],detail=False)
    def getCategory(self,request):
        data=Product.objects.values_list('category',flat=True).distinct()
        return Response(data=data)

    # here we just take the productview and a custom method to add a product to cart
    # http://127.0.0.1:8000/api/productmodelsviewset/6/addtoCart/
    @action(methods=["POST"],detail=True)
    def addtoCart(self,request,*args,**kwargs):
        pid=kwargs.get("pk")
        user=request.user
        product=Product.objects.get(id=pid)
        user.user_carts.create(product=product)
        return Response(data="successfully added to cart")

    # http://127.0.0.1:8000/api/productmodelsviewset/6/addReview/
    @action(methods=["POST"], detail=True)
    def addReview(self, request, *args, **kwargs):
        pid = kwargs.get("pk")
        user = request.user
        product = Product.objects.get(id=pid)
        review_serializer=ReviewSerializer(data=request.data)
        if review_serializer.is_valid():
            review_serializer.save(user=user,product=product)
            return Response(data=review_serializer.data)
        else:
            return Response(review_serializer.errors)

    # http://127.0.0.1:8000/api/productmodelsviewset/6/getProductReview/
    @action(methods=["GET"], detail=True)
    def getProductReview(self, request, *args, **kwargs):
        # pid = kwargs.get("pk")
        # product=Product.objects.get(id=pid)
        # equivalent to above
        product=self.get_object()#**************************
        # review=Review.objects.filter(product=product)
        # accessed with related name
        review=product.product_reviews.all()#*****************

        review_serializer=ReviewSerializer(review,many=True)
        return Response(data=review_serializer.data, status=status.HTTP_200_OK, )





# viewset method
class ProductViewsetClassView(viewsets.ViewSet):
    def list(self,request):
        products=Product.objects.all()
        productSerialer = ProductSerializer(products, many=True)
        return Response(data=productSerialer.data)

    def create(self,request):
        productSerialer = ProductSerializer(data=request.data)
        if productSerialer.is_valid():
            productSerialer.save()
            return Response(productSerialer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(productSerialer.errors)

    def retrieve(self,request,pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except:
            return Response(data={"status": "failure"}, status=status.HTTP_400_BAD_REQUEST)
        product_serializer = ProductSerializer(product)
        return Response(data=product_serializer.data, status=status.HTTP_200_OK, )

    def update(self,request,pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except:
            return Response(data={"status": "failure"}, status=status.HTTP_400_BAD_REQUEST)
        product_serializer = ProductSerializer(product, request.data)
        # product_serializer = ProductSerializer(instance=product, data=request.data)

        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data)
        else:
            return Response(product_serializer.errors)

    def destroy(self,request,pk=None):
        try:
            product = Product.objects.get(pk=pk)
            print(product)
        except:
            return Response(data={"status": "failure"}, status=status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,data="success")




# APIView method
class ProductListView(APIView):
    def get(self,request):
        products=Product.objects.all()
        productSerialer=ProductSerializer(products,many=True)

        return Response(data=productSerialer.data)
    def post(self,request):

        product_serializer = ProductSerializer(data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(product_serializer.errors)


class ProductDetailUpdateDeleteView(APIView):
    def get(self,request,pk):
        try:
            product = Product.objects.get(pk=pk)
        except:
            return Response(data={"status": "failure"}, status=status.HTTP_400_BAD_REQUEST)
        product_serializer = ProductSerializer(product)
        return Response(data=product_serializer.data, status=status.HTTP_200_OK, )


    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except:
            return Response(data={"status": "failure"}, status=status.HTTP_400_BAD_REQUEST)
        product_serializer = ProductSerializer(product, request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data)
        else:
            return Response(product_serializer.errors)


    def delete(self, request,pk):
        try:
            product = Product.objects.get(pk=pk)
            print(product)
        except:
            return Response(data={"status": "failure"}, status=status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,data="success")
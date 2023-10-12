from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken
from api import views



router=DefaultRouter()
router.register('productsviewset',views.ProductViewsetClassView,basename='productsviewset')
router.register('productmodelsviewset',views.ProductModelViewSet,basename='productmodelsviewset')
router.register('user',views.UsermodelViewSet,basename='user')
router.register('cart',views.CartModelViewSet,basename='cart')




urlpatterns = [
    path('products',views.ProductListView.as_view(),name='products'),
    path('products/<int:pk>/', views.ProductDetailUpdateDeleteView.as_view(), name='products-detail'),#apiview method
    path("", include(router.urls)),#viewset method
    # path('getCategory', views.ProductModelViewSet.as_view({'get': 'getCategory'}), name='get-category'),#not needed since above route contains this and  +router.urls adds all
    path('reviews/<int:pk>/', views.ReviewDetailViewset.as_view(), name='review-detail'),
    path('token', ObtainAuthToken.as_view(), name='token_obtain'),
]+router.urls

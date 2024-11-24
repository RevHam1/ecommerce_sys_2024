from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from store import views as store_views
from userauths import views as userauths_views

urlpatterns = [
    # Userauth API Endpoints
    path('user/token/', userauths_views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', userauths_views.RegisterView.as_view(),
         name='auth_register'),
    path('user/password-rest/',
         userauths_views.RegisterView.as_view(), name='auth_register'),
    path('user/password-reset/<email>/',
         userauths_views.PasswordRestEmailVerify.as_view(), name='password_reset'),
    path('user/password-change/',
         userauths_views.PasswordChangeView.as_view(), name='password_change'),

    # Store API Endpoints
    path('category/', store_views.CategoryListAPIView.as_view(), name='category'),
    path('products/', store_views.ProductListAPIView.as_view(), name='products'),
    path('products/<slug:slug>/', store_views.ProductDetailAPIView.as_view()),
    path('cart-view/', store_views.CartAPIView.as_view(), name='cart-view'),
    # path('cart-view/', store_views.CartApiView.as_view(), name='cart-view'),
]
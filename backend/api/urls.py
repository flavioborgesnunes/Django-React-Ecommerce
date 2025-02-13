from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from store import views as store_views
from userauths import views as userauths_views

urlpatterns = [
    path('user/token/', userauths_views.MyTokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
    path('user/register/', userauths_views.RegisterView.as_view()),
    path('user/password-reset/<email>/',
         userauths_views.PasswordResetEmailVerify.as_view()),
    path('user/password-change/',
         userauths_views.PasswordChangeView.as_view()),

    # Stores Endpoints

    path('category/', store_views.CategoryListAPIView.as_view()),
    path('products/', store_views.ProductAPIView.as_view()),
    path('products/<slug>/', store_views.ProductDetailAPIView.as_view()),
]

from django.urls import path, include
from users import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('users/create/', views.UserViewset.as_view({'post': 'create_user'})),
    path('users/verify/', views.UserViewset.as_view({'post': 'verify_user'})),
    path('users/create_token/', views.UserViewset.as_view({'post': 'create_token'})),
    path('users/verify_token/', views.UserViewset.as_view({'post': 'verify_token'})),
    path('auth/', include('djoser.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
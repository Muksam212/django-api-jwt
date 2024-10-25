from django.urls import path
from .import views

urlpatterns = [
    path('api/user/register/', views.UserRegisterAPIView.as_view(), name = 'api-user-register'),
    path('api/user/list/', views.UserListView.as_view(), name = 'api-user-list'),
    path('api/user/login/', views.UserLoginView.as_view(), name = 'api-user-login'),
    path('api/user/profile/view/', views.UserProfileView.as_view(), name = 'api-user-view'),
    path('api/user/password/reset/', views.UserPasswordResetView.as_view(), name = 'api-user-password-reset')
]

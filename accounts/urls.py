from django.urls import path
from .views import (
    RegistrationView,
    ProfileView,
    UserDetailView,
    FollowToggleView,
)

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/',      ProfileView.as_view(),      name='profile'),
    path('users/<str:username>/',               UserDetailView.as_view(),    name='user-detail'),
    path('users/<str:username>/follow-toggle/', FollowToggleView.as_view(), name='follow-toggle'),
]

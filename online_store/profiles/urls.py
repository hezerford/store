from django.urls import path
from .views import ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('profile/<str:username>', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/edit/<str:username>', ProfileUpdateView.as_view(), name='profile-update'),
]
from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/edit/<int:pk>', ProfileUpdateView.as_view(), name='profile-update'),
]

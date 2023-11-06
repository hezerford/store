from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/edit/<int:pk>', ProfileUpdateView.as_view(), name='profile-update'),
]
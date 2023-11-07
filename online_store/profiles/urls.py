from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<str:username>', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/edit/<str:username>', ProfileUpdateView.as_view(), name='profile-update'),
]
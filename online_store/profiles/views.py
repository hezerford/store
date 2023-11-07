import profile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.views.generic import TemplateView, UpdateView
from django.urls import reverse, reverse_lazy

from profiles.forms import UserProfileForm
from .models import UserProfile

class ProfileDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/detail.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        context["user_profile"] = user_profile
        return context
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'profiles/update.html'
    context_object_name = 'user_profile'
    form_class = UserProfileForm
    success_url = '/profile/'

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        return self.request.user.userprofile # Обращаемся к текущему пользователю

    def get_success_url(self):
        username = self.request.user.username
        return reverse('profile-detail', kwargs={'username': self.request.user.username})
    
    def form_valid(self, form):
        profile_picture = self.request.FILES.get('profile_picture')
        if profile_picture:
            self.object.profile_picture = profile_picture

        if 'reset_profile_picture' in self.request.POST:
            user_profile = self.request.user.userprofile
            if user_profile.profile_picture:
                # Удалить фотографию профиля и установить значение profile_picture в None
                user_profile.profile_picture.delete()
                user_profile.profile_picture = None
                user_profile.save()  # Сохраняем модель профиля

        return super().form_valid(form)
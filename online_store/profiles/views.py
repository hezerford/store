import profile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse, reverse_lazy

from profiles.forms import UserProfileForm
from .models import UserProfile

class ProfileDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/detail.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context["user_profile"] = user_profile
        return context
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'profiles/update.html'
    context_object_name = 'user_profile'
    form_class = UserProfileForm
    success_url = '/profile/'

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse('profile-detail', args=[user_id])
    
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
                user_profile.save()
                messages.success(self.request, "Profile picture has been reset to default.")

        return super().form_valid(form)
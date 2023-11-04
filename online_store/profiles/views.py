from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
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
    fields = ['first_name', 'last_name', 'address', 'phone_number']
    success_url = reverse_lazy('profile-detail')

    def get_object(self, queryset=None):
        return self.request.user.userprofile
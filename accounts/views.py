from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .models import UserProfile


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = AuthenticationForm
    
    def get_success_url(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return reverse('admin:index')
        else:
            return reverse('weatherwise:home')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to WeatherWise!')
            return redirect('weatherwise:home')
        else:
            # Show first error only
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
                    break
                break
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})
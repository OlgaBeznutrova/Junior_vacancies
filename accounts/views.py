from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect

from django.contrib.auth import login

from django.views.generic import CreateView

from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages


class UserRegisterView(UserPassesTestMixin, CreateView):
    form_class = UserRegisterForm
    template_name = "accounts/register_form.html"

    def test_func(self):
        return self.request.user.is_anonymous

    def handle_no_permission(self):
        messages.warning(self.request, "Вы являетесь зарегистрированным пользователем")
        return redirect("lets_start")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Вы успешно зарегистрировались!")
        return redirect("lets_start")


class UserLoginView(LoginView):
    template_name = "accounts/login_form.html"
    form_class = UserLoginForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = "home_page"

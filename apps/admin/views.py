from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import redirect
from apps.admin.forms import AdminLoginForm
from django.contrib import messages
from .decorators import admin_required
from django.views.decorators.csrf import csrf_exempt


def admin_logout_view(request):
    logout(request)

    return redirect('admin:admin-login')


class AdminLoginView(View):
    template_name = 'admin_login.html'
    form_class = AdminLoginForm

    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('')

        return render(request, self.template_name)

    def post(self, request):
        login_form = self.form_class(request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password']
            )
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('admin:dashboards')
                else:
                    messages.error(request, 'Permission Denied !')
            else:
                messages.error(request, 'Username or Password Invalid')

        else:
            messages.error(request, 'Username or Password Invalid')

        return redirect(reverse('admin:admin-login'))


class AdminDashboardView(View):
    template_name = 'dashboard.html'

    @method_decorator(admin_required)
    def get(self, request):
        return render(request, self.template_name)

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.shortcuts import redirect, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.utils.decorators import method_decorator
from apps.admin.decorators import admin_required


class UserListView(View):
    template_name = 'list_user.html'
    paginate = 10

    @method_decorator(admin_required)
    def get(self, request):
        users = User.objects.order_by('-id')
        paginator = Paginator(users, self.paginate)

        page = request.GET.get('page')
        users_object = paginator.get_page(page)

        context = {
            'users': users_object,
        }
        return render(request, self.template_name, context)


class DetailUser(View):
    template_name = 'detail_user.html'

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, pk=user_id)
        context = {
            'user': user,
        }
        return render(request, self.template_name, context)


class EditUser(View):
    template_name = 'edit_user.html'

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, pk=user_id)
        context = {
            'user': user,
        }
        return render(request, self.template_name, context)

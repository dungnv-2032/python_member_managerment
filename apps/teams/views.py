from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.shortcuts import redirect, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Team
from django.utils.decorators import method_decorator
from apps.admin.decorators import admin_required
from .forms import AddTeamForm
from django.contrib import messages
from apps.users.models import User


class TeamListView(View):
    template_name = 'list_team.html'
    paginate = 10

    @method_decorator(admin_required)
    def get(self, request):
        teams = Team.objects.order_by('-id')
        paginator = Paginator(teams, self.paginate)

        page = request.GET.get('page')
        teams_object = paginator.get_page(page)

        context = {
            'teams': teams_object,
        }
        return render(request, self.template_name, context)


class AddTeamView(View):
    template_name = 'add_team.html'
    form_class = AddTeamForm

    @method_decorator(admin_required)
    def get(self, request):
        users_in_team = Team.objects.select_related('team_user').values_list('user__team_user__user', flat=True)
        users = User.objects.exclude(id__in=users_in_team)
        context = {
            'users': users
        }
        return render(request, self.template_name, context)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        add_team_form = self.form_class(request.POST)
        if add_team_form.is_valid():

            Team.objects.create(
                name=request.POST['name'],
                description=request.POST['description'],
                leader=request.POST['leader']
            )

            return redirect('admin:teams:team-list')
        users_in_team = Team.objects.select_related('team_user').values_list('user__team_user__user', flat=True)
        users = User.objects.exclude(id__in=users_in_team)
        context = {
            'form': add_team_form,
            'users': users,
        }
        return render(request, self.template_name, context)


class EditTeamView(View):
    template_name = 'edit_team.html'
    form_class = AddTeamForm

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        team_id = kwargs.get('id')
        team = get_object_or_404(Team, pk=team_id)

        context = {
            'team': team,
        }
        return render(request, self.template_name, context)

    @method_decorator(admin_required)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        team_id = request.POST['id']
        team = get_object_or_404(Team, pk=team_id)
        form = self.form_class(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update Team Success !')
        else:
            return render(request, self.template_name, {'form': form})

        return redirect(reverse('admin:teams:team-edit', kwargs={'id': team_id}))


class DeleteTeamView(View):
    method_decorator(admin_required)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        team_id = request.POST['id']
        team = get_object_or_404(Team, pk=team_id)
        team.delete()
        response = {
            'code': 'success',
        }
        return JsonResponse(response)

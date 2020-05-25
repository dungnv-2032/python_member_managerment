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
        users = User.objects.raw(
            'SELECT * FROM user where user.id not in '
            '(SELECT user_team.user_id as id from user_team group  by user_id)'
        )
        context = {
            'users': users
        }
        return render(request, self.template_name, context)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        add_team_form = self.form_class(request.POST)
        if add_team_form.is_valid():

            team = Team.objects.create(
                name=request.POST['name'],
                description=request.POST['description'],
                leader_id=request.POST['leader_id']
            )

            if request.POST['member']:
                for member in request.POST.getlist('member'):
                    team.team_user.add(member)

            return redirect('admin:teams:team-list')

        users = User.objects.raw(
            'SELECT * FROM user where user.id not in '
            '(SELECT user_team.user_id as id from user_team group  by user_id)'
        )

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

        users = User.objects.raw(
            'SELECT * FROM user where user.id not in '
            '(SELECT user_team.user_id as id from user_team group  by user_id)'
        )
        members = User.objects.raw(
            'SELECT * FROM user where user.id in '
            '(SELECT user_team.user_id as id from user_team group by user_id)'
        )
        leader = User.objects.filter(id=team.leader_id).get()
        context = {
            'team': team,
            'users': users,
            'members': members,
            'leader': leader,
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
            if request.POST.getlist('member'):
                team.team_user.clear()
                for member in request.POST.getlist('member'):
                    user = User.objects.get(id=member)
                    team.team_user.add(user)
            else:
                team.team_user.clear()
            messages.success(request, 'Update Team Success !')
        else:
            users = User.objects.raw(
                'SELECT * FROM user where user.id not in '
                '(SELECT user_team.user_id as id from user_team group  by user_id)'
            )

            leader = User.objects.filter(id=team.leader_id).get()
            context = {
                'team': team,
                'users': users,
                'form': form,
                'leader': leader,
            }
            return render(request, self.template_name, context)

        return redirect(reverse('admin:teams:team-edit', kwargs={'id': team_id}))


class DeleteTeamView(View):
    method_decorator(admin_required)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        team_id = request.POST['id']
        team = get_object_or_404(Team, pk=team_id)
        team.team_user.clear()
        team.delete()
        response = {
            'code': 'success',
        }
        return JsonResponse(response)

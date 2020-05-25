from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.shortcuts import redirect, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Skill
from django.utils.decorators import method_decorator
from apps.admin.decorators import admin_required
from .forms import AddSkillForm
from django.contrib import messages


class SkillListView(View):
    template_name = 'list_skill.html'
    paginate = 10

    @method_decorator(admin_required)
    def get(self, request):
        skills = Skill.objects.order_by('-id')
        paginator = Paginator(skills, self.paginate)

        page = request.GET.get('page')
        users_object = paginator.get_page(page)

        context = {
            'skills': users_object,
        }
        return render(request, self.template_name, context)


class AddSkillView(View):
    template_name = 'add_skill.html'
    form_class = AddSkillForm

    @method_decorator(admin_required)
    def get(self, request):
        return render(request, self.template_name)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        add_skill_form = self.form_class(request.POST)
        if add_skill_form.is_valid():

            Skill.objects.create(
                name=request.POST['name'],
                level=request.POST['level'],
                used_year_number=request.POST['used_year_number']
            )

            return redirect('admin:skills:skill-list')
        return render(request, self.template_name, {'form': add_skill_form})


class EditSkillView(View):
    template_name = 'edit_skill.html'
    form_class = AddSkillForm

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        skill_id = kwargs.get('id')
        skill = get_object_or_404(Skill, pk=skill_id)

        context = {
            'skill': skill,
        }
        return render(request, self.template_name, context)

    @method_decorator(admin_required)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        skill_id = request.POST['id']
        skill = get_object_or_404(Skill, pk=skill_id)
        form = self.form_class(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update Skill Success !')
        else:
            return render(request, self.template_name, {'form': form})

        return redirect(reverse('admin:skills:skill-edit', kwargs={'id': skill_id}))


class DeleteSkillView(View):
    method_decorator(admin_required)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        skill_id = request.POST['id']
        skill = get_object_or_404(Skill, pk=skill_id)
        skill.delete()
        response = {
            'code': 'success',
        }
        return JsonResponse(response)

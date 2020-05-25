from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.shortcuts import redirect, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Position
from django.utils.decorators import method_decorator
from apps.admin.decorators import admin_required
from .forms import AddPositionForm
from django.contrib import messages


class PositionListView(View):
    template_name = 'list_position.html'
    paginate = 10

    @method_decorator(admin_required)
    def get(self, request):
        paginator = Paginator(Position.objects.order_by('-id'), self.paginate)

        page = request.GET.get('page')
        positions_object = paginator.get_page(page)

        context = {
            'positions': positions_object,
        }
        return render(request, self.template_name, context)


class AddPositionView(View):
    template_name = 'add_position.html'
    form_class = AddPositionForm

    @method_decorator(admin_required)
    def get(self, request):
        return render(request, self.template_name)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        add_position_form = self.form_class(request.POST)
        if add_position_form.is_valid():

            Position.objects.create(
                name=request.POST['name'],
                abbreviation=request.POST['abbreviation'],
            )

            return redirect('admin:positions:position-list')
        return render(request, self.template_name, {'form': add_position_form})


class EditPositionView(View):
    template_name = 'edit_position.html'
    form_class = AddPositionForm

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        position_id = kwargs.get('id')
        position = get_object_or_404(Position, pk=position_id)

        context = {
            'position': position,
        }
        return render(request, self.template_name, context)

    @method_decorator(admin_required)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        position_id = request.POST['id']
        position = get_object_or_404(Position, pk=position_id)
        form = self.form_class(request.POST, instance=position)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update Position Success !')
        else:
            return render(request, self.template_name, {'form': form})

        return redirect(reverse('admin:positions:position-edit', kwargs={'id': position_id}))


class DeletePositionView(View):
    method_decorator(admin_required)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        position_id = request.POST['id']
        position = get_object_or_404(Position, pk=position_id)
        position.delete()
        response = {
            'code': 'success',
        }
        return JsonResponse(response)

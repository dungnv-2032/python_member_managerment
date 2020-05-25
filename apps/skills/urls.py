from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views as auth_views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'skills'

urlpatterns = [
    path('', auth_views.SkillListView.as_view(), name='skill-list'),
    path('add/', auth_views.AddSkillView.as_view(), name='skill-add'),
    path('edit/<int:id>/', auth_views.EditSkillView.as_view(), name='skill-edit'),
    path('delete/', auth_views.DeleteSkillView.as_view(), name='skill-delete'),
]

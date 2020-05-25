from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views as auth_views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'teams'

urlpatterns = [
    path('', auth_views.TeamListView.as_view(), name='team-list'),
    path('add/', auth_views.AddTeamView.as_view(), name='team-add'),
    path('edit/<int:id>/', auth_views.EditTeamView.as_view(), name='team-edit'),
    path('delete/', auth_views.DeleteTeamView.as_view(), name='team-delete'),
]

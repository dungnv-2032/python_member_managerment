from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views as auth_views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'admin'

urlpatterns = [
    path('login/', auth_views.AdminLoginView.as_view(), name='admin-login'),
    path('dashboards/', auth_views.AdminDashboardView.as_view(), name='dashboards'),
    path('users/', include('apps.users.urls')),
    path('skills/', include('apps.skills.urls')),
    path('positions/', include('apps.positions.urls')),
    path('teams/', include('apps.teams.urls')),

]

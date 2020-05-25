from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views as auth_views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'users'

urlpatterns = [
    path('', auth_views.UserListView.as_view(), name='user-list'),
    path('<int:id>/', auth_views.DetailUser.as_view(), name='user-detail'),
    path('edit/<int:id>/', auth_views.EditUser.as_view(), name='user-edit'),
]


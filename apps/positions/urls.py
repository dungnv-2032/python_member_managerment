from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views as auth_views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'positions'

urlpatterns = [
    path('', auth_views.PositionListView.as_view(), name='position-list'),
    path('add/', auth_views.AddPositionView.as_view(), name='position-add'),
    path('edit/<int:id>/', auth_views.EditPositionView.as_view(), name='position-edit'),
    path('delete/', auth_views.DeletePositionView.as_view(), name='position-delete'),
]

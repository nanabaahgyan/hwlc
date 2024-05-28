from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'contribution'

urlpatterns = [
    path('next-of-kin/', views.member_next_of_kins, name='next_of_kin'),
    path('add/', views.add_next_of_kin, name='next_of_kin_add'),
    path('edit/', views.edit_next_of_kin, name='next_of_kin_edit'),
    path('edit/<uuid>', views.edit_next_of_kin, name='next_of_kin_edit'),
    path('remove/<int:id>', views.remove, name='next_of_kin_remove'),
    path('<type>/', views.member_contributions, name='contribution_type'),
]

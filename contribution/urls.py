from django.urls import path

from . import views

app_name = 'contribution'

urlpatterns = [
    path('next-of-kin/', views.member_next_of_kins, name='next_of_kin'),
    path('<type>/', views.member_contributions, name='contribution_type'),
]

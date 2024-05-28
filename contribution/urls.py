from django.urls import path

from . import views

app_name = 'contribution'

urlpatterns = [
    path('next-of-kin/', views.member_next_of_kins, name='next_of_kin'),
    path('add/', views.add_next_of_kin, name='next_of_kin_add'),
    path('edit/', views.edit_next_of_kin, name='next_of_kin_edit'),
    path('edit/<uuid>', views.edit_next_of_kin, name='next_of_kin_edit'),
    path('remove/<int:id>', views.remove, name='next_of_kin_remove'),
    path('savings/', views.member_savings, name='savings'),
    path('savings/<type>/', views.member_savings, name='savings'),
    path('withdrawal/', views.member_withdrawals, name='withdrawals'),
    path('withdrawal/<type>/', views.member_withdrawals, name='withdrawals'),
]

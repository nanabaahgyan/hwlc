from django.urls import path

from . import views

app_name = 'contribution'

urlpatterns = [
    path('',
         views.member_health_contributions,
         name='health_contribution'),
    # path('<int:id>', views.health_contribution_detail, name='health_detail')
]

from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Savings, Withdrawal
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def member_health_contributions(request, id)
    health_contribution = get_list_or_404(Savings,
                                          type=Savings.Type.HEALTH,
                                          member=id)

    return render(request,
                  'contribution/health/contribution.html',
                  {'health_fund': health_contribution,
                   'section': 'contribution'})


# def health_contribution_detail(request, id):
#     health_contribution = get_object_or_404(Savings,
#                                             id=id,
#                                             type=Savings.Type.HEALTH)

#     return render(request,
#                   'contribution/health/detail.html',
#                   {'health_fund': health_contribution})

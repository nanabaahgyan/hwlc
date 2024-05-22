from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Savings, Withdrawal, NextOfKin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings


# Create your views here.

@login_required
def member_contributions(request, type):
    if type == "health":
        contribution = Savings.objects.filter(member_id=request.user.id)\
                                      .filter(type=Savings.Type.HEALTH)
    elif type == "pension":
        contribution = Savings.objects.filter(member_id=request.user.id)\
                                      .filter(type=Savings.Type.PENSION)

    # pagination with PAGINATOR_COUNT per page
    paginator = Paginator(contribution, settings.PAGINATION_COUNT)
    page_number = request.GET.get('page', 1)
    contributions = paginator.page(page_number)

    return render(request,
                  'contribution/contribution_info.html',
                  {'contributions': contributions,
                   'type': type,
                   'section': 'contribution'})


@login_required
def member_next_of_kins(request):
    next_of_kin = NextOfKin.objects.filter(to_member=request.user.id)

    # pagination with PAGINATOR_COUNT per page
    paginator = Paginator(next_of_kin, settings.PAGINATION_COUNT)
    page_number = request.GET.get('page', 1)
    next_of_kins = paginator.page(page_number)

    return render(request,
                  'contribution/next_of_kin.html',
                  {'next_of_kin': next_of_kins,
                   'section': 'contribution'})

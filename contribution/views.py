from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect

from .models import Savings, Type, Withdrawal, NextOfKin
from .forms import NextOfKinForm

# Create your views here.


@login_required
def member_savings(request, type=''):
    if type == "health":
        savings = Savings.objects.filter(member_id=request.user.id)\
            .filter(type=Type.HEALTH)
    elif type == "pension":
        savings = Savings.objects.filter(member_id=request.user.id)\
            .filter(type=Type.PENSION)
    else:
        savings = Savings.objects.filter(member_id=request.user.id)

    # pagination with PAGINATOR_COUNT per page
    paginator = Paginator(savings, settings.PAGINATION_COUNT)
    page_number = request.GET.get('page', 1)
    savings = paginator.page(page_number)

    return render(request,
                  'contribution/savings.html',
                  {'savings': savings,
                   'type': type,
                   'section': 'contribution'})


@login_required
def member_withdrawals(request, type=''):
    if type == "health":
        withdrawal = Withdrawal.objects.filter(member_id=request.user.id)\
            .filter(type=Type.HEALTH).order_by('-withdrawn')
    elif type == "pension":
        withdrawal = Withdrawal.objects.filter(member_id=request.user.id)\
            .filter(type=Type.PENSION).order_by('-withdrawn')
    else:
        withdrawal = Withdrawal.objects.filter(
            member_id=request.user.id).order_by('-withdrawn')

    # pagination with PAGINATOR_COUNT per page
    paginator = Paginator(withdrawal, settings.PAGINATION_COUNT)
    page_number = request.GET.get('page', 1)
    withdrawals = paginator.page(page_number)

    return render(request,
                  'contribution/withdrawal.html',
                  {'withdrawals': withdrawals,
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
                  {'next_of_kins': next_of_kins,
                   'section': 'next-of-kins'})


@login_required
def edit_next_of_kin(request, uuid=None):

    next_of_kin = get_object_or_404(NextOfKin, uuid=uuid)

    if request.method == 'POST':

        next_of_kin_form = NextOfKinForm(instance=next_of_kin,
                                         data=request.POST,
                                         files=request.FILES)

        if next_of_kin_form.is_valid():
            next_of_kin.save()

            messages.success(
                request, f"{next_of_kin.first_name} {next_of_kin.last_name}'s profile updated successfully.")
            HttpResponseRedirect('edit/')
        else:
            messages.error(request, 'Error updating profile of next of kin.')
            HttpResponseRedirect('edit/')
    else:
        next_of_kin_form = NextOfKinForm(instance=next_of_kin)

    return render(request,
                  'contribution/next_of_kin_edit.html',
                  {'next_of_kin_form': next_of_kin_form,
                   'next_of_kin': next_of_kin})


@ login_required
def add_next_of_kin(request):
    if request.method == 'POST':
        user = get_object_or_404(get_user_model(), id=request.user.id)

        next_of_kin = None

        next_of_kin_form = NextOfKinForm(
            data=request.POST,
            files=request.FILES)

        if next_of_kin_form.is_valid():

            # get cleaned data
            cd = next_of_kin_form.cleaned_data

            # create a new form object but avoid saving it yet
            next_of_kin = next_of_kin_form.save(commit=False)

            # add member_id
            next_of_kin.to_member = user

            # Save the User object
            next_of_kin.save()

            messages.success(
                request, f"{cd['first_name']} {cd['last_name']} added as a next of kin.")
            return redirect('contribution:next_of_kin')
        else:
            messages.error(request, 'Error updating profile of next of kin.')
            HttpResponseRedirect('add/')
    else:
        next_of_kin_form = NextOfKinForm(
            initial={'to_member': request.user.pk})

    return render(request,
                  'contribution/next_of_kin_edit.html',
                  {'next_of_kin_form': next_of_kin_form,
                   'section': 'next-of-kins'})


@ login_required
def remove(request, id):
    try:
        next_of_kin = NextOfKin.objects.get(pk=id)

        next_of_kin.delete()

        message = f'{next_of_kin.first_name} {next_of_kin.last_name}\
          successfully removed from next of kin.'
        messages.success(request, message)
    except:
        message = "Sorry. Something went wrong. Please try again."
        messages.error(request, message)

    return redirect('contribution:next_of_kin')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.db import transaction


from .forms import UserEditForm, ProfileEditForm
from .models import UserProfile

# Create your views here.


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


@login_required
@transaction.atomic
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.user_profile,
                                       data=request.POST,
                                       files=request.FILES
                                       )
        if user_form.is_valid and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        try:
            profile_form = ProfileEditForm(instance=request.user.user_profile)
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=request.user)
            profile_form = ProfileEditForm(instance=request.user.user_profile)

    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})

from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import SignUpForm,User_form,Profile_form
from .models import Profile
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
# Create your views here.

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def myProfile(request,user_id):
    my_details =  Profile.objects.all().filter(user_id=user_id)
    return render(request=request,
                  template_name="userApp/my_profile.html",
                  context={"my_details":my_details}
                  )


def editProfile(request,user_id):
    user = get_object_or_404(User,id=user_id)
    if request.method == 'POST':
        user_form =User_form(request.POST, instance=user)
        profile_form = Profile_form(request.POSR or None,request.FILES or None ,instance =user)
        if user_form.is_valid() and Profile_form.is_valid():
            user_form.save()
            profile_form.save()
            if profile_form.cleaned_data['staff']:
                user.is_staff = True
                user.save()
            else:
                user.is_staff = False
                user.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return myProfile(request,user_id)
        else:
            messages.error(request('Please correct the error below.')) 
            return HttpResponsePermanentRedirect(reverse('edit_profile',args=(user_id,)))
    else:
        user_form = User_form(instance=user)
        profile_form = Profile_form(instance=user.profile)
    return render(request, 'userApp/edit_profile_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def deactivate(request,user_id):
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = 0
    else:
        user.is_active = 1
    user.save()
    return myProfile(request,user_id)
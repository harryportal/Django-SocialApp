import requests
from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm, EditUser, EditProfile
from django.contrib.auth.decorators import login_required
from .models import Profile, Contact
from django.contrib import messages
from django.contrib.auth.models import User
from .common.decorators import ajax_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from action.utils import create_action
from action.models import action
# This has been replaced with django's authentication view
"""
def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password= cd['password'])
            if user is not None:
                if user.is_active():
                    login(request, user)
                    return HttpResponse('User Authenticated, Login Successful')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
        else:
            return HttpResponse('Invalid form submission, check form and try again')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form':form})
"""


@login_required
def dashboard(request):
    #get all actions by default
    actions = action.objects.exclude(user=request.user)
    # get the id of everyone the user is following
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # retrieve actions of only those the user follows
        actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'actions':actions})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])  # using set_password handles hashing
            new_user.save()
            create_action(user=new_user, verb='registers a new account')
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
        else:
            pass
    else:
        form = UserRegistrationForm()
        return render(request, 'account/register.html', {'form': form})


@login_required
def edit_account(request):
    if request.method == 'POST':
        user_edit_form = EditUser(instance=request.user, data=request.POST)
        profile_edit_form = EditProfile(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_edit_form.is_valid() and profile_edit_form.is_valid():
            user_edit_form.save()
            profile_edit_form.save()
            messages.success(request, 'Account updated successfully')
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            messages.error(request, 'Account could not be updated')
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        user_form = EditUser(instance=request.user)
        try:  # in the case account created using google or facebook sign in
            profile_form = EditProfile(instance=request.user.profile)
        except:
            profile_form = EditProfile()
        context = {'user_form': user_form, 'profile_form': profile_form, 'section': 'profile'}
        return render(request, 'account/edit_account.html', context)


# returns a list of users on the social app
@login_required
def users_list(request):
    users = User.objects.filter(is_active=True).all()
    return render(request, 'users/userlist.html', {'section': 'people', 'users': users})


# returns the detail of the user specified
def get_user(request, username):
    user = get_object_or_404(User, is_active=True, username=username)
    context = {'user': user, 'section': 'people'}
    return render(request, 'users/userdetail.html')


@ajax_required
@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(pk=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
                create_action(request.user, 'follows', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})



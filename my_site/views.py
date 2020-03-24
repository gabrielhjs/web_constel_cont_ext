from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import FormLogin


def view_login(request):

    next_page = request.GET.get('next', None)

    if request.user.is_authenticated:
        return HttpResponseRedirect('/psw/login/')

    else:

        if request.method == 'POST':
            form = FormLogin(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)

                    if next_page is not None:
                        return HttpResponseRedirect(next_page)

                    return HttpResponseRedirect('/psw/login/')

        else:
            form = FormLogin()

        context = {
            'form': form,
        }

        return render(request, 'my_site/login.html', context)


@login_required
def view_logout(request):

    logout(request)

    return HttpResponseRedirect('/login/')

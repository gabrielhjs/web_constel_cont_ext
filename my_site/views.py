from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import FormLogin
from .objects import Button


def view_login(request):

    next_page = request.GET.get('next', None)

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

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

                    return HttpResponseRedirect('/')

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


@login_required
def view_menu_principal(request):

    button_1 = Button('psw_login', 'Realizar baixa de Ont no sistema')
    button_logout = Button('logout', 'Logout')

    context = {
        'buttons': [
            button_1,
        ],
        'guia_titulo': 'Cont2WE',
        'pagina_titulo': 'Cont2WE',
        'menu_titulo': 'Menu principal',
        'rollback': button_logout,
    }

    return render(request, 'my_site/menu.html', context)

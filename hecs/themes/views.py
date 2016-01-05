from django.shortcuts import render, get_object_or_404, redirect
from .models import Theme, Reference
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import SignupForm, LoginForm
from django.db import IntegrityError

HOMEPAGE_ROWS = 10
HOMEPAGE_COLS = 16

def home_page(request):
    themes = Theme.objects.all()
    rows = [[row, [[col, None] for col in range(HOMEPAGE_COLS)]] for row in range(HOMEPAGE_ROWS)]
    for theme in themes:
        try:
            rows[theme.x][1][theme.y][1] = theme
        except IndexError:
            pass
    return render(request, 'homepage.html', {'rows': rows})


def theme_page(request, theme_id):
    theme = get_object_or_404(Theme, pk=theme_id)
    references = list(Reference.objects.filter(theme=theme).all())
    groups = {}
    for reference in references:
        if reference.group.name not in groups.keys():
            groups[reference.group.name] = []
        groups[reference.group.name].append(reference)


    return render(request, 'theme.html', {'name': theme.name,
                                          'groups': sorted(groups.items(), key=lambda x: x[0])})


def signup_page(request):
    if request.user.is_authenticated():
        return redirect('/home')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        try:
            user = User.objects.create_user(form.data['login'], password=form.data['password'], first_name=form.data['firstname'], last_name=form.data['lastname'])
            user.save()
        except IntegrityError:
            return redirect('/signup?login_used')
        user = authenticate(username=form.data['login'], password=form.data['password'])
        login(request, user)
        return redirect('/home')
    else:
        return render(request, 'signup_form.html', {'login_used': 'login_used' in request.GET})
    
def login_page(request):
    if request.user.is_authenticated():
        return redirect('/home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = authenticate(username=form.data['login'], password=form.data['password'])
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            return redirect('/login?login_error')
    else:
        return render(request, 'login_form.html', {'login_error': 'login_error' in request.GET})
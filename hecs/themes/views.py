from django.shortcuts import render, get_object_or_404, redirect
from .models import Theme, Reference, Blank
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm, SettingsForm, BlankForm
from django.db import IntegrityError

HOMEPAGE_ROWS = 10
HOMEPAGE_COLS = 16

def home_page(request):
    auth_user = request.user
    if not auth_user.is_authenticated():
        auth_user = None
    themes = Theme.objects.all()
    rows = [[row, [[col, None] for col in range(HOMEPAGE_COLS)]] for row in range(HOMEPAGE_ROWS)]
    for theme in themes:
        try:
            rows[theme.x][1][theme.y][1] = theme
        except IndexError:
            pass
    rows[0][1] = rows[0][1][2:]
    return render(request, 'homepage.html', {'rows': rows, 'auth_user': auth_user})


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


def profile_page(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    top_string = user.username
    if user.first_name != "" or user.last_name != "":
        top_string += " (" + user.last_name + (" " if user.last_name != "" and user.first_name != "" else "") + user.first_name + ")"
    return render(request, 'profile.html', {'user': user, 'me': user == request.user,   
                                            'top_string': top_string})

def signup_page(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if not (form.data['login'] and form.data['password'] and form.data['password_1'] and form.data['firstname'] and form.data['lastname']):
            return redirect('/signup?missing')
        try:
            user = User.objects.create_user(form.data['login'], password=form.data['password'], first_name=form.data['firstname'], last_name=form.data['lastname'])
            user.save()
        except IntegrityError:
            return redirect('/signup?login_used')
        if form.data['password'] != form.data['password_1']:
            return redirect('/signup?passwords_not_match')
        user = authenticate(username=form.data['login'], password=form.data['password'])
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'signup_form.html', {'login_used': 'login_used' in request.GET, 'missing': 'missing' in request.GET, 'passwords_not_match': 'passwords_not_match' in request.GET})
    
def login_page(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = authenticate(username=form.data['login'], password=form.data['password'])
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login?login_error')
    else:
        return render(request, 'login_form.html', {'login_error': 'login_error' in request.GET})
    
def logout_page(request):
    logout(request)
    return redirect('/')

def settings_page(request):
    if not request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if not (form.data['firstname'] and form.data['lastname']):
            return redirect('/settings?missing')
        request.user.first_name = form.data['firstname']
        request.user.last_name = form.data['lastname']
        request.user.save()
        if form.data['password']:
            request.user.set_password(form.data['password'])
            request.user.save()
            user = authenticate(username=request.user.username, password=form.data['password'])
            login(request, user)
        return redirect('/profile/' + str(request.user.id))
    else:
        return render(request, 'settings_form.html', {'user': request.user, 'missing': 'missing' in request.GET})

def blank_page(request):
    user = request.user
    themes = list(Theme.objects.all())
    forms = list(Blank.objects.filter(user=user).all())

    if request.method == 'POST':
        form = BlankForm(request.POST)

        for theme in themes:
            try:
                blank = get_object_or_404(Blank, user=user, theme=theme)
            except Exception:
                blank = Blank()
                blank.user = user
                blank.theme = theme
            blank.result = form.data[theme.name]
            blank.save()

        return redirect('/')

    marks = []

    for form in forms:
        mark = (form.theme.name, form.result)
        marks.append(mark)
        themes.remove(form.theme)

    for theme in themes:
        mark = (theme.name, '')
        marks.append(mark)

    marks.sort()
    return render(request, 'blank.html', {'marks': marks,
                                          'lst': ['', '1', '2', '3', '4', '5'],
                                          'id': user.id})

from django.shortcuts import render, get_object_or_404
from .models import Theme, Reference
from django.contrib.auth.models import User

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


def profile_page(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    top_string = user.username
    if user.first_name != "" or user.last_name != "":
        top_string += " (" + user.last_name + (" " if user.last_name != "" and user.first_name != "" else "") + user.first_name + ")"
    return render(request, 'profile.html', {'user': user,
                                            'top_string': top_string})


from django.shortcuts import render
from .models import Theme

HOMEPAGE_ROWS = 10
HOMEPAGE_COLS = 16

def home_page(request):
    themes = Theme.objects.all()
    rows = [[row, [[col, None] for col in range(HOMEPAGE_COLS)]] for row in range(HOMEPAGE_ROWS)]
    for theme in themes:
        try:
            print (theme.x, theme.y)
            rows[theme.x][1][theme.y][1] = theme
        except IndexError:
            pass
    return render(request, 'homepage.html', {'rows': rows})

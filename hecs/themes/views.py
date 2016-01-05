from django.shortcuts import render, get_object_or_404
from .models import Theme, Reference


def theme_page(request, theme_id):
    theme = get_object_or_404(Theme, pk=theme_id)
    references = list(Reference.objects.filter(theme=theme))
    groups = {}
    for reference in references:
        if reference.group not in groups.keys():
            groups[reference.group.name] = []
        groups[reference.group.name].append(reference)

    return render(request, 'theme.html', {'name': theme.name,
                                          'groups': sorted(groups.items(), key=lambda x: (x[0], x[1].target.name))})


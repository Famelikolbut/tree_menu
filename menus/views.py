from django.shortcuts import render


def page(request):
    return render(request, 'page.html', {
        'current_path': request.path
    })
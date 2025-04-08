from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {'current_page': 'home'})

def about(request):
    return render(request, 'about.html', {'current_page': 'about'})

def contact(request):
    return render(request, 'contact.html', {'current_page': 'contact'})

def service(request):
    return render(request, 'service.html', {'current_page': 'services'})


def starter(request):
    return render(request,'starter-page.html')
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact

def index(request):
    return render(request, 'index.html', {'current_page': 'home'})

def about(request):
    return render(request, 'about.html', {'current_page': 'about'})

def contact(request):
    if request.method == 'POST':
        Contact.objects.create(
            name=request.POST['name'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message']
        )
        messages.success(request, "Your message has been received. We'll get back to you soon.")
        return redirect('contact')
    return render(request, 'contact.html', {'current_page': 'contact'})

def service(request):
    return render(request, 'service.html', {'current_page': 'services'})


def starter(request):
    return render(request,'starter-page.html')
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact, Payment
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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

def paypal_page(request):
    return render(request, 'paypal_payment.html', { 'current_page': 'services'})

def receipt(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    return render(request, 'receipt.html', {'payment': payment})

@csrf_exempt
def paypal_capture(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        order_id = data.get('orderID')
        payer_id = data.get('payerID')
        details = data.get('details')

        # Save the payment details to your database
        payment = Payment.objects.create(
            order_id=order_id,
            payer_id=payer_id,
            status='Completed',
            amount=details['purchase_units'][0]['amount']['value'],
            payer_name=details['payer']['name']['given_name'],
        )

        return JsonResponse({"status": "success", "id": payment.id})
    return JsonResponse({"status": "failed"}, status=400)

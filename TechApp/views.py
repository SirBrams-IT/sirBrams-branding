import logging
import os  
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact, PortfolioItem
from .content import SITE, ANNOUNCEMENT, STATS
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from django.utils.html import strip_tags
from django.template.loader import render_to_string
 

logger = logging.getLogger(__name__)

def page_context(page, **extra):
    """Shared context for every page (announcement bar, contact details)."""
    ctx = {
        'current_page': page,
        'site': SITE,
        'announcement': ANNOUNCEMENT,
    }
    ctx.update(extra)
    return ctx


def index(request):
    return render(request, 'index.html', page_context('home', stats=STATS))


def about(request):
    return render(request, 'about.html', page_context('about', stats=STATS))


def portfolio(request):
    # Managed from the admin panel (Portfolio). Only published items appear.
    items = list(PortfolioItem.objects.filter(is_published=True))
    projects = [i for i in items if i.category == PortfolioItem.WEB]
    designs = [i for i in items if i.category == PortfolioItem.DESIGN]
    return render(request, 'portfolio.html', page_context(
        'portfolio', projects=projects, designs=designs, total_count=len(items),
    ))

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not all([name, phone, email, subject, message]):
            messages.error(request, "Please fill in all the fields.")
            return redirect('contact')

        try:
            mycontact = Contact.objects.create(
                name=name,
                phone=phone,
                email=email,
                subject=subject,
                message=message
            )

            logger.info(f"✅ Contact saved: {mycontact.id}")

            current_time = timezone.localtime(
                timezone.now()
            ).strftime("%d-%m-%Y at %I:%M %p")

            # Admin email
            admin_context = {
                'name': name,
                'phone': phone,
                'email': email,
                'subject': subject,
                'message': message,
                'current_time': current_time,
            }
            
            admin_html = render_to_string('email/admin.html', admin_context)
            admin_text = strip_tags(admin_html)
            
            admin_email = EmailMultiAlternatives(
                f"New Enquiry: {subject}",
                admin_text,
                settings.DEFAULT_FROM_EMAIL,
                ['sirbrams.b@gmail.com']
            )
            admin_email.attach_alternative(admin_html, "text/html")
            admin_email.send()

            logger.info("📧 Admin email sent")

            # Client auto-reply
            client_context = {
                'name': name,
                'message': message,
            }
            
            client_html = render_to_string('email/client.html', client_context)
            client_text = strip_tags(client_html)
            
            client_email = EmailMultiAlternatives(
                "Thank you for contacting SirBrams Tech Solutions",
                client_text,
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            client_email.attach_alternative(client_html, "text/html")
            client_email.send()

            logger.info(f"📧 Auto-reply sent to {email}")

            messages.success(
                request,
                "Your message has been sent successfully. Please check your email for confirmation."
            )

        except Exception as e:
            logger.error(f"❌ Contact failed: {str(e)}", exc_info=True)
            messages.error(request, "Something went wrong. Please try again later.")

        return redirect('contact')

    return render(request, 'contact.html', page_context('contact'))


def service(request):
    return render(request, 'service.html', page_context('services'))


def main(request):
    return render(request, 'main.html', page_context('home'))
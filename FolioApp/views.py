import logging
import os  
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from django.utils.html import strip_tags
 

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html', {'current_page': 'home'})

def about(request):
    return render(request, 'about.html', {'current_page': 'about'})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        # Validate required fields
        if not all([name, phone, email, subject, message]):
            messages.error(request, "Please fill in all the fields.")
            return redirect('contact')

        try:
            # 1. SAVE TO DATABASE
            mycontact = Contact.objects.create(
                name=name,
                phone=phone,
                email=email,
                subject=subject,
                message=message
            )

            logger.info(f"✅ Contact saved successfully: {mycontact.id}")

            # Get current Nairobi time
            current_time = timezone.localtime(
                timezone.now()
            ).strftime("%d-%m-%Y at %I:%M %p")

            # ============================================================
            # 2. SEND MODERN HTML EMAIL NOTIFICATION TO ADMIN
            # ============================================================

            admin_subject = f"New Website Enquiry: {subject}"

            admin_html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>New Website Enquiry</title>
            </head>

            <body style="
                margin:0;
                padding:0;
                background:#f1f5f9;
                font-family:Arial, Helvetica, sans-serif;
                color:#1e293b;
            ">

                <div style="
                    width:100%;
                    padding:40px 15px;
                    box-sizing:border-box;
                ">

                    <div style="
                        max-width:650px;
                        margin:0 auto;
                        background:#ffffff;
                        border-radius:18px;
                        overflow:hidden;
                        box-shadow:0 8px 30px rgba(15,23,42,0.08);
                    ">

                        <!-- HEADER -->
                        <div style="
                            background:linear-gradient(135deg,#0f172a,#1e3a8a);
                            padding:35px 30px;
                            text-align:center;
                        ">

                            <img
                                src="https://res.cloudinary.com/dbkuxm0jo/image/upload/v1759413687/profile_images/ztqvzdv1ajimw4894t7h.png"
                                alt="SirBrams Logo"
                                style="
                                    height:60px;
                                    width:auto;
                                    margin-bottom:20px;
                                "
                            >

                            <div style="
                                color:#93c5fd;
                                font-size:13px;
                                font-weight:bold;
                                letter-spacing:1.5px;
                                text-transform:uppercase;
                            ">
                                Website Notification
                            </div>

                            <h1 style="
                                margin:8px 0 0;
                                color:#ffffff;
                                font-size:26px;
                                line-height:1.3;
                            ">
                                New Contact Enquiry
                            </h1>

                        </div>


                        <!-- CONTENT -->
                        <div style="padding:35px 30px;">

                            <p style="
                                margin:0 0 25px;
                                color:#475569;
                                font-size:15px;
                                line-height:1.7;
                            ">
                                You have received a new enquiry through the
                                <strong style="color:#1e3a8a;">
                                    SirBrams Tech Virtual Campus
                                </strong>
                                website.
                            </p>


                            <!-- CONTACT DETAILS -->
                            <div style="
                                border:1px solid #e2e8f0;
                                border-radius:14px;
                                overflow:hidden;
                                margin-bottom:25px;
                            ">

                                <div style="
                                    background:#f8fafc;
                                    padding:16px 20px;
                                    border-bottom:1px solid #e2e8f0;
                                ">
                                    <h3 style="
                                        margin:0;
                                        color:#0f172a;
                                        font-size:16px;
                                    ">
                                        👤 Contact Details
                                    </h3>
                                </div>

                                <div style="padding:10px 20px;">

                                    <table style="
                                        width:100%;
                                        border-collapse:collapse;
                                    ">

                                        <tr>
                                            <td style="
                                                padding:13px 0;
                                                color:#64748b;
                                                font-size:14px;
                                                width:32%;
                                            ">
                                                Name
                                            </td>

                                            <td style="
                                                padding:13px 0;
                                                color:#0f172a;
                                                font-size:14px;
                                                font-weight:bold;
                                            ">
                                                {name}
                                            </td>
                                        </tr>


                                        <tr>
                                            <td style="
                                                padding:13px 0;
                                                color:#64748b;
                                                font-size:14px;
                                                border-top:1px solid #f1f5f9;
                                            ">
                                                Email
                                            </td>

                                            <td style="
                                                padding:13px 0;
                                                border-top:1px solid #f1f5f9;
                                            ">
                                                <a
                                                    href="mailto:{email}"
                                                    style="
                                                        color:#2563eb;
                                                        text-decoration:none;
                                                        font-size:14px;
                                                    "
                                                >
                                                    {email}
                                                </a>
                                            </td>
                                        </tr>


                                        <tr>
                                            <td style="
                                                padding:13px 0;
                                                color:#64748b;
                                                font-size:14px;
                                                border-top:1px solid #f1f5f9;
                                            ">
                                                Phone
                                            </td>

                                            <td style="
                                                padding:13px 0;
                                                color:#0f172a;
                                                font-size:14px;
                                                border-top:1px solid #f1f5f9;
                                            ">
                                                {phone}
                                            </td>
                                        </tr>


                                        <tr>
                                            <td style="
                                                padding:13px 0;
                                                color:#64748b;
                                                font-size:14px;
                                                border-top:1px solid #f1f5f9;
                                            ">
                                                Subject
                                            </td>

                                            <td style="
                                                padding:13px 0;
                                                color:#0f172a;
                                                font-size:14px;
                                                font-weight:bold;
                                                border-top:1px solid #f1f5f9;
                                            ">
                                                {subject}
                                            </td>
                                        </tr>


                                        <tr>
                                            <td style="
                                                padding:13px 0;
                                                color:#64748b;
                                                font-size:14px;
                                                border-top:1px solid #f1f5f9;
                                            ">
                                                Received
                                            </td>

                                            <td style="
                                                padding:13px 0;
                                                color:#0f172a;
                                                font-size:14px;
                                                border-top:1px solid #f1f5f9;
                                            ">
                                                {current_time}
                                            </td>
                                        </tr>

                                    </table>

                                </div>

                            </div>


                            <!-- MESSAGE -->
                            <div style="
                                background:#eff6ff;
                                border-left:4px solid #2563eb;
                                border-radius:10px;
                                padding:20px;
                                margin-bottom:25px;
                            ">

                                <div style="
                                    color:#1e3a8a;
                                    font-size:13px;
                                    font-weight:bold;
                                    text-transform:uppercase;
                                    letter-spacing:0.5px;
                                    margin-bottom:10px;
                                ">
                                    📝 Message
                                </div>

                                <div style="
                                    color:#334155;
                                    font-size:15px;
                                    line-height:1.7;
                                    white-space:pre-wrap;
                                ">
                                    {message}
                                </div>

                            </div>


                            <!-- REPLY BUTTON -->
                            <div style="
                                text-align:center;
                                padding:10px 0 5px;
                            ">

                                <a
                                    href="mailto:{email}"
                                    style="
                                        display:inline-block;
                                        background:#2563eb;
                                        color:#ffffff;
                                        text-decoration:none;
                                        padding:13px 25px;
                                        border-radius:8px;
                                        font-size:14px;
                                        font-weight:bold;
                                    "
                                >
                                    Reply to {name}
                                </a>

                            </div>

                        </div>


                        <!-- FOOTER -->
                        <div style="
                            background:#f8fafc;
                            border-top:1px solid #e2e8f0;
                            padding:22px 30px;
                            text-align:center;
                        ">

                            <p style="
                                margin:0 0 6px;
                                color:#334155;
                                font-size:13px;
                                font-weight:bold;
                            ">
                                SirBrams Tech Virtual Campus
                            </p>

                            <p style="
                                margin:0;
                                color:#94a3b8;
                                font-size:12px;
                                line-height:1.6;
                            ">
                                This notification was automatically generated
                                from your website contact form.
                            </p>

                        </div>

                    </div>

                </div>

            </body>
            </html>
            """

            admin_text = strip_tags(admin_html)

            admin_email = EmailMultiAlternatives(
                admin_subject,
                admin_text,
                settings.DEFAULT_FROM_EMAIL,
                ['sirbrams.b@gmail.com']
            )

            admin_email.attach_alternative(
                admin_html,
                "text/html"
            )

            admin_email.send()

            logger.info(
                "📧 HTML Contact email sent successfully "
                "to sirbrams.b@gmail.com"
            )


            # ============================================================
            # 3. SEND MODERN HTML AUTO-REPLY TO CLIENT
            # ============================================================

            client_subject = (
                "Thank you for contacting SirBrams Tech Virtual Campus"
            )

            client_html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Thank You</title>
            </head>

            <body style="
                margin:0;
                padding:0;
                background:#f1f5f9;
                font-family:Arial, Helvetica, sans-serif;
                color:#1e293b;
            ">

                <div style="
                    width:100%;
                    padding:40px 15px;
                    box-sizing:border-box;
                ">

                    <div style="
                        max-width:620px;
                        margin:0 auto;
                        background:#ffffff;
                        border-radius:18px;
                        overflow:hidden;
                        box-shadow:0 8px 30px rgba(15,23,42,0.08);
                    ">

                        <!-- HEADER -->
                        <div style="
                            background:linear-gradient(135deg,#0f172a,#1e3a8a);
                            padding:40px 30px;
                            text-align:center;
                        ">

                            <img
                                src="https://res.cloudinary.com/dbkuxm0jo/image/upload/v1759413687/profile_images/ztqvzdv1ajimw4894t7h.png"
                                alt="SirBrams Logo"
                                style="
                                    height:60px;
                                    width:auto;
                                    margin-bottom:20px;
                                "
                            >

                            <div style="
                                display:inline-block;
                                background:rgba(255,255,255,0.12);
                                color:#bfdbfe;
                                padding:7px 13px;
                                border-radius:30px;
                                font-size:12px;
                                font-weight:bold;
                                letter-spacing:0.5px;
                            ">
                                MESSAGE RECEIVED
                            </div>

                        </div>


                        <!-- MAIN CONTENT -->
                        <div style="
                            padding:40px 30px;
                            text-align:center;
                        ">

                            <div style="
                                font-size:42px;
                                margin-bottom:10px;
                            ">
                                👋
                            </div>


                            <h1 style="
                                margin:0 0 15px;
                                color:#0f172a;
                                font-size:28px;
                                line-height:1.3;
                            ">
                                Hello {name}!
                            </h1>


                            <p style="
                                margin:0 auto 25px;
                                max-width:480px;
                                color:#64748b;
                                font-size:15px;
                                line-height:1.8;
                            ">
                                Thank you for reaching out to
                                <strong style="color:#1e3a8a;">
                                    SirBrams Tech Virtual Campus
                                </strong>.
                                We appreciate you taking the time to contact us.
                            </p>


                            <!-- SUCCESS MESSAGE -->
                            <div style="
                                background:#ecfdf5;
                                border:1px solid #bbf7d0;
                                border-radius:12px;
                                padding:18px 20px;
                                margin:25px 0;
                            ">

                                <div style="
                                    font-size:20px;
                                    margin-bottom:7px;
                                ">
                                    ✓
                                </div>

                                <p style="
                                    margin:0;
                                    color:#166534;
                                    font-size:14px;
                                    line-height:1.6;
                                ">
                                    Your message has been successfully received.
                                    Our team will review it and get back to you
                                    within <strong>24 hours</strong>.
                                </p>

                            </div>


                            <!-- YOUR MESSAGE -->
                            <div style="
                                text-align:left;
                                background:#f8fafc;
                                border:1px solid #e2e8f0;
                                border-radius:12px;
                                padding:20px;
                                margin:25px 0;
                            ">

                                <div style="
                                    color:#1e3a8a;
                                    font-size:12px;
                                    font-weight:bold;
                                    text-transform:uppercase;
                                    letter-spacing:0.7px;
                                    margin-bottom:12px;
                                ">
                                    Your Message
                                </div>


                                <div style="
                                    background:#ffffff;
                                    border-radius:8px;
                                    padding:15px;
                                    color:#475569;
                                    font-size:14px;
                                    line-height:1.7;
                                    white-space:pre-wrap;
                                ">
                                    {message}
                                </div>

                            </div>


                            <!-- SUPPORT -->
                            <div style="
                                margin-top:30px;
                            ">

                                <p style="
                                    margin:0 0 8px;
                                    color:#64748b;
                                    font-size:13px;
                                ">
                                    Need urgent assistance?
                                </p>

                                <a
                                    href="tel:+254742524370"
                                    style="
                                        color:#2563eb;
                                        text-decoration:none;
                                        font-size:15px;
                                        font-weight:bold;
                                    "
                                >
                                    +254 742 524 370
                                </a>

                            </div>

                        </div>


                        <!-- FOOTER -->
                        <div style="
                            background:#f8fafc;
                            border-top:1px solid #e2e8f0;
                            padding:25px 30px;
                            text-align:center;
                        ">

                            <p style="
                                margin:0 0 5px;
                                color:#0f172a;
                                font-size:14px;
                                font-weight:bold;
                            ">
                                SirBrams Tech Solutions
                            </p>

                            <p style="
                                margin:0;
                                color:#94a3b8;
                                font-size:11px;
                                line-height:1.6;
                            ">
                                This is an automated confirmation that your
                                message was received.
                                Please do not reply to this email.
                            </p>

                        </div>

                    </div>

                </div>

            </body>
            </html>
            """

            client_text = strip_tags(client_html)

            client_email = EmailMultiAlternatives(
                client_subject,
                client_text,
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )

            client_email.attach_alternative(
                client_html,
                "text/html"
            )

            client_email.send()

            logger.info(
                f"📧 HTML Auto-reply sent to {email}"
            )


            messages.success(
                request,
                "Your message has been sent successfully. Please check your email for confirmation."
            )

        except Exception as e:
            logger.error(
                f"❌ Contact processing failed: {str(e)}",
                exc_info=True
            )

            messages.error(
                request,
                "Something went wrong. Please try again later."
            )

        return redirect('contact')

    return render(
        request,
        'contact.html',
        {'current_page': 'contact'}
    )

def service(request):
    return render(request, 'service.html', {'current_page': 'services'})


def main(request):
    return render(request,'main.html')
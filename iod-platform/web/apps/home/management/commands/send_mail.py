from django.core.management.base import BaseCommand
from django.conf import settings
from apps.home.lib import email
from django.template.loader import render_to_string
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Send networth update to nominee'

    def handle(self, *args, **options):
        subject = 'Networth Summary Update'
        message = f'Hi Sameer, below is the update of networth summary.'
        email_from = settings.EMAIL_HOST_USER
        print(email_from)
        #recipient_list = ["portfolio@investodiary.com","sameersh@sameershaikcoder.c1.is"]
        recipient_list = ["sameersh@sameershaikcoder.c1.is"]
        print("Sending email..")
        context = email.compose_networth_summary()
        html_message = render_to_string('home/email.html', context=context)
        html_content_transformed = html_message
        try:
            result = send_mail(subject, message, email_from, recipient_list,html_message=html_content_transformed ,fail_silently=False)
            print("result is "+str(result))
            print("Email was sent successfully")
        except Exception as e:
            print("error occured "+ str(e))
            
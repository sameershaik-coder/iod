from django.core.management.base import BaseCommand
from django.conf import settings
import asyncio
import aiosmtpd.controller
import threading

class Command(BaseCommand):
    help = 'Starts a local SMTP server for development'

    def handle(self, *args, **options):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        handler = CustomSMTPHandler()
        self.server = aiosmtpd.controller.Controller(handler, hostname='localhost', port=8025)

        print("Starting smtp server locally...")
        self.server.start()

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print("Stopping smtp server...")
        finally:
            self.server.stop()
            loop.close()

class CustomSMTPHandler:
    EMAIL_NUMBER=1
    async def handle_DATA(self, server, session, envelope):
        print(f"Recieved new message ---BEGIN---------{CustomSMTPHandler.EMAIL_NUMBER}------------------------------------------------------------------------------- ")
        print("Message from:", envelope.mail_from)
        print("Message for:", envelope.rcpt_tos)
        print("Message content:", envelope.content.decode())
        print(f"Recieved new message ---END---------{CustomSMTPHandler.EMAIL_NUMBER}------------------------------------------------------------------------------- ")
        CustomSMTPHandler.EMAIL_NUMBER = CustomSMTPHandler.EMAIL_NUMBER + 1
        return '250 OK'

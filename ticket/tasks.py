from celery import shared_task
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Book
from django.conf import settings
from accounts.models import CustomUser

User = CustomUser

@shared_task
def send_departure_reminders():
    channel_layer = get_channel_layer()
    current_time = now()

    users = User.objects.all()
    for user in users:
        if user.created_at == current_time:
            message_body = (f"You have created a new account into our platform.\n"
                            f"Please make your request as we wait to serve them.\n"
                            f"All rights reserved @WORTH_PORT_UG.")

            message = send_mail(
                f"Dear {user.username},",
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list=(user.email,),
                fail_silently=False
            )

            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notifications",
                    "message": message
                }
            )

    books = Book.objects.all()
    for book in books:
        if book.bus.departure == current_time:
            message_body = (f"Dear {book.user.email}, your bus with the following details has started its journey. \n"
                       f"BOOKING NAME: {book.full_name}\n"
                       f"BUS: {book.bus.bus_name}\n"
                       f"SEAT: {book.seat}\n"
                       f"BUS NUMBER: {book.bus.number}\n"
                       f"DESTINATION: From {book.bus.start} To {book.bus.stop}\n")

            message = send_mail(
                "WARNING FOR YOUR BOOKED TICKET",
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list=(book.user.email,),
                fail_silently=False
            )

            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notifications",
                    "message": message
                }
            )

        elif book.bus.departure < timedelta(minutes=30):
            message_body = (f"Dear {book.user.email}, your bus with the following details LEAVES in 30 minutes. \n"
                       f"BOOKING NAME: {book.full_name}\n"
                       f"BUS: {book.bus.bus_name}\n"
                       f"SEAT: {book.seat}\n"
                       f"BUS NUMBER: {book.bus.number}\n"
                       f"DESTINATION: From {book.bus.start} To {book.bus.stop}\n"
                       f"PLEASE BE DO NOT MISS YOUR BUS.")

            message = send_mail(
                "TICKET REMINDER",
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list=(book.user.email,),
                fail_silently=False
            )
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notifications",
                    "message": message
                }
            )

        elif book.bus.departure < timedelta(minutes=60):
            message_body = (f"Dear {book.user.email}, your bus with the following details LEAVES in 1 hour from NOW. \n"
                       f"BOOKING NAME: {book.full_name}\n"
                       f"BUS: {book.bus.bus_name}\n"
                       f"SEAT: {book.seat}\n"
                       f"BUS NUMBER: {book.bus.number}\n"
                       f"DESTINATION: From {book.bus.start} To {book.bus.stop}\n"
                       f"PLEASE BE DO NOT MISS YOUR BUS.")

            message = send_mail(
                "TICKET REMINDER",
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list=(book.user.email,),
                fail_silently=False
            )
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notifications",
                    "message": message
                }
            )

        elif book.created_at == current_time:
            message_body = (f"Dear {book.user.username}, you booked a bus with the following details. \n"
                       f"BOOKING NAME: {book.full_name}\n"
                       f"BUS: {book.bus.bus_name}\n"
                       f"SEAT: {book.seat}\n"
                       f"BUS NUMBER: {book.bus.number}\n"
                       f"DESTINATION: From {book.bus.start} To {book.bus.stop}\n"
                       f"PLEASE BE SURE TO PREPARE EARLY.")

            message = send_mail(
                "WARNING FOR YOUR BOOKED TICKET",
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list=(book.user.email,),
                fail_silently=False
            )
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notifications",
                    "message": message
                }
            )

        elif book.updated_at == current_time:
            message_body = (f"Dear {book.user.username}, you have updated your booked ticket to the following details. \n"
                       f"BOOKING NAME: {book.full_name}\n"
                       f"BUS: {book.bus.bus_name}\n"
                       f"SEAT: {book.seat}\n"
                       f"BUS NUMBER: {book.bus.number}\n"
                       f"DESTINATION: From {book.bus.start} To {book.bus.stop}\n"
                       f"PLEASE BE SURE TO PREPARE EARLY.")

            message = send_mail(
                "WARNING FOR YOUR BOOKED TICKET",
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list=(book.user.email,),
                fail_silently=False
            )
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notifications",
                    "message": message
                }
            )

        else:
            message_body = (f"Dear {book.user.username}, you booked bus LEAVES at {book.bus.departure}. \n"
                       f"BOOKING NAME: {book.full_name}\n"
                       f"BUS: {book.bus.bus_name}\n"
                       f"SEAT: {book.seat}\n"
                       f"BUS NUMBER: {book.bus.number}\n"
                       f"DESTINATION: From {book.bus.start} To {book.bus.stop}\n"
                       f"PLEASE BE SURE TO PREPARE EARLY.")

            message = send_mail(
                "WARNING FOR YOUR BOOKED TICKET",
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list=(book.user.email,),
                fail_silently=False
            )
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notifications",
                    "message": message
                }
            )


from django.core.mail.backends.smtp import EmailBackend
from django.contrib import messages
from django.utils import timezone
import time
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Bus, Book, Service, Attachment
from .forms import BusForm, BookForm, ServiceForm, UpdateBookForm, AttachmentForm, UpdateBusForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from django.http import JsonResponse

users = get_user_model()

@login_required(login_url="register")
def home(request):

    books = Book.objects.order_by("-created_at")[:3]

    services = Service.objects.all()[:2]
    context = {"books": books, "services": services}
    return render(request, "ticket/home.html", context)

@login_required(login_url="login")
def all_buses(request):

    all_created_buses = Bus.objects.filter(archived=False)

    services = Service.objects.all()[:2]
    context = {"all_created_buses": all_created_buses, "services": services}
    return render(request, "ticket/all_buses.html", context)

@login_required(login_url="login")
def view_archived_tickets(request):
    current_time = now()

    buses = Bus.objects.filter(departure__lte=current_time)
    for bus in buses:
        bus.archived = True
        bus.save()

        books = Book.objects.filter(bus=bus)
        for book in books:
            book.archived = True
            book.save()

    archived_buses = Bus.objects.filter(archived=True).order_by("-created_at")
    bus_count = archived_buses.count()

    services = Service.objects.all()[:2]
    context = {"archived_buses": archived_buses, "bus_count":bus_count, "services": services}
    return render(request, "ticket/archived_bus.html", context)

@login_required(login_url="login")
def view_archived_books(request, bus_id):
    archived_books = Book.objects.filter(bus_id=bus_id,archived=True)
    book_count = archived_books.count()
    context = {"archived_books": archived_books, "book_count": book_count}
    return render(request, "ticket/archived_books.html", context)

@login_required(login_url="login")
def all_tickets(request):
    all_created_tickets = Book.objects.order_by("-created_at")
    services = Service.objects.all()[:2]
    context = {"all_created_tickets": all_created_tickets, "services": services}
    return render(request, "ticket/all_tickets.html", context)

@login_required(login_url="login")
def all_bus_tickets(request, bus_id):
    bus = Bus.objects.get(bus_id=bus_id)
    bus_bookings = Book.objects.filter(bus=bus)
    bus_bookings_count = bus_bookings.count()

    services = Service.objects.all()[:2]
    context = {"bus_bookings": bus_bookings, "bus_bookings_count": bus_bookings_count, "services": services}
    return render(request, "ticket/bus_tickets.html", context)

@login_required(login_url="login")
def all_services(request):
    our_services = Service.objects.all()
    services = Service.objects.all()[:2]
    context = {"our_services": our_services, "services": services}
    return render(request, "ticket/services.html", context)

# All creation views
@login_required(login_url="login")
def enter_bus(request):
    if request.method == "POST":
        form = BusForm(request.POST)
        if form.is_valid():
            bus = form.save(commit=False)
            bus.save()
            return redirect("home")
    else:
        form = BusForm()
    services = Service.objects.all()[:2]
    context = {"form": form, "services": services}
    return render(request, "ticket/bus.html", context)

@login_required(login_url="login")
def book_bus(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.bus =  Bus.objects.get(bus_id=request.POST.get("bus"))
            form.user = request.user

            form.status = "WAITING"
            form.upload = "NO UPLOAD"
            messages.info(request, f"You have booked a ticket on BUS: {form.bus.bus_name} & NUMBER: {form.bus.number}")
            form.save()
            return redirect("home")

    else:
        form = BookForm()
    services = Service.objects.all()[:2]
    context = {"form": form, "services": services}
    return render(request, "ticket/book.html", context)

@login_required(login_url="login")
def service_create_view(request):
    if request.method == "POST":
        service_form = ServiceForm(request.POST)
        if service_form.is_valid():
            service_form = service_form.save(commit=False)
            service_form.save()
            return redirect("home")
    else:
        service_form = ServiceForm()
    services = Service.objects.all()[:2]
    context = {"service_form": service_form, "services": services}
    return render(request, "ticket/service.html", context)

@login_required(login_url="login")
def attachment_create_view(request, book_id):
    book = Book.objects.get(book_id=book_id)
    if request.method == "POST":
        form = AttachmentForm(request.POST, request.FILES)

        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.book = book
            attachment.status = "UPLOADED"
            attachment.attached = True
            messages.info(request, f"You have attached payments for ticket booked on BUS: {attachment.book.bus.bus_name}")
            attachment.save()
            book.attached = True
            book.save()
            form.save(attachment)
            return redirect("home")
    else:
        form = AttachmentForm()
    context = {"form": form}
    return render(request, "ticket/attachment_add.html", context)

# All update views
@login_required(login_url="login")
def book_update_view(request, book_id):
    booking = Book.objects.get(book_id=book_id)

    if request.method == "POST":
        form = UpdateBookForm(request.POST, instance=booking)
        if form.is_valid():
            form = form.save(commit=False)
            form.bus = Bus.objects.get(bus_id=request.POST.get("bus"))

            if form.user == booking.user:
                messages.info(request, f"You have updated your booked ticket on BUS: {form.bus.bus_name}")
                form.save()
                return redirect("book-details", book_id)
            else:
                messages.error(request, "You can't update this Ticket, you did not create it.")
                return redirect("home")
    else:
        form = UpdateBookForm(instance=booking)
    services = Service.objects.all()[:2]
    context = {"form": form, "services": services, "booking": booking}
    return render(request, "ticket/update_ticket.html", context)

@login_required(login_url="login")
def bus_update_view(request, bus_id):
    bus = Bus.objects.get(bus_id=bus_id)

    if request.method == "POST":
        form = UpdateBusForm(request.POST, instance=bus)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect("all-buses")
    else:
        form = UpdateBusForm(instance=bus)
    services = Service.objects.all()[:2]
    context = {"services": services, "form": form}
    return render(request, "ticket/update_bus.html", context)

@login_required(login_url="login")
def update_archived_bus(request, bus_id):
    bus = Bus.objects.filter(bus_id=bus_id, archived=True)

    if request.method == "POST":
        form = UpdateBusForm(request.POST, instance=bus)
        if form.is_valid():
            form.save()
            return redirect("bus-details", bus_id)
    else:
        form = UpdateBusForm(instance=bus)
    services = Service.objects.all()[:2]
    context = {"form": form, "services": services}
    return render(request, "ticket/update_bus.form", context)

@login_required(login_url="login")
def service_update_view(request, service_id):
    service = Service.objects.get(service_id=service_id)

    if request.method == "POST":
        service_form = ServiceForm(request.POST, instance=service)
        if service_form.is_valid():
            service_form = service_form.save(commit=False)
            service_form.save()
            return redirect("home")
    else:
        service_form = ServiceForm(instance=service)
    services = Service.objects.all()[:2]
    context = {"service_form": service_form, "services": services}
    return render(request, "ticket/update_service.html", context)

# All details views
@login_required(login_url="login")
def bus_details_views(request, bus_id):
    bus = Bus.objects.get(bus_id=bus_id)
    services = Service.objects.all()[:2]
    context = {"bus": bus, "services": services}
    return render(request, "ticket/bus_details.html", context)

@login_required(login_url="login")
def book_details_view(request, book_id):
    # current_time = now()
    book = Book.objects.get(book_id=book_id)

    # send_bus_departure_notifications()
    services = Service.objects.all()[:2]
    context = {"book": book, "services": services}
    return render(request, "ticket/book_details.html", context)

@login_required(login_url="login")
def service_details_view(request, service_id):
    service = Service.objects.get(service_id=service_id)
    services = Service.objects.all()[:2]
    context = {"service": service, "services": services}
    return render(request, "ticket/service_details.html", context)

@login_required(login_url="login")
def attachment_details(request, book_id):
    book = Book.objects.get(book_id=book_id)
    attachment = Attachment.objects.filter(book=book)
    attach_count = attachment.count()
    context = {"attachment": attachment, "attach_count": attach_count}
    return render(request, "ticket/attach_details.html", context)

# All delete views
@login_required(login_url="login")
def delete_book_view(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)

    if request.method == "POST":
        if request.user == book.user:
            book.delete()
            messages.info(request, "You have have deleted your ticket")
            return redirect("home")

        elif request.user.is_staff or request.user.is_admin:
            book.delete()
            messages.info(request, f"You have have deleted {book.user.username} ticket.")
            return redirect("home")

        else:
            messages.error(request, "Not Your Ticket.")
            return redirect("home")
    services = Service.objects.all()[:2]
    context = {"obj": book, "services": services}
    return render(request, "ticket/delete.html", context)

@login_required(login_url="login")
def delete_bus_view(request, bus_id):
    bus = get_object_or_404(Bus, bus_id=bus_id)

    if request.method == "POST":
        bus.delete()
        return redirect("home")
    services = Service.objects.all()[:2]
    context = {"obj": bus, "services": services}
    return render(request, "ticket/delete.html", context)

def delete_service_view(request, service_id):
    service = get_object_or_404(Service, service_id=service_id)

    if request.method == "POST":
        service.delete()
        return redirect("home")
    services = Service.objects.all()[:2]
    context = {"obj": service, "services": services}
    return render(request, "ticket/delete.html", context)

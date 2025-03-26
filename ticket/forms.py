from datetime import datetime
from random import random

from django import forms
from .models import Book, Bus, Service, Attachment
from django.utils.timezone import now, timedelta


# All creation forms
class BookForm(forms.ModelForm):
    current_time = now()
    bus = forms.ModelChoiceField(
        queryset=Bus.objects.filter(departure__gt=current_time, archived=False),
        empty_label="Select A Bus",
        label="Bus",
        widget=forms.Select(attrs={"class": "form-control", "bus_id": "bus-select", "onchange": "this.form.submit()"})
    )
    seat = forms.ChoiceField(choices=[], widget=forms.Select(attrs={"class": "form-control"}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_css_class = " "

        if self.data.get("bus"):
            bus_id = self.data.get("bus")
            bus = Bus.objects.get(bus_id=bus_id)

            available_seats = bus.get_available_seats()

            self.fields["seat"].choices = [(" ", "Select a seat")] + [(seat, seat) for seat in available_seats]
            self.fields["seat"].required = True
        else:
            self.fields["seat"].choices = [(" ", "Select a bus first")]

    class Meta:
        model = Book
        fields = ("bus", "seat", "full_name", "phone")

        widgets = {
            "bus": forms.Select(attrs={"class": "form-control"}),
            "seat": forms.Select(attrs={"class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Booking Name"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
        }
        error_messages = {
            "full_name": {"required": " "},
            "phone": {"required": " "}
        }



class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ("bus_name", "number", "start", "stop", "departure", "arrival", "total_seats", "amount")
        widgets = {
            "bus_name": forms.TextInput(attrs={"class": "form-control"}),
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "start": forms.TextInput(attrs={"class": "form-control"}),
            "stop": forms.TextInput(attrs={"class": "form-control"}),
            "departure": forms.DateTimeInput(attrs={"class": "form-control"}),
            "arrival": forms.DateTimeInput(attrs={"class": "form-control"}),
            "total_seats": forms.NumberInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"})
        }

    def clean_bus(self):
        bus_name = self.cleaned_data["bus_name"]
        number = self.cleaned_data["number"]
        start = self.cleaned_data["start"]
        stop = self.cleaned_data["stop"]
        departure = self.cleaned_data["departure"]
        arrival = self.cleaned_data["arrival"]
        total_seats = self.cleaned_data["total_seats"]

        if Bus.objects.filter(bus_name=bus_name, number=number, start=start, stop=stop, departure=departure, arrival=arrival, total_seats=total_seats).exists():
            raise forms.ValidationError("Bus already exists, please check the correct details.")
        return bus_name


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ("name", "description")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }


# All update forms
class UpdateBookForm(forms.ModelForm):
    current_time = now()

    bus = forms.ModelChoiceField(
        queryset=Bus.objects.filter(departure__gt=current_time),
        required=False,
        empty_label=None,
        label="Available Buses",
        widget=forms.Select(attrs={"class": "form-control", "bus_id": "bus-select", "onchange": "this.form.submit()"})
    )

    seat = forms.ChoiceField(
        required=False,
        label="Available Seats",
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=[]
    )

    class Meta:
        model = Book
        fields = ("bus", "seat", "full_name", "phone")

        widgets = {
            "bus": forms.Select(attrs={"readonly": "readonly", "class": "form-control"}),
            "seat": forms.Select(attrs={"readonly": "readonly", "class": "form-control"}),
            "full_name": forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
            "phone": forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        selected_bus = kwargs.pop("selected_bus", None)
        super().__init__(*args, **kwargs)

        if self.instance.bus_id:
            self.fields["full_name"].initial = self.instance.full_name
            self.fields["phone"].initial = self.instance.phone
            self.fields["bus"].initial = self.instance.bus
            self.fields["seat"].initial = self.instance.seat

            bus = self.instance.bus
            all_available_seat = bus.get_available_seats()
            current_time = now()

            if bus.departure > current_time:
                available_seats = [seat for seat in all_available_seat if not Book.objects.filter(bus=bus, seat=seat).exists()]

                self.fields["seat"].choices = [(seat, seat) for seat in available_seats]
                self.fields["seat"].choices.insert(0, (self.instance.seat, self.instance.seat))
                self.fields["seat"].initial = self.instance.seat

            elif bus.departure < current_time:
                available_seats = ["Seats not available, bus has already left"]
                self.fields["seat"].choices = [(seat, seat) for seat in available_seats]
                self.fields["seat"].initial = self.instance.seat

            elif selected_bus:
                available_seats = [seat for seat in bus.get_available_seats() if not Book.objects.filter(bus=bus, seat=seat).exists()]
                self.fields["seat"].choices = [(seat, seat) for seat in available_seats]
                self.fields["seat"].initial = self.instance.seat

        if self.data.get("bus"):
            bus_id = self.data.get("bus")
            bus = Bus.objects.get(bus_id=bus_id)

            available_seats = bus.get_available_seats()
            self.fields["seat"].choices = [(seat, seat) for seat in available_seats if not Book.objects.filter(bus=bus, seat=seat).exists()]
            self.fields["seat"].required = True
        else:
            self.fields["seat"].choices = [(" ", " ")]

    def clean(self):
        cleaned_data = super().clean()
        new_bus = cleaned_data.get("bus")
        new_seat = cleaned_data.get("seat")
        if new_bus and new_seat:
            available_seats = [seat for seat in new_bus.get_available_seats() if not Book.objects.filter(bus=new_bus, seat=new_seat).exists()]

            if new_seat not in available_seats:
                self.add_error("seat", "seat is not available on the selected bus.")
        return cleaned_data


class UpdateBusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ("bus_name", "number", "start", "stop", "departure", "arrival", "total_seats", "amount")

        widgets = {
            "bus_name": forms.TextInput(attrs={"class": "form-control"}),
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "start": forms.TextInput(attrs={"class": "form-control"}),
            "stop": forms.TextInput(attrs={"class": "form-control"}),
            "departure": forms.DateTimeInput(attrs={"class": "form-control"}),
            "arrival": forms.DateTimeInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "total_seats": forms.NumberInput(attrs={"class": "form-control"}),
        }


class UpdateServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ("image",)


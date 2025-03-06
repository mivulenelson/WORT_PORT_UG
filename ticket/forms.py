from datetime import datetime
from django import forms
from .models import Book, Bus, Service, Attachment
from django.utils.timezone import now, timedelta


# All creation forms
class BookForm(forms.ModelForm):
    current_time = now()
    bus = forms.ModelChoiceField(queryset=Bus.objects.filter(departure__gt=current_time, archived=False))

    class Meta:
        model = Book
        fields = ("bus", "seat", "full_name", "phone")

        widgets = {
            "bus": forms.Select(attrs={"class": "form-control"}),
            "seat": forms.NumberInput(attrs={"class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_seat(self):
        seat = self.cleaned_data["seat"]
        bus = self.cleaned_data["bus"]

        if Book.objects.filter(bus=bus, seat=seat).exists():
            raise forms.ValidationError("Seat already taken")
        return seat


class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ("bus_name", "number", "start", "stop", "departure", "arrival", "total_seats")
        widgets = {
            "bus_name": forms.TextInput(attrs={"class": "form-control"}),
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "start": forms.TextInput(attrs={"class": "form-control"}),
            "stop": forms.TextInput(attrs={"class": "form-control"}),
            "departure": forms.DateTimeInput(attrs={"class": "form-control"}),
            "arrival": forms.DateTimeInput(attrs={"class": "form-control"}),
            "total_seats": forms.NumberInput(attrs={"class": "form-control"}),
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
    class Meta:
        model = Book
        fields = ("bus", "seat", "full_name", "phone")
        widgets = {
            "bus": forms.Select(attrs={"class": "form-control"}),
            "seat": forms.NumberInput(attrs={"class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"})
        }


class UpdateBusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ("bus_name", "number", "start", "stop", "departure", "arrival", "total_seats")
        widgets = {
            "bus_name": forms.TextInput(attrs={"class": "form-control"}),
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "start": forms.TextInput(attrs={"class": "form-control"}),
            "stop": forms.TextInput(attrs={"class": "form-control"}),
            "departure": forms.DateTimeInput(attrs={"class": "form-control"}),
            "arrival": forms.DateTimeInput(attrs={"class": "form-control"}),
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


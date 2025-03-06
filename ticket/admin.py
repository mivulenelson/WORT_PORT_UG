from django.contrib import admin
from .models import Bus, Book, Service, Attachment

admin.site.register(Book)
admin.site.register(Bus)
admin.site.register(Service)
admin.site.register(Attachment)

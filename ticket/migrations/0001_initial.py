# Generated by Django 5.0 on 2025-03-26 08:57

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('bus_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bus_name', models.CharField(max_length=30)),
                ('number', models.CharField(max_length=15, unique=True)),
                ('start', models.CharField(max_length=30)),
                ('stop', models.CharField(max_length=30)),
                ('departure', models.DateTimeField()),
                ('arrival', models.DateTimeField()),
                ('total_seats', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('AVAILABLE', 'AVAILABLE'), ('UNAVAILABLE', 'UNAVAILABLE')], default='AVAILABLE', max_length=15)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('archived', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('service_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('seat', models.CharField(max_length=2)),
                ('full_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('status', models.CharField(blank=True, choices=[('ACTIVE', 'ACTIVE'), ('WAITING', 'WAITING'), ('CLOSED', 'CLOSED')], default='WAITING', max_length=225, null=True)),
                ('is_taken', models.BooleanField(default=False)),
                ('archived', models.BooleanField(default=False)),
                ('attached', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Assigned to')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL, verbose_name='Ticket Owner')),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_set', to='ticket.bus')),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('attach_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(max_length=1000, upload_to='images')),
                ('attached', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.book')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]

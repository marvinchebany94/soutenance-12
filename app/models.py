from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from rest_framework import request


class User(AbstractUser):
    class Meta:
        permissions = (
            ('sales_permissions', 'sales_permissions'),
            ('support_permissions', 'support_permissions')
        )
    username = None
    email = models.EmailField(max_length=100, blank=False, unique=True)
    password = models.CharField(max_length=254, blank=False)
    EQUIPES = [
        ('gestion', 'gestion'),
        ('vente', 'vente')
    ]
    equipe = models.CharField(choices=EQUIPES, blank=False, max_length=10)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('password',)

    def has_sales_permissions(self):
        if self.equipe == "vente":
            return True


class Clients(models.Model):
    first_name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=25, blank=False)
    email = models.EmailField(max_length=100, blank=False, unique=True)
    phone = models.CharField(max_length=20, blank=False, unique=True)
    mobile = models.CharField(max_length=20, blank=False, unique=True)
    company_name = models.CharField(max_length=250, blank=False, unique=True)
    date_created = models.DateTimeField(blank=False, auto_now_add=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE,
                                      blank=False)


class Contrats(models.Model):
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE,
                                      blank=False, default="")
    client_associe = models.ForeignKey(Clients, on_delete=models.CASCADE,
                                       blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(blank=False)
    amout = models.FloatField(blank=False)
    payement_due = models.DateTimeField(blank=False)


class Events(models.Model):
    client_associe = models.ForeignKey(Clients, on_delete=models.CASCADE,
                                       blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(blank=True)
    support_contact = models.ForeignKey(User, on_delete=models.CASCADE,
                                        blank=False)
    #event_status = models.ForeignKey(Contacts, on_delete=models.CASCADE,
                                     #blank=True)
    participants = models.IntegerField(blank=False)
    event_date = models.DateTimeField(blank=False)
    notes = models.CharField(max_length=8124, blank=True)

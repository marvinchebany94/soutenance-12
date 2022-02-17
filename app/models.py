from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.


class User(AbstractUser):
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


class Clients(models.Model):
    first_name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=25, blank=False)
    email = models.EmailField(max_length=100, blank=False, unique=True)
    phone = models.CharField(max_length=20, blank=False, unique=True)
    mobile = models.CharField(max_length=20, blank=False, unique=True)
    company_name = models.CharField(max_length=250, blank=False, unique=True)
    date_created = models.DateTimeField(blank=False, auto_now_add=True)
    date_updated = models.DateTimeField(blank=True)
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE,
                                      blank=False)


class Contacts(models.Model):
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE,
                                      blank=False)
    client_associe = models.ForeignKey(Clients, on_delete=models.CASCADE,
                                       blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(blank=True)
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

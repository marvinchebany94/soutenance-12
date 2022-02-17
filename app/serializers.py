from rest_framework.serializers import ModelSerializer
from app import models


class UserSerializers(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['email', 'password', 'first_name', 'last_name', 'equipe']


class ClientsSerializers(ModelSerializer):
    class Meta:
        model = models.Clients
        fields = '__all__'


class ContactsSerializers(ModelSerializer):
    class Meta:
        model = models.Contacts
        fields = '__all__'


class EventsSerializers(ModelSerializer):
    class Meta:
        model = models.Events
        fields = '__all__'

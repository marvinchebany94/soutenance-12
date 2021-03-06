from datetime import datetime

import pytz
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required
from django.db import IntegrityError
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from app.serializers import UserSerializers, ClientsSerializers, \
    ContratsSerializers, EventsSerializers
from .models import User, Clients, Contrats, Events
from .permissions import EquipeDeVente, EquipeDeGestion
from .my_own_fonctions import verifiy_pk

# Create your views here.


@api_view(['POST'])
def connexion_view(request):
    if request.POST.get('email') and request.POST.get('password'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response("Aucun compte n'existe avec cet email.",
                            status=status.HTTP_404_NOT_FOUND)
        if user.check_password(password):
            request.user = authenticate(request, email=email, password=password)
            if request.user.is_authenticated:

                return Response('Tu es connecté.')
            else:
                return Response(request.user.is_authenticated)
        else:
            if not request.user.is_authenticated:
                return Response("Mot de passe invalide.",
                                status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("Tu dois entrer ton email et mdp.",
                        status=status.HTTP_404_NOT_FOUND)


class ClientsView(ModelViewSet):
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        client_name = self.request.GET.get('name')
        client_email = self.request.GET.get('email')
        if client_name:
            queryset = self.queryset.filter(last_name=client_name,
                                            sales_contact=self.request.user)
            if not queryset:
                raise ValidationError({"Error":
                                      ["Aucun client n'a été trouvé avec ce \
nom."]})
            else:
                return queryset
        elif client_email:
            queryset = self.queryset.filter(email=client_email,
                                            sales_contact=self.request.user)
            if not queryset:
                raise ValidationError({"Error":
                                      ["Aucun client n'a été trouvé avec cet \
email."]})
            else:
                return queryset
        else:
            """
            if verifiy_pk(self.kwargs.get('pk')):
                pk = verifiy_pk(self.kwargs.get('pk'))
                client = get_object_or_404(Clients, id=pk,
                                           sales_contact=self.request.user)
                return client
            else:
                queryset = self.queryset.filter(sales_contact=self.request.user)
                if not queryset:
                    raise ValidationError({"EmptyQueryset":
                                          ["Vous n'avez aucun client."]})
                else:"""
            return self.queryset.filter(sales_contact=self.request.user)

    def create(self, request, *args, **kwargs):
        if request.user.equipe == 'gestion':
            return Response("Tu ne peux pas être ici tu es dans l'équipe de \
gestion.", status=status.HTTP_403_FORBIDDEN)
        serializers = ClientsSerializers(data=request.data)
        if serializers.is_valid():
            sales_contact = serializers.validated_data['sales_contact']
            try:
                User.objects.get(id=sales_contact.id, equipe="vente")
            except ObjectDoesNotExist:
                return Response("L'email ne correspond pas à l'email d'un \
membre de l'équipe de vente.",
                                status=status.HTTP_404_NOT_FOUND)
            try:
                serializers.save()
                return Response("formulaire enregistré")
            except IntegrityError:
                return Response("Formulaire non enregistré dans la base de \
données.", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializers.errors)

    def partial_update(self, request, *args, **kwargs):
        if request.user.equipe == 'gestion':
            return Response("Tu ne peux pas être ici tu es dans l'équipe de \
        gestion.", status=status.HTTP_403_FORBIDDEN)
        if not self.kwargs.get('pk'):
            return Response("Tu dois entrer un chiffre.",
                            status=status.HTTP_404_NOT_FOUND)
        else:
            pk = self.kwargs.get('pk')
            try:
                int(pk)
            except ValueError:
                return Response("Tu dois entrer un chiffre.",
                                status=status.HTTP_404_NOT_FOUND)
            client = get_object_or_404(Clients, id=pk,
                                       sales_contact=request.user)
            serializers = ClientsSerializers(client, data=request.data,
                                             partial=True)
            if serializers.is_valid():
                try:
                    serializers.save()
                    client.date_updated = timezone.now()
                    client.save()
                    return Response(serializers.data)
                except IntegrityError:
                    return Response("erreur pendant l'enregistrement du \
client.", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializers.errors)


class ContratsView(ModelViewSet):
    queryset = Contrats.objects.all()
    serializer_class = ContratsSerializers
    permission_classes = [EquipeDeVente]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        """
            Ajoutez une url pour voir tous les contrats d'un client
            api/clients/<pk>/contrats/
        """
        client_name = self.request.GET.get('name')
        client_email = self.request.GET.get('email')
        date_contrat = self.request.GET.get('date')
        montant_contrat = self.request.GET.get('montant')
        if client_name:
            queryset = self.queryset.filter(
                client_associe__last_name=client_name,
                sales_contact=self.request.user)
            if not queryset:
                raise ValidationError({"ContratNotFoud":
                                       ["Aucun contrat trouvé avec ce nom."]})
            else:
                return queryset
        elif client_email:
            queryset = self.queryset.filter(
                client_associe__email=client_email,
                sales_contact=self.request.user)
            if not queryset:
                raise ValidationError({"ContratNotFoud":
                                      ["Aucun contrat trouvé avec cet \
email."]})
            else:
                return queryset
        elif date_contrat:
            queryset = self.queryset.filter(
                payement_due=date_contrat,
                sales_contact=self.request.user)
            if not queryset:
                raise ValidationError({"ContratNotFoud":
                                      ["Aucun contrat trouvé avec cette \
date."]})
            else:
                return queryset
        elif montant_contrat:
            queryset = self.queryset.filter(
                amout=montant_contrat,
                sales_contact=self.request.user)
            if not queryset:
                raise ValidationError({"ContratNotFoud":
                                      ["Aucun contrat trouvé avec ce \
montant."]})
            else:
                return queryset
        else:
            if not self.queryset.filter(sales_contact=self.request.user):
                raise ValidationError({"EmptyQueryset":
                                      ["Aucun contrat n'a été trouvé"]})
            return self.queryset.filter(sales_contact=self.request.user)

    def create(self, request, *args, **kwargs):
        """
            à voir si un client peut avoir un ou plusieurs contrat
        """
        if not request.user.has_sales_permissions():
            return Response("Tu ne peux pas être ici tu es dans l'équipe de \
gestion.", status=status.HTTP_403_FORBIDDEN)
        else:
            form = self.serializer_class(data=request.data)
            if form.is_valid():
                form.validated_data['sales_contact'] = request.user
                form.save()
                return Response(form.data)
            else:
                return Response(form.errors)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.has_sales_permissions():
            return Response("Tu ne peux pas être ici tu es dans l'équipe de \
gestion.", status=status.HTTP_403_FORBIDDEN)
        else:
            if not verifiy_pk(self.kwargs.get('pk')):
                return Response("Tu dois entrer l'id du contrat.",
                                status=status.HTTP_404_NOT_FOUND)
            else:
                pk = verifiy_pk(self.kwargs.get('pk'))
                contrat = get_object_or_404(Contrats,
                                            id=pk,
                                            sales_contact=request.user)
                serializer = ContratsSerializers(contrat,
                                                 data=request.data,
                                                 partial=True)
                if serializer.is_valid():
                    try:
                        serializer.save()
                        contrat.date_updated = timezone.now()
                        contrat.save()
                        return Response(serializer.data)
                    except IntegrityError:
                        return Response("Erreur pendant la modification.",
                                        status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(serializer.errors)


class EventsView(ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [EquipeDeGestion]

    def create(self, request, *args, **kwargs):
        """
            url : POST api/clients/<pk>/events/
        """
        if not request.user.has_sales_permissions():
            return Response("Tu ne peux pas être ici tu es dans l'équipe de \
gestion.", status=status.HTTP_403_FORBIDDEN)
        else:
            if not verifiy_pk(self.kwargs.get('pk')):
                return Response("Tu dois entrer l'idée du client. \
'api/clients/id/events/'", status=status.HTTP_404_NOT_FOUND)
            else:
                pk = verifiy_pk(self.kwargs.get('pk'))
                serializer = EventsSerializers(data=request.data)
                if serializer.is_valid():
                    support_contact =\
                        serializer.validated_data['support_contact']
                    try:
                        User.objects.get(
                            id=support_contact.id, equipe="gestion")
                    except ObjectDoesNotExist:
                        return Response("La personne n'existe pas ou ne fait \
    pas partie de l'équipe de gestion.", status=status.HTTP_404_NOT_FOUND)
                    try:
                        client = Clients.objects.get(id=pk)
                    except ObjectDoesNotExist:
                        return Response("Le client n'existe pas.",
                                        status=status.HTTP_404_NOT_FOUND)
                    try:
                        serializer.validated_data['client_associe'] = client
                        serializer.save()
                        return Response(serializer.data)
                    except IntegrityError:
                        return Response("Erreur pendant la sauvegarde de \
l'event.", status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(serializer.errors)

    def get_queryset(self):
        """
            Nom du client/email/date evenement
        """
        client_name = self.request.GET.get('name')
        client_email = self.request.GET.get('email')
        date_event = self.request.GET.get('date')
        if client_name:
            queryset = self.queryset.filter(
                client_associe__last_name=client_name,
                support_contact=self.request.user)
            if not queryset:
                raise ValidationError({"ContratNotFoud":
                                      ["Aucun contrat trouvé avec ce nom.\
"]})
            else:
                return queryset
        elif client_email:
            queryset = self.queryset.filter(
                client_associe__email=client_email,
                support_contact=self.request.user)
            if not queryset:
                raise ValidationError({"ContratNotFoud":
                                      ["Aucun contrat trouvé avec cet \
email."]})
            else:
                return queryset
        elif date_event:
            queryset = self.queryset.filter(
                event_date=date_event,
                support_contact=self.request.user)
            if not queryset:
                raise ValidationError({"ContratNotFoud":
                                      ["Aucun contrat trouvé avec cette \
date."]})
            else:
                return queryset
        else:
            if not self.queryset.filter(
                        support_contact=self.request.user):
                raise ValidationError({"EmptyQueryset":
                                      ["Aucun event n'a été trouvé"]})
            return self.queryset.filter(support_contact=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        if request.user.has_sales_permissions():
            return Response("Tu ne peux pas être ici tu es dans l'équipe de \
vente.", status=status.HTTP_403_FORBIDDEN)
        else:
            if not verifiy_pk(self.kwargs.get('pk')):
                return Response("Tu dois entrer l'id de l'event.",
                                status=status.HTTP_404_NOT_FOUND)
            else:
                pk = verifiy_pk(self.kwargs.get('pk'))
                try:
                    event = Events.objects.get(id=pk,
                                               support_contact=request.user)
                    serializer = EventsSerializers(event, data=request.data,
                                                   partial=True)
                    if serializer.is_valid():
                        try:
                            serializer.save()
                            event.date_updated = timezone.now()
                            event.save()
                            return Response(serializer.data)
                        except IntegrityError:
                            return Response("L'event n'a pas été modifié.",
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(serializer.errors)
                except ObjectDoesNotExist:
                    return Response("Aucun event trouvé avec cet id.",
                                    status=status.HTTP_404_NOT_FOUND)